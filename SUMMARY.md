**TACO: Trash Annotations in Context** is a dataset for instance segmentation, semantic segmentation, and object detection tasks. It is used in the waste recycling industry. 

The dataset consists of 1500 images with 9823 labeled objects belonging to 60 different classes including *plastic_film*, *unlabeled_litter*, *cigarette*, and other: *clear_plastic_bottle*, *plastic_bottle_cap*, *other_plastic_wrapper*, *other_plastic*, *drink_can*, *plastic_straw*, *disposable_plastic_cup*, *other_carton*, *styrofoam_piece*, *glass_bottle*, *pop_tab*, *plastic_lid*, *normal_paper*, *paper_cup*, *metal_bottle_cap*, *single-use_carrier_bag*, *other_plastic_bottle*, *aluminium_foil*, *drink_carton*, *corrugated_carton*, *disposable_food_container*, *tissues*, *crisp_packet*, *plastic_utensils*, *rope&strings*, and 32 more.

Images in the TACO dataset have pixel-level instance segmentation annotations. Due to the nature of the instance segmentation task, it can be automatically transformed into a semantic segmentation (only one mask for every class) or object detection (bounding boxes for every object) tasks. All images are labeled (i.e. with annotations). There are no pre-defined <i>train/val/test</i> splits in the dataset. Also the dataset includes ***batch*** and ***scene*** image-level tags, ***supercategory*** object tag. The dataset was released in 2019.

Here is a visualized example for randomly selected sample classes:

[Dataset classes](https://github.com/dataset-ninja/taco/raw/main/visualizations/classes_preview.webm)
