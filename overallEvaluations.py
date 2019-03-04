#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 18 11:22:09 2019

@author: shariba

"""

import json
    
def get_args():
    import argparse
    parser = argparse.ArgumentParser(description="For EAD2019 challenge: semantic segmentation", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--detectionMetric", type=str, default="mAP-IOU_EAD2019_results/metrics_detection.json", help="json file for detection")
    parser.add_argument("--generalizationMetric", type=str, default="mAP-IOU_EAD2019_results/metrics_detection.json", help="json file for generalization")
    parser.add_argument("--semantic_detection", type=str, default="mAP-IOU_EAD2019_results/metrics_detection.json", help="son file for segmentation")
    parser.add_argument("--semanticMetric", type=str, default="evaluation_semantic/results/metrics_semantic.json", help="son file for segmentation")
    parser.add_argument("--caseType", type=int, default=3, help="please set 0: only for dection both balanced, 1: only for instance segmentation only, 2: for generalization, 3: for all tasks")
    parser.add_argument("--Result_dir", type=str, default="finalEvaluationScores", help="all evaluation scores used for grading")
    parser.add_argument("--jsonFileName", type=str, default="metrics.json", help="all evaluation scores used for grading")
    
    args = parser.parse_args()
    
    return args


def read_json(jsonFile):
    with open(jsonFile) as json_data:
        data = json.load(json_data)
        return data
    
if __name__ == '__main__':
    import os
    
    valArgs = get_args()
    exists = os.path.isfile(valArgs.detectionMetric)
    mAP_d = 0
    mAP_s = 0
    IOU_d = 0
    overlap = 0
    semScore = 0
    mAP_g = 0
    score_d = 0
    debug = 0
    
    if exists:
        data = read_json(valArgs.detectionMetric)
        valAppend = []
        for p in data["EADChallenge2019"].values():
            valAppend.append(p)
        scoreDetection = valAppend[2]['value']*0.01
        if valArgs.caseType == 0 or valArgs.caseType == 3 or valArgs.caseType == 2:
            if debug:
                print('final score is computed for detection, (task-I, EAD2019 challenge)')
                print('your score is:', valAppend[2]['value']*0.01)
                
                print('~~~~~~~~~~~~~~~Complimentary informations~~~~~~~~~~~~~~~')
                print('mean mAP:', valAppend[0]['value']*0.01)
                print('mean IOU:', valAppend[1]['value']*0.01)
                print('~~~~~~~~~~~~~~~~~~~~~~~~E.O.F~~~~~~~~~~~~~~~~~~~~~~~~~~')
                print('All scores are saved in json files, see dir:', valArgs.Result_dir)
            
            mAP_d = valAppend[0]['value']*0.01
            IOU_d = valAppend[1]['value']*0.01
            score_d = valAppend[2]['value']*0.01
                
        if valArgs.caseType == 1 or valArgs.caseType == 3:
#            Detection has been removed from final submission for semantic
            # first read the json file for detection
#            data = read_json(valArgs.semantic_detection)
#            valAppend = []
#            for p in data["EADChallenge2019"].values():
#                valAppend.append(p)
#            if debug:
#                print('final score computed for instance segmentation (task-II, EAD2019 challenge), please make sure that you have computed mAP before hand on the same data...')
            
            data = read_json(valArgs.semanticMetric)
            valAppend_Semantic=[]
            for p in data["EADChallenge2019"].values():
                valAppend_Semantic.append(p)
                
            # compute scores
            finalScore = 0.75*valAppend_Semantic[3]['value'] + 0.25*valAppend_Semantic[2]['value']
            scoreSemantic = valAppend_Semantic[3]['value']
            if debug:
                print ('overall score for instance segmentation for EAD2019 challenge is:', finalScore)
                print('~~~~~~~~~~~~~~~Complimentary informations~~~~~~~~~~~~~~~')
                print('number of semantic samples:', len(data))
                print('mean mAP alone:', valAppend[0]['value']*0.01)
                print('mean semantic score alone:', scoreSemantic)
                print('~~~~~~~~~~~~~~~~~~~~~~E.O.F~~~~~~~~~~~~~~~~~~~~~~~~~~~')
            
            F2_score = valAppend_Semantic[2]['value']
            overlap = scoreSemantic
            semScore = finalScore
            
        if valArgs.caseType == 2 or valArgs.caseType == 3 or valArgs.caseType == 4:
            data = read_json(valArgs.generalizationMetric)
            valAppendGeneral = []
            for p in data["EADChallenge2019"].values():
                valAppendGeneral.append(p)
            
            if debug:
                print('final score is computed only for generalization, (task-III, EAD2019 challenge)')
                print('your score is:', valAppendGeneral[2]['value']*0.01)
                print('~~~~~~~~~~~~~~~Complimentary informations~~~~~~~~~~~~~~~')
                print('mean mAP:', valAppendGeneral[0]['value']*0.01)
                print('mean IOU:', valAppendGeneral[1]['value']*0.01)
                print('~~~~~~~~~~~~~~~E.O.F~~~~~~~~~~~~~~~')
            
#            print('computing generalization gap...')
#            print('semantic gap:', (1- (valAppendGeneral[0]['value']*0.01-valAppend[0]['value']*0.01)))
            # read json file from your mAP score from task I - your current mAP score on this data 
    
            mAP_g = valAppendGeneral[0]['value']*0.01
    
    else:
        print('no multi-class artefact detection found, mAPs are required for scoring both segmentation and generalization tasks')
        
    '''
    creating json file
    '''
    # TODO: Loop this for 
    my_dictionary = {
        "EADChallenge2019":{
                "mAP_d":{
                 "value":  (mAP_d) 
                },
                "IOU_d":{
                  "value": (IOU_d)
                },
                "score_d":{
                  "value": (score_d)
                },
                "F2-score":{
                 "value":   (F2_score) 
                },
                "overlap":{
                 "value":   (overlap) 
                },
                "semantic":{
                  "value": (semScore)
                },
                "mAP_g":{
                  "value": (mAP_g),  
                }
                
            }
    }   
                
    # append json file             
    os.makedirs(valArgs.Result_dir, exist_ok=True)
    jsonFileName=os.path.join(valArgs.Result_dir, valArgs.jsonFileName)
    
    fileObj= open(jsonFileName, "a")
    fileObj.write("\n")
    json.dump(my_dictionary, fileObj)
    fileObj.close()
    
            
            
        
        
