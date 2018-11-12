#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 11 12:50:49 2018

@author: shariba
"""        
        
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

def read_obj_names(textfile):

    classnames = []

    with open(textfile) as f:
        for line in f:
            line = line.strip('\n')
            if len(line)>0:
                classnames.append(line)

    return np.hstack(classnames)


debug = 0
useParsing=0

if __name__=="__main__":

    import numpy as np
#    import pandas as pd
    import argparse
    import glob

    annotationImagePaths=''
    classnames=''
    
    if useParsing:
        
        parser = argparse.ArgumentParser()
        parser.add_argument('-bounding_boxes_folder', action='store', help='please include the full path of the folder with bounding boxes (.txt)', type=str)
        parser.add_argument('-class_lists', action='store', help='class list file (fullpath)', type=str)
        args = parser.parse_args()
        classtextfile= args.class_lists
        annotationImagePaths=args.bounding_boxes_folder
        # read class names (equivalent to indexes stored in annotation Oth index)
        classnames=read_obj_names(classtextfile)
        
    else:
        #use you explicit path settings here if you dont want to parse
        bbox_base_path='/Users/shariba/development/dockerContainers/OpenLabeling/phase_1_annotations/'
        bbox_subFolder='fused_sharib_felix_bboxes/'
        #
        fileName='00002.txt'
        classFileName='class_list.txt'
        classtextfile = bbox_base_path+classFileName
        # read class names in bbox (equivalent to indexes stored in annotation bbox[0-len(bboxes)][0]Oth index)
        textfile = bbox_base_path+bbox_subFolder+fileName
        bboxes=read_boxes(textfile)
        classnames=read_obj_names(classtextfile)
        annotationImagePaths=bbox_base_path+bbox_subFolder
        if debug:
            print('box class identified:', bboxes[0][0])
            i =(int)(bboxes[0][0])
            print('corresponding name of the class type:', classnames[i])
            print('total boxes annotated in this file:', len(bboxes))
            

    # histogram
    ext = ['*.txt']
    classCounter = [ 0, 0, 0, 0, 0, 0, 0 ]
    print(annotationImagePaths)
    for filename in sorted(glob.glob(annotationImagePaths + ext[0], recursive = True)):
        if debug:
            print(filename) 
        #1) read 
        bboxes=read_boxes(filename)
        #2) loop throgh for class types in array
        for i in range (len(bboxes)):
            for j in range (len(classnames)):
                if (j == (int)(bboxes[i][0])): 
                     classCounter[j]=((int)(classCounter[j])+1) 
    # percentage 
    label = (classCounter/np.sum(classCounter))*100 
    # plot            
    import matplotlib.pyplot as plt    
    fig, ax = plt.subplots()
    x = np.arange(7)
    plt.bar(x, classCounter)
    plt.xticks(x, (classnames))
    plt.xticks(rotation=45)
    for i in range(len(classCounter)):
        plt.text(-0.35+i , classCounter[i]+10, s = str(round(label[i],2)), size = 10,color='red', fontweight='bold')
    plt.show()
    
