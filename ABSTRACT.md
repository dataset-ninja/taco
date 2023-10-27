*TACO*, which stands for __Trash Annotations in Context__ is an open image dataset that focuses on waste in various real-world settings. It encompasses a collection of images depicting litter in diverse environments, ranging from tropical beaches to urban streets in places like London. The dataset is notable for its manual labeling and segmentation, providing a hierarchical taxonomy for object detection algorithms to train and evaluate their performance. It comprises 1,500 images that cover 60 distinct waste classes, including items like *aluminum_foil*, *batterie*, and *aluminum_blister_pack*.

TACO contains high resolution images, taken mostly by mobile phones. These are managed and stored by Flickr, whereas authors' server manages the annotations and runs periodically a crawler to collect more potential images of litter. Additionally, authors also selected some images from [source](https://openlittermap.com/). All images are under free copyright licences and are annotated and segmented by users using [online tool](http://tacodataset.org/annotate).

<img src="https://i.ibb.co/98fp8xJ/Screenshot-2023-10-27-132125.png" alt="image" width="400">

<span style="font-size: smaller; font-style: italic;">Distribution of image resolutions.</span>

Specifically, images are labeled with the scene tags to describe their background – these are not mutually exclusive – and litter instances are segmented and labeled using a hierarchical taxonomy with 60 categories of litter which belong to 28 super (top) categories, including a special category: Unlabeled litter for objects that are either ambiguous or not covered by the other categories.

<img src="https://i.ibb.co/ykht6jJ/Screenshot-2023-10-27-132440.png" alt="image" width="400">

<span style="font-size: smaller; font-style: italic;"> Proportion of images by background tag.</span>

Authors targeted 9 super categories based on the number of instances and merged the rest under the class name Other Litter. Authors call this TACO-10 and Figure below shows the size variability of annotations per category for this new taxonomy. Authors can see that most of the cigarettes, the third largest class, have an area less than 64 × 64 pixels.

<img src="https://i.ibb.co/tJR3dhY/Screenshot-2023-10-27-140039.png" alt="image" width="300">

<span style="font-size: smaller; font-style: italic;">  Histogram of bounding box sizes per category for TACO-10.</span>
