#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 17 17:46:11 2019

@author: shariba
"""
import numpy as np

def get_args():
    
    import argparse
    parser = argparse.ArgumentParser(description="For EAD2019 challenge: semantic segmentation", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--GT_maskImage", type=str, default="../masks/0000600_mask.tif", help="ground truth mask image (5 channel tif image only)")
    parser.add_argument("--originalImage", type=str, default="../imgs/0000600.jpg", help="original Image")
    parser.add_argument("--Result_dir", type=str, default="../imgs/", help="predicted mask image (color overlay image)")
    args = parser.parse_args()
    
    return args


if __name__ == '__main__':
    
    import tifffile as tiff
    import cv2
    import os
    from matplotlib import pyplot as plt 
    classTypes =  ['Instrument', 'Specularity', 'Artefact' , 'Bubbles', 'Saturation'] 
    
    args=get_args()
    
    y_true_Array = tiff.imread(args.GT_maskImage)
    img = np.zeros([512, 512, 3], dtype=np.uint8)
    img_original = cv2.imread(args.originalImage, 1)
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 0, 255), (0, 255, 255)]
    
    for i in range(len(classTypes)):
        y_true = (((y_true_Array[i, :, :])> 0).astype(np.uint8))
        img1, contours, hierarchy = cv2.findContours(y_true, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if contours !=[]:
            midVal = int(contours[0].shape[0]/2)
            cv2.drawContours(img_original, contours, -1, colors[i], 3)
            cv2.putText(img_original,classTypes[i],(contours[0][midVal][0][0],  contours[0][midVal][0][1]),  cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255),2,cv2.LINE_AA)
       
    plt.imshow(img_original[:,:,[2,1,0]])
    cv2.imwrite(os.path.join(args.Result_dir, 'mask_overlayimage.jpg'), img_original)