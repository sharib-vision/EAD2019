#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 18 11:22:09 2019

@author: shariba
"""


def get_args():
    import argparse
    parser = argparse.ArgumentParser(description="For EAD2019 challenge: semantic segmentation", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--detectionMetric", type=str, default="mAP-IOU_EAD2019_results/metrics_detection.json", help="json file for detection")
    parser.add_argument("--generalizationMetric", type=str, default="mAP-IOU_EAD2019_results/metrics_detection.json", help="json file for generalization")
    parser.add_argument("--semanticMetric", type=str, default="semantic_EAD2019_results/metrics_semantic.json", help="son file for segmentation")
    parser.add_argument("--caseType", type=int, default=2, help="please set 0: only for dection both balanced, 1: only for instance segmentation only, 2: for generalization")
    parser.add_argument("--Result_dir", type=str, default="finalEvaluationScores", help="all evaluation scores used for grading")
    args = parser.parse_args()
    
    return args


def read_json(jsonFile):
    import json
    with open(jsonFile) as json_data:
        data = json.load(json_data)
        return data
    
    

if __name__ == '__main__':
    import numpy as np
    import os
    
    valArgs = get_args()
    exists = os.path.isfile(valArgs.detectionMetric)
    
    if exists:
        data = read_json(valArgs.detectionMetric)
        valAppend = []
        for p in data["EADChallenge2019"].values():
            valAppend.append(p)
        scoreDetection = valAppend[2]['value']*0.01
        
        if valArgs.caseType == 0 or valArgs.caseType == 1:
            
            print('final score is computed only for detection, (task-I, EAD2019 challenge)')
            print('your score is:', valAppend[2]['value']*0.01)
            
            print('~~~~~~~~~~~~~~~Complimentary informations~~~~~~~~~~~~~~~')
            print('mean mAP:', valAppend[0]['value']*0.01)
            print('mean IOU:', valAppend[1]['value']*0.01)
            print('~~~~~~~~~~~~~~~~~~~~~~~~E.O.F~~~~~~~~~~~~~~~~~~~~~~~~~~')
            
            # create a json file
            
            print('All scores are saved in json files, see dir:', valArgs.Result_dir)
            
            
        elif valArgs.caseType == 1:
            print('final score computed for instance segmentation (task-II, EAD2019 challenge), please make sure that you have computed mAP before hand on the same data...')
            data = read_json(valArgs.semanticMetric)
            valAppend_Semantic=[]
            for i in range (len(data)):
                print(data[i])
                valAppend_Semantic.append(data[i])
                
            #compute average score only
            scoreSemantic = []
            for p in range(len(valAppend_Semantic)):
                scoreSemantic.append(valAppend_Semantic[0]['EADChallenge2019']['score']['value'])
                
            # compute scores
            finalScore = 0.75*np.mean(scoreSemantic) + 0.25*valAppend[0]['value']*0.01
            print ('overall score for instance segmentation for EAD2019 challenge is:', finalScore)
            
            
            print('~~~~~~~~~~~~~~~Complimentary informations~~~~~~~~~~~~~~~')
            print('number of semantic samples:', len(data))
            print('mean mAP alone:', valAppend[0]['value']*0.01)
            print('mean semantic score alone:', np.mean(scoreSemantic))
            print('~~~~~~~~~~~~~~~~~~~~~~E.O.F~~~~~~~~~~~~~~~~~~~~~~~~~~~')
            
        elif valArgs.caseType == 2:
            
            print('final score is computed only for generalization, (task-III, EAD2019 challenge)')
                 
            data = read_json(valArgs.generalizationMetric)
            valAppendGeneral = []
            for p in data["EADChallenge2019"].values():
                valAppendGeneral.append(p)
                
    
            print('your score is:', valAppendGeneral[2]['value']*0.01)
            print('~~~~~~~~~~~~~~~Complimentary informations~~~~~~~~~~~~~~~')
            print('mean mAP:', valAppendGeneral[0]['value']*0.01)
            print('mean IOU:', valAppendGeneral[1]['value']*0.01)
            print('~~~~~~~~~~~~~~~E.O.F~~~~~~~~~~~~~~~')
            
            print('computing generalization gap...')
            print('semantic gap:', (1- (valAppendGeneral[0]['value']*0.01-valAppend[0]['value']*0.01)))
            # read json file from your mAP score from task I - your current mAP score on this data 
    else:
        print('no multi-class artefact detection found, mAPs are required for scoring both segmentation and generalization tasks')
            
            
            
        
        