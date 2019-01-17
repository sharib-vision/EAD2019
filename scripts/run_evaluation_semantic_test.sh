#!/bin/bash
# About: script for converting GT annotation from yolo format (normalized format with maxHeight and maxWidth)
# to COCO format (non-normalized)
# contact: sharib.ali@eng.ox.ac.uk

# change me

CURRENT_DIR=`pwd`
cd $CURRENT_DIR

DATA_DIR=$CURRENT_DIR/masks
echo 'dataDir is' $DATA_DIR

#-------
BASE_FOLDER=$CURRENT_DIR/evaluation_semantic
RESULT_FOLDER=$CURRENT_DIR/semantic_EAD2019_results
mkdir -p $RESULT_FOLDER

python $BASE_FOLDER/semanticEval_dice_Jaccard.py --GT_maskImage $DATA_DIR/0000600_mask.tif --Eval_maskImage $DATA_DIR/0000600_mask.tif --Result_dir $RESULT_FOLDER 

# TODO: grep values from txt file and put it in json file
echo " Semantic Evaluation complete !!!"
