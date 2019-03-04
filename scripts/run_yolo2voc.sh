#!/bin/bash
# About: script for converting GT annotation from yolo format (normalized format with maxHeight and maxWidth)
# to COCO format (non-normalized)
# contact: sharib.ali@eng.ox.ac.uk

# change me
DATA_DIR=../annotationImages_and_labels

DATA_DIR=/Users/shariba/development/EAD2019_testDeployment/'test_generalization_2'
#-------
BASE_FOLDER=../fileFormatConverters
CLASS_NAMES=../endo.names

if [ -d "$RESULT_FOLDER" ]; then rm -Rf $RESULT_FOLDER; fi

# change me (if you want to rename the folder to something else)
RESULT_FOLDER=../csvFiles
RESULT_FOLDER=/Users/shariba/development/EAD2019_testDeployment/gen_VOC

# first make sure the list of files exist in your dataFolder
ext='.jpg'
j=0

echo "convert to VOC format..."

python $BASE_FOLDER/any2voc.py -baseImgFolder $DATA_DIR -baseBoxFolder $DATA_DIR -pathToClassNames $CLASS_NAMES  -outFolder $RESULT_FOLDER -datatype 'GT'


