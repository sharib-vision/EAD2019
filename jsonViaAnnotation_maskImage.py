#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 16 17:25:52 2018

@author: ead2019
"""
''' ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Redundancies still might be present. Please use this at your own risk.

~~~~~~~~~~~~~converts via annotator () to corresponding label images~~~~~~~~~~
For via image annotator see: https://www.robots.ox.ac.uk/~vgg/software/via/via-2.0.1.html
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ '''

def rectangle(height, width, c0, r0 ):
    rr, cc = [r0, r0 + width, r0 + width, r0], [c0, c0, c0 + height, c0 + height]
    return skimage.draw.polygon(rr, cc)


''' Change me!!!'''
"""
 TODO: change 'dataset_dir' to your image directory
 Original_images (https://s3.amazonaws.com/semanticsegmentation-v1/semanticSegmentation_EAD2019.zip)
"""
dataset_dir= '../../via/semanticSegmentation_EAD2019/'
via_annotationFile = 'sampleJsonFile/via_EAD_Challenge2019_Semantic_v3_MALI_v15.json'


# todo: change to the class def
import json

annotations = json.load(open(via_annotationFile))
annotations_noDictKey = list(annotations.values())

import numpy as np
category = []
bbox = []
segment=[]
fileList=[]
result_tuple_from_segment=[]
    
with open(via_annotationFile) as json_data:
    data = json.load(json_data)
    for p in data["_via_img_metadata"].values():
        print(p)
        if len(p['regions'])!=0:
            fileList.append(p['filename'])
            segment.append(p['regions'])
            
            
            
# from segment find the dicts of polygon or other options
shapeFormat=[]
classCategory = []
segx = []
segy = []
rect = []
circ=[]
#len(segment)
debugLevel = 1
for i in range (0, len(segment)):
    seg = segment[i]
    
    shapeFormat_1=[]
    classCategory_1 = []
    segx_1 = []
    segy_1 = []
    rect_1 = []
    circ_1=[]
    
    for k in range (0, len(seg)):
        seg_1 = seg[k]
        seg2 = seg_1['region_attributes']
        seg1 = seg_1['shape_attributes']  
        # for class identification
        seg1_category = seg2['EAD-Challenge2019']
        boolean = []
        if len(seg1_category) == 5:
            categoryList = ['Instrument', 'Specularity', 'Artefact' , 'Bubbles', 'Saturation']
        else:
            categoryList = ['Instrument', 'Artefact' , 'Bubbles', 'Saturation']
            
        listBoolCat = list(seg1_category.values())
        x = {k:v for k,v in enumerate(listBoolCat) if v == True}
        classCategory_1.append(list(x))
       
        # for shape identification
        shapesArray=['polygon', 'polyline', 'circle', 'rect']
        seg2_shape = seg1['name']  
        
        if seg2_shape == shapesArray[1]:
            if debugLevel:
                print('polyline exists')
            shapeFormat_1.append(seg2_shape)
            segx_1.append(seg1['all_points_x'])
            segy_1.append(seg1['all_points_y'])
            
        elif seg2_shape == shapesArray[0]:
            if debugLevel:
                print('polygon exists')
            shapeFormat_1.append(seg2_shape)
            segx_1.append(seg1['all_points_x'])
            segy_1.append(seg1['all_points_y'])
            
        elif seg2_shape == shapesArray[2]:
            circleRegion=[]
            if debugLevel:
                print('circle exists')
            shapeFormat_1.append(seg2_shape)
            circleRegion.append(int(seg1['cx']))
            circleRegion.append(int(seg1['cy']))
            circleRegion.append(int(seg1['r']))
            circ_1.append(circleRegion)
            
        elif seg2_shape == shapesArray[3]:
            if debugLevel:
                print('rectangle exists')
            rectangleCoordinates=[]
            shapeFormat_1.append(seg2_shape)
            rectangleCoordinates.append(int(seg1['height']))
            rectangleCoordinates.append(int(seg1['width']))
            rectangleCoordinates.append(int(seg1['x']))
            rectangleCoordinates.append(int(seg1['y']))
            
            rect_1.append(rectangleCoordinates)
            
        else:
            print('unidentified')
            
        
   
    shapeFormat.append(shapeFormat_1)
    classCategory.append(classCategory_1)
    segx.append(segx_1)
    segy.append(segy_1)
    rect.append(rect_1)
    circ.append(circ_1)
 
    
classCategory = list(filter(None, classCategory))
shapeFormat = list(filter(None, shapeFormat))

#create your masks
import skimage.io
import skimage.draw
import os
from tifffile import imsave
from miscClasses import clearArray

categoryList = ['Instrument', 'Specularity', 'Artefact' , 'Bubbles', 'Saturation']
unique_entries = set(categoryList)

for ll in range (0, len(fileList)):
    print(ll)
    
    image_path = os.path.join(dataset_dir, fileList[ll])
    image = skimage.io.imread(image_path)
    height, width = image.shape[:2]
    
    # get unique classes
    indices = { value : [ i for i, v in enumerate(classCategory) if v == value ] for value in unique_entries }
    
    mask = np.zeros([height, width, len(categoryList)], dtype=np.uint8)
    
    cnt = 0
    cnt_p=0
    cnt_r = 0
    
    for i in range (0, len(shapeFormat[ll])):
        if shapeFormat[ll][i]== 'polyline':
            if debugLevel:
                print('we are dealing with polyline')
            rr, cc = skimage.draw.polygon(segy[ll][cnt_p], segx[ll][cnt_p])
            rr = np.clip(rr, 0, height-1)
            cc = np.clip(cc, 0, width-1) 
            cnt_p = cnt_p + 1
    
        elif shapeFormat[ll][i]== 'polygon':
            if debugLevel:
                print('we are dealing polygon')
            
            rr, cc = skimage.draw.polygon(segy[ll][cnt_p], segx[ll][cnt_p])
            rr = np.clip(rr, 0, height-1)
            cc = np.clip(cc, 0, width-1)              
            cnt_p = cnt_p + 1

        elif shapeFormat[ll][i]== 'circle':
            if debugLevel:
                print('we are dealing with circle')
            rr, cc = skimage.draw.circle(circ[ll][cnt][1], circ[ll][cnt][0], circ[ll][cnt][2])
            rr = np.clip(rr, 0, height-1)
            cc = np.clip(cc, 0, width-1) 
            cnt = cnt +1
            
        elif shapeFormat[ll][i]== 'rect':
            if debugLevel:
                print('we are dealing with rectangle')
            rr, cc = rectangle(rect[ll][cnt_r][1], rect[ll][cnt_r][0], rect[ll][cnt_r][2],rect[ll][cnt_r][3] )
            rr = np.clip(rr, 0, height-1)
            cc = np.clip(cc, 0, width-1)
            cnt_r = cnt_r+1

        if (classCategory[ll][i]) == []:
            print('empty')
        else:
            mask[rr,cc, int(classCategory[ll][i][0])] = 255
    
    im_mask = mask.transpose([2,0,1])    

    saveImageFile=fileList[ll].split('.')[0]
    imsave(saveImageFile+'_mask.tif', im_mask)

    
