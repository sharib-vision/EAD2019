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
#    parser.add_argument("--semantic_detection", type=str, default="mAP-IOU_EAD2019_results/metrics_detection.json", help="son file for segmentation")
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
    mAP_d = 0
    mAP_s = 0
    IOU_d = 0
    overlap = 0
    semScore = 0
    mAP_g = 0
    score_d = 0
    F2_score=0
    score_g = 0
    debug = 0
    """ case: Detection """
    if valArgs.caseType == 0 or valArgs.caseType == 3 or valArgs.caseType == 2 or valArgs.caseType == 4 or valArgs.caseType == 5:
        exists = os.path.isfile(valArgs.detectionMetric)
        if exists:
            data = read_json(valArgs.detectionMetric)
            valAppend = []
            for p in data["EADChallenge2019"].values():
                valAppend.append(p)
            scoreDetection = valAppend[2]['value']*0.01
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
            ratioPass = int(valAppend[10]['value'])
        
    """ case: Semantic """
    if valArgs.caseType == 1 or valArgs.caseType == 3 or valArgs.caseType == 5:
        exists = os.path.isfile(valArgs.semanticMetric)
        if exists:
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
                print('mean semantic score alone:', scoreSemantic)
                print('~~~~~~~~~~~~~~~~~~~~~~E.O.F~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        
            F2_score = valAppend_Semantic[2]['value']
            overlap = scoreSemantic
            semScore = finalScore
            ratioPass = 0
                
            """ case: Generalization """
    if  valArgs.caseType == 3 or valArgs.caseType == 4:
        exists = os.path.isfile(valArgs.generalizationMetric)
        if exists:
            data = read_json(valArgs.generalizationMetric)
            valGen = []
            for p in data["EADChallenge2019"].values():
                valGen.append(p)
                
            if debug:
                print('~~~~~~~~~~~~~~~Complimentary informations~~~~~~~~~~~~~~~')
                print('mean mAP:', valGen[0]['value']*0.01)
                print('mean score_g:', valGen[1]['value']*0.01)
                print('~~~~~~~~~~~~~~~E.O.F~~~~~~~~~~~~~~~')
  
            mAP_g = valGen[0]['value']
            score_g = valGen[1]['value']
#    
#    else:
#        print('no multi-class artefact detection found, mAPs are required for scoring both segmentation and generalization tasks')
#        
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
                  "value": (mAP_g)
                },
                "dev_g":{
                  "value": (score_g)
                },
                "ratioPass":{
                    "value": (ratioPass),
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
    
            
            
        
        
