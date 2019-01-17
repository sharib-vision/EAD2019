#!/bin/bash
# About: script for converting GT annotation from yolo format (normalized format with maxHeight and maxWidth)
# to COCO format (non-normalized)
# contact: sharib.ali@eng.ox.ac.uk

# change me

CURRENT_DIR=`pwd`
cd $CURRENT_DIR

#cd "$(CURRENT_DIR "$0")"

DATA_DIR=$CURRENT_DIR/mAP-IoU_testdata

echo 'dataDir is' $DATA_DIR
#-------
BASE_FOLDER=$CURRENT_DIR/evaluation_mAP-IoU
CLASS_NAMES=$CURRENT_DIR/endo.names

# change me (if you want to rename the folder to something else)
RESULT_FOLDER=$CURRENT_DIR/mAP-IOU_EAD2019_results

mkdir -p $RESULT_FOLDER

# compute the mAP and IoU (Please note that weighted value will be scored, see challenge website for details, https://ead2019.grand-challenge.org/Evaluation/)

#PARAMETERS=$BASE_FOLDER/compute_mAP_IoU.py \#$DATA_DIR/predicted\#$DATA_DIR/ground-truth\#$RESULT_FOLDER
#echo $PARAMETERS

python $BASE_FOLDER/compute_mAP_IoU.py $DATA_DIR/predicted $DATA_DIR/ground-truth $RESULT_FOLDER

# grep values from txt file and put it in json file


echo " Evaluation complete !!!"
