#!/bin/bash
# About: script for converting GT annotation from yolo format (normalized format with maxHeight and maxWidth)
# to COCO format (non-normalized)
# contact: sharib.ali@eng.ox.ac.uk

# change me
DATA_DIR=../annotationImages_and_labels

#-------
BASE_FOLDER=../fileFormatConverters
CLASS_NAMES=../endo.names

if [ -d "$RESULT_FOLDER" ]; then rm -Rf $RESULT_FOLDER; fi

# change me (if you want to rename the folder to something else)
RESULT_FOLDER=../csvFiles

# first make sure the list of files exist in your dataFolder
ext='.jpg'
j=0
fileTrainList=endoTrainList.txt

if [ -f $fileTrainList ] ; then
    rm $fileTrainList
fi

for i in `ls ${DATA_DIR} | grep $ext`; do
#echo $i
    echo ${DATA_DIR}/$i >> $fileTrainList
    j=$((j+1))
done

# change me (only if its not same, hard-coded inside code so should be fine!)
fileTrainListCSV=train_endo_rescale.csv

if [ -f $fileTrainListCSV ] ; then
    rm $fileTrainListCSV
fi

echo "printing csv file for yolo ---> coco format"
python $BASE_FOLDER/yolo2csv.py -baseDataFolder $DATA_DIR -pathToClassNames $CLASS_NAMES  -csvFileFolder $RESULT_FOLDER


# split into train-val set
echo "splitting csv file for train-val set ---> coco format"


python $BASE_FOLDER/create_train_val_lists.py -csvFile_trainingSet train_endo_rescale.csv -saveFolder $RESULT_FOLDER

echo "COCO format for your detection is now ready!!! Enjoy training !!!"
