#!/bin/bash
#=========================================================================
#
# Project:   EAD2019 challenge
# Language:  bash
# Begin:     2019-03-05
#
# Author: Sharib Ali
# Responsible person: Sharib Ali <sharib.ali@eng.ox.ac.uk>
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#           FILES USED
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# evaluation_mAP-IoU/compute_mAP_IoU.py
# evaluation_semantic/semanticEval_dice_Jaccard_Overall.py
# overallEvaluations.py
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#           FILE   STRUCTURE TO BE LOADED
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#   - ead2019_testSubmission.zip
#       - detection_bbox
#       - semantic_masks
#       - generalization_bbox
# Please note: for semantic you will need to upload both semantic_bbox and semantic_masks (single folder is not accepted!)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

BASE_DIR=/home/ead2019/app
INPUT_FILES='/input'
MYDIR=$INPUT_FILES

# count number of directories
shopt -s nullglob
numfiles=($INPUT_FILES/*)
numfiles=${#numfiles[@]}

DIRS=`ls -l $MYDIR | grep '^d' | awk '{print $9}'`

RESULT_FOLDER='/home/ead2019/output'

for DIR in $DIRS
do
    echo "directory considering......"$DIRS
    # DETECTION
    if [ "$DIR" == "detection_bbox" ]; then
        echo "detection detected"
        python $BASE_DIR/evaluation_EAD2019_allFiles/compute_mAP_IoU.py  $MYDIR/detection_bbox $BASE_DIR/groundTruths_EAD2019/detection_bbox $RESULT_FOLDER metrics_det.json
    fi
    # SEMANTIC
    if [ "$DIR" == "semantic_masks" ]; then
        echo "semantic detected"
        # TODO!!!: make a function to estimate average dice and jaccard over all images
        python $BASE_DIR/evaluation_EAD2019_allFiles/semanticEval_dice_Jaccard_Overall.py --GT_maskDIR $MYDIR/semantic_masks/ --Eval_maskDIR $BASE_DIR/groundTruths_EAD2019/semantic_masks/ --Result_dir $RESULT_FOLDER --jsonFileName metrics_sem.json
    fi
    # GENERALIZATION
    if [ "$DIR" == "generalization_bbox" ]; then
        echo "generalization detected"
        python $BASE_DIR/evaluation_EAD2019_allFiles/compute_mAP_IoU.py  $MYDIR/generalization_bbox $BASE_DIR/groundTruths_EAD2019/generalization_bbox $RESULT_FOLDER  metrics_gen.json
    fi
done

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#            COMPUTE THE FINAL METRICS.JSON for leaderboard
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
shopt -s nullglob
numfiles=($RESULT_FOLDER/*json)
numfiles=${#numfiles[@]}
echo "COMPUTING FINAL METRICS....identified json files $numfiles"
RESULT_FOLDER_FINAL='/output'
for DIR in $RESULT_FOLDER
do
# all
    if [ $numfiles == 3 ]; then
        # first find the generalization score
         python $BASE_DIR/evaluation_EAD2019_allFiles/compute_score_g.py \
            --detectionMetric $RESULT_FOLDER/metrics_det.json \
            --generalizationMetric $RESULT_FOLDER/metrics_gen.json\
            --Result_dir $RESULT_FOLDER \
            --jsonFileName metric_gen_score.json

        python $BASE_DIR/evaluation_EAD2019_allFiles/overallEvaluations.py \
            --detectionMetric $RESULT_FOLDER/metrics_det.json \
            --generalizationMetric $RESULT_FOLDER/metric_gen_score.json\
            --semanticMetric  $RESULT_FOLDER/metrics_sem.json \
            --caseType 3\
            --Result_dir  ${RESULT_FOLDER_FINAL}\
            --jsonFileName metrics.json

# it can be either both semantic and detection
    elif [ $numfiles == 2 ]; then
        for jsonFile in `ls $RESULT_FOLDER/ |grep '.json'`;do
            IFS='_' read -r -a array <<< "$jsonFile"
        done

        if [ "${array[1]}" == 'sem.json' ]; then
            python $BASE_DIR/evaluation_EAD2019_allFiles/overallEvaluations.py \
            --detectionMetric $RESULT_FOLDER/metrics_det.json \
            --semanticMetric  $RESULT_FOLDER/metrics_sem.json \
            --caseType 5\
            --Result_dir  ${RESULT_FOLDER_FINAL} \
            --jsonFileName metrics.json

        elif [ "${array[1]}" == 'gen.json' ]; then
            # detection and generalization
            python $BASE_DIR/evaluation_EAD2019_allFiles/compute_score_g.py \
            --detectionMetric $RESULT_FOLDER/metrics_det.json \
            --generalizationMetric $RESULT_FOLDER/metrics_gen.json\
            --Result_dir $RESULT_FOLDER \
            --jsonFileName metric_gen_score.json

            python $BASE_DIR/evaluation_EAD2019_allFiles/overallEvaluations.py \
            --generalizationMetric $RESULT_FOLDER/metric_gen_score.json\
            --detectionMetric $RESULT_FOLDER/metrics_det.json \
            --caseType 4\
            --Result_dir  ${RESULT_FOLDER_FINAL}\
            --jsonFileName metrics.json
        fi
# it can be either generalization or detection
    elif [ $numfiles == 1 ]; then
        for jsonFile in `ls $RESULT_FOLDER/ |grep '.json'`;do
            IFS='_' read -r -a array <<< "$jsonFile"
            echo ${array[1]}
        done
        if [ "${array[1]}" == 'sem.json' ]; then
            python $BASE_DIR/evaluation_EAD2019_allFiles/overallEvaluations.py \
            --semanticMetric  $RESULT_FOLDER/metrics_sem.json \
            --caseType 1\
            --Result_dir  ${RESULT_FOLDER_FINAL} \
            --jsonFileName metrics.json
        elif [ "${array[1]}" == 'det.json' ]; then
            echo "detected file is"${jsonFile[1]}
            python $BASE_DIR/evaluation_EAD2019_allFiles/overallEvaluations.py \
            --detectionMetric $RESULT_FOLDER/metrics_det.json\
            --caseType 0\
            --Result_dir  $RESULT_FOLDER_FINAL\
            --jsonFileName metrics.json
        else
        echo "provied file is generalization which requires both detection and generaliz...."
        fi
    fi
done
