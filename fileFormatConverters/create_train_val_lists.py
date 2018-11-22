#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 13 13:41:17 2018

@author:  ead2019
"""

if __name__=="__main__":
    
    import numpy as np 
    import pandas as pd
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-csvFile_trainingSet', action='store', help='filepath/filename.names', type=str)
    parser.add_argument('-saveFolder', action='store', help='foldername here')
    args = parser.parse_args()
    
#    infile = 'train_endo_rescale.csv'
    infile = args.csvFile_trainingSet
    intable = pd.read_csv(infile, sep=',', header=None )
    
    ratio = 0.9
    select = np.arange(len(intable))
    
    np.random.shuffle(select)
    
    cutoff = int(ratio*len(select))
    train_idx = select[:cutoff]
    test_idx = select[cutoff:]
    
    
    traintable = intable.ix[train_idx,:]
    testtable = intable.ix[test_idx,:]
    
    """
    Save out 
    """

    traintable.to_csv(args.saveFolder+'/'+infile.split('.')[0]+'_train.csv', index=None, header=None, sep=',')
    testtable.to_csv(args.saveFolder+'/'+infile.split('.')[0]+'_test.csv', index=None, header=None, sep=',')
    
    
