#!/bin/bash
# About: script for converting GT annotation from yolo format (normalized format with maxHeight and maxWidth)
# to COCO format (non-normalized)
# contact: sharib.ali@eng.ox.ac.uk

# change me
DATA_DIR=../mAP-IoU_testdata

#-------
BASE_FOLDER=../evaluation_mAP-IoU
CLASS_NAMES=../endo.names

if [ -d "$RESULT_FOLDER" ]; then rm -Rf $RESULT_FOLDER; fi

# change me (if you want to rename the folder to something else)
RESULT_FOLDER=../mAP-IOU_EAD2019_results/

# compute the mAP and IoU (Please note that weighted value will be scored, see challenge website for details, https://ead2019.grand-challenge.org/Evaluation/)

python $BASE_FOLDER/compute_mAP_IoU.py $DATA_DIR/predicted $DATA_DIR/ground-truth $RESULT_FOLDER

# grep values from txt file and put it in json file


echo " Evaluation complete !!!"
