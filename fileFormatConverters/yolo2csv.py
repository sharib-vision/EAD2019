#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 13 10:52:32 2018

@author: felix and sharib
"""

def detect_imgs(infolder, ext='.tif'):

    import os

    items = os.listdir(infolder)

    flist = []
    for names in items:
        if (names.endswith(ext) or names.endswith(ext.upper())) and ('._' not in names):
            flist.append(os.path.join(infolder, names))

    return np.sort(flist)


def read_txt_file(txtfile):

    import numpy as np
    lines = []

    with open(txtfile, "r") as f:

        for line in f:
            line = line.strip()
            lines.append(line)

    return np.array(lines)


def read_boxes(txtfile):

    import numpy as np
    lines = []

    with open(txtfile, "r") as f:

        for line in f:
            line = line.strip()
            box = np.hstack(line.split()).astype(np.float)
            box[0] = int(box[0])
            lines.append(box)

    return np.array(lines)


def read_img(imgfile):

    import cv2

    return cv2.imread(imgfile)[:,:,::-1]


def read_obj_names(textfile):

    classnames = []

    with open(textfile) as f:
        for line in f:
            line = line.strip('\n')
            if len(line)>0:
                classnames.append(line)

    return np.hstack(classnames)


def construct_annot_table(boxes, class_names, imgpath, imgshape):

    data = []
    n_objects = len(boxes)

    for i in range(n_objects):

        bbox = boxes[i]
        class_int = bbox[0]
        class_name = class_names[int(class_int)]

        nrows, ncols = imgshape
        box = bbox[1:]
        box[0]*=ncols; box[2]*=ncols;
        box[1]*=nrows; box[3]*=nrows;
        box = box.astype(np.int)

        data.append([imgpath, box[0], box[1], box[2], box[3], class_name])

    return np.array(data)


if __name__=="__main__":

    import numpy as np
    import pandas as pd
    import argparse
    import os

    parser = argparse.ArgumentParser()
    parser.add_argument('-baseDataFolder', action='store', help='please include the full path of the folder (-->images+labels)', type=str)
    parser.add_argument('-pathToClassNames', action='store', help='filepath/filename.names', type=str)
    parser.add_argument('-csvFileFolder', action='store', help='csv file path to store', type=str)
    args = parser.parse_args()
    #
    # old_root = '/well/rittscher/projects/felix-Sharib/endoData/trainEndo_rescale'
    # new_root = '../Artifact Training Dataset/trainEndo_rescale_full'

    """
    Read the Box labels
    """
    if not os.path.exists(args.csvFileFolder):
        os.makedirs(args.csvFileFolder)

    class_name_file = args.pathToClassNames
    bbox_class_names = read_obj_names(class_name_file)
    class_names = bbox_class_names # has to be list.


    trainfile = 'endoTrainList.txt'
    csvTrainFile= 'train_endo_rescale.csv'

    # delete file if exists
    try:
        os.remove(csvTrainFile)
    except OSError:
        pass

    trainimgs = read_txt_file(trainfile)
    # testimgs = read_txt_file(testfile)


    # load the respective bounding box info and write out a csv.
    trainimgpaths = np.hstack([imfile.replace(args.baseDataFolder, args.baseDataFolder) for imfile in trainimgs])
    trainboxpaths = np.hstack([(imfile.replace(args.baseDataFolder, args.baseDataFolder).replace('.jpg','.txt')) for imfile in trainimgs])
    # print(enumerate(trainimgpaths))
    # for counter, value in enumerate(trainimgpaths):
    #     print(counter, value)

    all_annot_tables = []

    for ii, imgpath in enumerate(trainimgpaths):
        print(ii, imgpath)
        img = read_img(imgpath)
        nrows, ncols, _ = img.shape
        boxes = read_boxes(trainboxpaths[ii])

        # need to give absolute box sizes?
        annot_table = construct_annot_table(boxes, class_names, imgpath, imgshape=(nrows, ncols))
        annot_table = pd.DataFrame(annot_table)
        all_annot_tables.append(annot_table)

    all_annot_tables = pd.concat(all_annot_tables, ignore_index=True)

    """
    save out the final table.
    """
    all_annot_tables.to_csv('train_endo_rescale.csv', sep=',', index=None, columns=None, header=False)


    """
    split into train-test Dataset

    """
