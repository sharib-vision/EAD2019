#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 13 10:52:32 2018

@author:  ead2019
"""
def process_image(image_data):
    image = cv2.imread(image_data.image_path)
    image = cv2.putText(image, image_data.image_name, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    for ann in image_data.annotations:
        box_color = (0, 255, 0)  #Green
        if ann.difficult or ann.truncated:
            box_color = (0, 0, 255) #Red
        image = cv2.rectangle(image, (ann.xmin, ann.ymin), (ann.xmax, ann.ymax), box_color, args.line_thickness)
        image = cv2.putText(image, ann.name, (ann.xmin, ann.ymin), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    return image


def locate_files(infolder, ext='.txt'):

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
            box = np.hstack(line.split()) # just append the line.
            lines.append(box)

    return np.array(lines)

def write_boxes_voc(boxes_voc, savepath):
    
    with open(savepath, 'w') as f:
        if len(boxes_voc) > 0:
            for bbox in boxes_voc:
                f.write(' '.join(bbox)+'\n')
        else:
            # create new empty file.
            open(fname, 'a').close()

    return []

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


def convert_boxes(boxes, class_names, datatype, imgshape):

    nrows, ncols = imgshape
    data = []

    if len(boxes) > 0:
        for bbox in boxes:
            if datatype=='GT':
                cls, b1, b2, b3, b4 = bbox
            elif datatype=='Pred':
                cls, conf, b1, b2, b3, b4 = bbox
            else:
                raise Exception('datatype should be either \'GT\' or \'Pred\'. The value of datatype was: {}'.format(datatype))

            # check whether we have been given the name already.
            try:
                cls = int(cls)
                cls_name = class_names[int(cls)]
            except:
                cls_name = str(cls)

            # check whether yolo or not.
            bbox_bounds = np.hstack([b1,b2,b3,b4]).astype(np.float)

            if bbox_bounds.max() < 1.1:
                # yolo:
#                x1 = (bbox_bounds[0] - bbox_bounds[2]) / 2. * ncols
#                y1 = (bbox_bounds[1] - bbox_bounds[3]) / 2. * nrows
#                x2 = (bbox_bounds[0] + bbox_bounds[2]) / 2. * ncols
#                y2 = (bbox_bounds[1] + bbox_bounds[3]) / 2. * nrows
                                
                # yolo 2 voc
                x = bbox_bounds[0] * ncols
                w = bbox_bounds[2] * ncols
                
                y = bbox_bounds[1] * nrows
                h = bbox_bounds[3] * nrows
                
                x1 = x - w/2
                x2 = x + w/2
                y1 = y - h/2
                y2 = y + h/2
       
            else:
                # assume voc:
                x1,y1,x2,y2 = bbox_bounds

            # clip to image bounds
            x1 = int(np.clip(x1, 0, ncols-1))
            y1 = int(np.clip(y1, 0, nrows-1))
            x2 = int(np.clip(x2, 0, ncols-1))
            y2 = int(np.clip(y2, 0, nrows-1))

            # strictly speaking we should have the following but we can implement a filter instead.
            # assert(x2>x1 and y2>y1) # check this is true! for voc
            if x2>x1 and y2>y1:
                # only append if this constraint is satisfied.
                if datatype=='GT':
                    data.append([cls_name, x1, y1, x2, y2])
                elif datatype=='Pred':
                    data.append([cls_name, float(conf), x1,y1,x2,y2])

        if len(data) > 0:
            return np.vstack(data) # create an array.
        else:
            return data
    else:
        return data


class_rgb = [
    (0, 0, 255), (255, 0, 0), (0, 255, 0), (255, 255, 0), (0, 255, 255),
    (255, 0, 255), (192, 192, 192), (128, 128, 128), (128, 0, 0),
    (128, 128, 0), (0, 128, 0), (128, 0, 128), (0, 128, 128), (0, 0, 128)]
import numpy as np
class_rgb = np.array(class_rgb)


classListBBOX=['specularity', 'saturation', 'artifact', 'blur', 'contrast', 'bubbles', 'instrument', 'blood']

if __name__=="__main__":

    import numpy as np
    import pandas as pd
    import argparse
    import os

    parser = argparse.ArgumentParser()
    parser.add_argument('-baseImgFolder',default='/Users/shariba/development/challenge2020/EndoCV-EAD2020-test/EAD2020_testData/Detection/detection_test_EAD2020/', action='store', help='please include the full path of the folder of the images', type=str)
    parser.add_argument('-baseBoxFolder',default='/Users/shariba/development/challenge2020/EndoCV-EAD2020-test/EAD2020_testData/Detection/bbox_detection_test_EAD2020/', action='store', help='please include the full path of the folder of the bounding boxes', type=str)
    parser.add_argument('-pathToClassNames', default='../endo.names',action='store', help='please include the full path to the class names file', type=str)
    parser.add_argument('-outFolder', default= 'tmp', action='store', help='please include the full path to the output folder for saving converted bounding boxes', type=str)
    parser.add_argument('-datatype', default= 'GT', action='store', help='please enter \'GT\' if bounding boxes are ground truth or \'Pred\' if boxes have been predicted', type=str)
    args = parser.parse_args()

    """
    Create output folder.
    """
    if not os.path.exists(args.outFolder):
        os.makedirs(args.outFolder)

    """
    Read the bounding box classes.
    """
    class_name_file = args.pathToClassNames
    bbox_class_names = read_obj_names(class_name_file)
    class_names = bbox_class_names # has to be list.

    """
    Read the bounding boxes.
    """
    # load the respective bounding box info and write out a csv.
    boxpaths = locate_files(args.baseBoxFolder, '.txt')
    imgpaths = np.hstack([(boxfile.replace(args.baseBoxFolder, args.baseImgFolder)).replace('.txt', '.jpg') for boxfile in boxpaths])
    savepaths = np.hstack([(boxfile.replace(args.baseBoxFolder, args.outFolder)) for boxfile in boxpaths])
    
    debug = 0
    
    import cv2
    for ii, imgpath in enumerate(imgpaths):
        # print(ii, imgpath)
        img = read_img(imgpath)
        image= cv2.imread(imgpath)
        nrows, ncols, _ = img.shape
        boxes = read_boxes(boxpaths[ii]) # read in boxes

        # check boxes, is it yolo or is it voc already?
        boxes_voc = convert_boxes(boxes, class_names, args.datatype, imgshape=(nrows, ncols))
        
        if debug:
            for i in range (0, len(boxes_voc)):
                for l in range (0, len(classListBBOX)):
                    if boxes_voc[i][0]== classListBBOX[l]:
                        color = class_rgb[l].tolist()
                        cv2.rectangle(image, (int(boxes_voc[i][1]), int(boxes_voc[i][2])), (int(boxes_voc[i][3]), int(boxes_voc[i][4])), color)

            if imgpath.split('/')[-1]=='ead2020_testD_0129.jpg':
                cv2.imshow("test", image)
                cv2.waitKey(50)
            
        else:
            write_boxes_voc(boxes_voc, savepaths[ii])
        
        # check the image overlay for some samples
        
