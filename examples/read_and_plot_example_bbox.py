#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 21 13:24:24 2018

@author: ead2019
"""

def read_img(imfile):
    
    import cv2
    
    return cv2.imread(imfile)[:,:,::-1]


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


def yolo2voc(boxes, imshape):
    
    import numpy as np 
    m, n = imshape[:2]
    
    box_list = []
    for b in boxes:
        cls, x, y, w, h = b
        
        x1 = (x-w/2.)
        x2 = x1 + w
        y1 = (y-h/2.)
        y2 = y1 + h
        
        # absolute:
        x1 = x1 * n ; x2 = x2*n
        y1 = y1 * m ; y2 = y2*m
        
        box_list.append([cls, x1,y1,x2,y2])
    
    if len(box_list)>0:
        box_list = np.vstack(box_list)
        
    return box_list


def plot_boxes(ax, boxes, labels):
    
    import seaborn as sns 
    
    color_pal = sns.color_palette('hls', n_colors = len(labels))
    
    for b in boxes:
        cls, x1, y1, x2, y2 = b
        ax.plot([x1,x2,x2,x1,x1], [y1,y1,y2,y2,y1],lw=2, color=color_pal[int(cls)])
        
    return []


def read_obj_names(textfile):
    
    import numpy as np 
    classnames = []
    
    with open(textfile) as f:
        for line in f:
            line = line.strip('\n')
            if len(line)>0:
                classnames.append(line)
            
    return np.hstack(classnames)


if __name__=="__main__":
    
    """
    Example script to read and plot bounding box annotations (which are provided in <x,y,w,h> format)
    
    (x,y) - box centroid
    (w,h) - width and height of box in normalised. 
    """
    import pylab as plt 
    
    imgfile = '../annotationImages_and_labels/00003.jpg'
    bboxfile = '../annotationImages_and_labels/00003.txt'
    
    classfile = '../class_list.txt'
    classes = read_obj_names(classfile)
    
    img = read_img(imgfile)
    boxes = read_boxes(bboxfile)
    
    # convert boxes from (x,y,w,h) to (x1,y1,x2,y2) format for plotting
    boxes_abs = yolo2voc(boxes, img.shape)
    
    
    fig, ax = plt.subplots()
    ax.imshow(img)
    plot_boxes(ax, boxes_abs, classes)
    plt.show()
    