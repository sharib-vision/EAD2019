# EAD2019 Challenge
![Build Status](https://travis-ci.org/sharibox/EAD2019.svg?branch=master)

#### About:
Endoscopic Artefact Detection (EAD) is a core challenge in facilitating diagnosis and treatment of diseases in hollow organs. Precise detection of specific artefacts like pixel saturations, motion blur, specular reflections, bubbles and debris is essential for high-quality frame restoration and is crucial for realising reliable computer-assisted tools for improved patient care. The challenge is sub-divided into three tasks: 

- Multi-class artefact detection: Localization of bounding boxes and class labels for 6 7  artefact classes for given frames.
- Region segmentation: Precise boundary delineation of detected artefacts. 
- Detection generalization: Detection performance independent of specific data type and source.


Website to [EAD2019-Challenge](https://ead2019.grand-challenge.org/EAD2019)

#### What you will find here?

- [Annotation file format converters](https://github.com/sharibox/EAD2019/tree/master/fileFormatConverters)

- [test script](https://github.com/sharibox/EAD2019/tree/master/scripts) 

- [configuring your training images and annotations](https://github.com/sharibox/EAD2019/tree/master/annotationImages_and_labels) 

- [evaluation: mAP and IoU](https://github.com/sharibox/EAD2019/tree/master/evaluation_mAP-IoU)


#### Semantic segmentation (New)

- [via to mask image converted](https://github.com/sharibox/EAD2019/blob/master/jsonViaAnnotation_maskImage.py)

- [DICE-JACCARD](https://github.com/sharibox/annotationTools)

 ``Note: For semantic segmentation we use only 5 classes {'Instrument', 'Specularity', 'Artefact' , 'Bubbles' and 'Saturation'}``


