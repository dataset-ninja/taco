from collections import defaultdict
import supervisely as sly
import os
from dataset_tools.convert import unpack_if_archive
import src.settings as s
from urllib.parse import unquote, urlparse
from supervisely.io.fs import get_file_name, get_file_size
from supervisely.io.json import load_json_file
import shutil

from tqdm import tqdm

def download_dataset(teamfiles_dir: str) -> str:
    """Use it for large datasets to convert them on the instance"""
    api = sly.Api.from_env()
    team_id = sly.env.team_id()
    storage_dir = sly.app.get_data_dir()

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, str):
        parsed_url = urlparse(s.DOWNLOAD_ORIGINAL_URL)
        file_name_with_ext = os.path.basename(parsed_url.path)
        file_name_with_ext = unquote(file_name_with_ext)

        sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
        local_path = os.path.join(storage_dir, file_name_with_ext)
        teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

        fsize = api.file.get_directory_size(team_id, teamfiles_dir)
        with tqdm(
            desc=f"Downloading '{file_name_with_ext}' to buffer...",
            total=fsize,
            unit="B",
            unit_scale=True,
        ) as pbar:        
            api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)
        dataset_path = unpack_if_archive(local_path)

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, dict):
        for file_name_with_ext, url in s.DOWNLOAD_ORIGINAL_URL.items():
            local_path = os.path.join(storage_dir, file_name_with_ext)
            teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

            if not os.path.exists(get_file_name(local_path)):
                fsize = api.file.get_directory_size(team_id, teamfiles_dir)
                with tqdm(
                    desc=f"Downloading '{file_name_with_ext}' to buffer...",
                    total=fsize,
                    unit="B",
                    unit_scale=True,
                ) as pbar:
                    api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)

                sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
                unpack_if_archive(local_path)
            else:
                sly.logger.info(
                    f"Archive '{file_name_with_ext}' was already unpacked to '{os.path.join(storage_dir, get_file_name(file_name_with_ext))}'. Skipping..."
                )

        dataset_path = storage_dir
    return dataset_path
    
def count_files(path, extension):
    count = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(extension):
                count += 1
    return count
    
