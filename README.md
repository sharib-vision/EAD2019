# EAD2019 Challenge
![Build Status](https://travis-ci.org/sharibox/EAD2019.svg?branch=master)
[![Run Status](https://api.shippable.com/projects/5c408fe786df400800bbfbc4/badge?branch=master)]()

#### About:
Endoscopic Artefact Detection (EAD) is a core challenge in facilitating diagnosis and treatment of diseases in hollow organs. Precise detection of specific artefacts like pixel saturations, motion blur, specular reflections, bubbles and debris is essential for high-quality frame restoration and is crucial for realising reliable computer-assisted tools for improved patient care. The challenge is sub-divided into three tasks: 

- Multi-class artefact detection: Localization of bounding boxes and class labels for 7  artefact classes for given frames.
- Region segmentation: Precise boundary delineation of detected artefacts. 
- Detection generalization: Detection performance independent of specific data type and source.

**Checkout the updates of this challenge here:** [EAD2019-Challenge](https://ead2019.grand-challenge.org/EAD2019)

#### What you will find here?

- [annotation file format converters](https://github.com/sharibox/EAD2019/tree/master/fileFormatConverters)

- [test script](https://github.com/sharibox/EAD2019/tree/master/scripts) 

- [configuring your training images and annotations](https://github.com/sharibox/EAD2019/tree/master/annotationImages_and_labels) 

- [detection evaluation: mAP and IoU](https://github.com/sharibox/EAD2019/tree/master/evaluation_mAP-IoU)

- [via to mask image converted](https://github.com/sharibox/EAD2019/blob/master/jsonViaAnnotation_maskImage.py)

- [semantic evaluation: DICE-JACCARD](https://github.com/sharibox/EAD2019/tree/master/evaluation_semantic)

#### Artefact detection (updated!)

- 7 classes for artefact detection. Below shows the distribution of samples in each artefact class. 
- Total labeled classes: **17818**
- Total labels per class: **[5835, 1122, 5096, 675, 1558, 3079, 453]**

![bbox](imgs/bboxhistogram_train_corrected.jpg)


#### Semantic segmentation (New)

 - For semantic segmentation we use only 5 classes ``{'Instrument', 'Specularity', 'Artefact' , 'Bubbles' and 'Saturation'}``

    ![mask_file](imgs/mask_overlayimage.jpg)

 
 