def convert_and_upload_supervisely_project(
    api: sly.Api, workspace_id: int, project_name: str
) -> sly.ProjectInfo:
    dataset_path = os.path.join("TACO","data")
    ann_path = os.path.join(dataset_path,"annotations.json")
    batch_size = 30
    ds_name = "ds"
    errors = []

    # for r,d,f in os.walk(dataset_path): # RENAME FILES BECAUSE OF DUBLICATE
    #     for file in f:
    #         if file != "annotations.json":
    #             old_path = os.path.join(r,file)
    #             new_filename = f"{os.path.basename(r)}_{file}"
    #             new_path = os.path.join(r,new_filename)
    #             os.rename(old_path, new_path)


    def recreate_name(name):
        """
        from
        'batch_1\\batch_1_000006.jpg'
        to
        'batch_1/000012.jpg'
        """
        batch, badname = os.path.split(name)
        if 'IMG' in badname:
            print(1)
        normalname = badname.split(batch)[-1][1:]
        return f"{batch}/{normalname}"

    def create_ann(image_path):
        labels = []
        tags = []

        image_name = image_path.split(dataset_path)[-1][1:]
        image_name = recreate_name(image_name)
        img_height = image_name_to_shape[image_name][0]
        img_wight = image_name_to_shape[image_name][1]

        subfolder_value = image_path.split("\\")[-2]
        subfolder = sly.Tag(subfolder_meta, value=subfolder_value)
        tags.append(subfolder)

        scene_data = image_name_to_scene.get(image_name)
        if scene_data is not None:
            for curr_scene_data in scene_data:
                cat_value = idx_to_scene_categories.get(curr_scene_data)
                if cat_value is not None:
                    scene = sly.Tag(scene_meta, value=cat_value)
                    tags.append(scene)

        ann_data = image_name_to_ann_data[image_name]
        for curr_ann_data in ann_data:
            category_id = curr_ann_data[0]
            supercategory_value = idx_to_supercategory[category_id]
            supercategory = sly.Tag(supercategory_meta, value=supercategory_value)
            obj_class = idx_to_obj_class[category_id]
            polygons_coords = curr_ann_data[1]
            for coords in polygons_coords:
                exterior = []
                for i in range(0, len(coords), 2):
                    exterior.append([int(coords[i + 1]), int(coords[i])])
                if len(exterior) < 3:
                    errors.append(image_name)
                    continue
                poligon = sly.Polygon(exterior)
                label_poly = sly.Label(poligon, obj_class, tags=[supercategory])
                labels.append(label_poly)

            bbox_coord = curr_ann_data[2]
            rectangle = sly.Rectangle(
                top=int(bbox_coord[1]),
                left=int(bbox_coord[0]),
                bottom=int(bbox_coord[1] + bbox_coord[3]),
                right=int(bbox_coord[0] + bbox_coord[2]),
            )
            label_rectangle = sly.Label(rectangle, obj_class, tags=[supercategory])
            labels.append(label_rectangle)

        return sly.Annotation(img_size=(img_height, img_wight), labels=labels, img_tags=tags)


    project = api.project.create(workspace_id, project_name, change_name_if_conflict=True)
    supercategory_meta = sly.TagMeta("supercategory", sly.TagValueType.ANY_STRING)
    scene_meta = sly.TagMeta("scene", sly.TagValueType.ANY_STRING)
    subfolder_meta = sly.TagMeta("subfolder", sly.TagValueType.ANY_STRING)
    meta = sly.ProjectMeta(tag_metas=[supercategory_meta, scene_meta, subfolder_meta])

    dataset = api.dataset.create(project.id, ds_name, change_name_if_conflict=True)

    idx_to_obj_class = {}
    idx_to_supercategory = {}
    image_id_to_name = {}
    image_name_to_ann_data = defaultdict(list)
    image_name_to_shape = {}
    image_name_to_scene = {}
    idx_to_scene_categories = {}

    ann = load_json_file(ann_path)
    for curr_category in ann["categories"]:
        idx_to_supercategory[curr_category["id"]] = curr_category["supercategory"]
        obj_class = sly.ObjClass(curr_category["name"], sly.AnyGeometry)
        meta = meta.add_obj_class(obj_class)
        idx_to_obj_class[curr_category["id"]] = obj_class
    api.project.update_meta(project.id, meta.to_json())

    for curr_image_info in ann["images"]:
        image_id_to_name[curr_image_info["id"]] = curr_image_info["file_name"]
        image_name_to_shape[curr_image_info["file_name"]] = (
            curr_image_info["height"],
            curr_image_info["width"],
        )

    for curr_scene_info in ann["scene_annotations"]:
        image_id = curr_scene_info["image_id"]
        image_name_to_scene[image_id_to_name[image_id]] = curr_scene_info["background_ids"]

    for curr_ann_data in ann["annotations"]:
        image_id = curr_ann_data["image_id"]
        image_name_to_ann_data[image_id_to_name[image_id]].append(
            [curr_ann_data["category_id"], curr_ann_data["segmentation"], curr_ann_data["bbox"]]
        )

    for curr_scene_cat in ann["scene_categories"]:
        idx_to_scene_categories[curr_scene_cat["id"]] = curr_scene_cat["name"]

    images_names = [im_name for im_name in image_name_to_shape.keys()]
    images_names = [f"{im_name.split('/')[0]}_{im_name.split('/')[1]}" for im_name in images_names]

    subfolder_dict = defaultdict()
    for name in images_names:
        value = f"{name.split('_')[0]}_{name.split('_')[1]}"
        key = name
        subfolder_dict[key]= value

    progress = sly.Progress("Create dataset {}".format(ds_name), len(images_names))

    for img_names_batch in sly.batched(images_names, batch_size=batch_size):
        images_pathes_batch = [os.path.join(dataset_path,subfolder_dict[image_name], image_name) for image_name in img_names_batch]

        img_infos = api.image.upload_paths(dataset.id, img_names_batch, images_pathes_batch)
        img_ids = [im_info.id for im_info in img_infos]

        anns_batch = [create_ann(image_path) for image_path in images_pathes_batch]
        api.annotation.upload_anns(img_ids, anns_batch)

        progress.iters_done_report(len(img_names_batch))

    return project
