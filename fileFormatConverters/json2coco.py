#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 13 13:41:17 2018

@author:  ead2019
"""

def read_json_file(jsonFile):
    import json
    import objectpath
    category = []
    bbox = []
    with open(jsonFile) as json_data:
        data = json.load(json_data)
        for p in data["layers"]:
            if len(p['items'])!=0:
                category.append(p['name'])
                jsonnn_tree = objectpath.Tree(p['items'])
                result_tuple_from = tuple(jsonnn_tree.execute('$..from'))
                result_tuple_to = tuple(jsonnn_tree.execute('$..to'))
                #  convert to string from dict/ check how many corners are present
                xbottom=json.dumps(result_tuple_from)
                bottom = re.findall("\d+\.\d+", xbottom)
                if len(bottom)>2:
                    for k in range ((int)(len(bottom)/2)-1):
                        category.append(p['name'])
                bbox.append(result_tuple_from)
                bbox.append(result_tuple_to)

    return category, bbox


if __name__=="__main__":

    import json
    import re
    import os
    from collections import Counter

    artefactsList=[]
    category,  bbox = read_json_file('AIDA_annotation-2.json')
    uvalue=Counter(category).values()
    uval=list(uvalue)
    print('length of unique lists',len(uval))
    print ('classes in category', (int)(len(category)/2))
    count = 0
    cnt=0
    for k in range (len(uval)):
        # top
        for l in range (uval[k]):
#            print(l)
            artefactsList.append(category[count])
            
#            print(bbox[cnt][l])
#            print(bbox[cnt+1][l])
            
            x_top = bbox[cnt][l]
            xtop=json.dumps(x_top)
            top = re.findall("\d+\.\d+", xtop)
            artefactsList.append(top)
            # bottom
            x_bottom = bbox[cnt+1][l]
            xbottom=json.dumps(x_bottom)
            bottom = re.findall("\d+\.\d+", xbottom)
            artefactsList.append(bottom)
            count=count+1
       
     
        cnt = cnt+2   
           
    print(artefactsList)
    
    """
    write bounding-box in text files TODO print bboxes on sample test image
    
    file = 'image_no.txt'
    textfile = open(file, 'a')
    textfile.write(artefactsList[0],' ',artefactsList[1], ' ', artefactsList[2])
    textfile.write('\n')
    textfile.write()
    # np.savetxt("foo.csv", a, delimiter=",")
    textfile.close()
    
    """
    file = 'image_no.txt'
    try:
        os.remove(file)
    except OSError:
        pass
    
    textfile = open(file, 'a')
    cnt = 0
    for i in range (len(category)):
        print(artefactsList[cnt])
        print(artefactsList[cnt+1])
        print(artefactsList[cnt+2])
        
        textfile.write(artefactsList[cnt]+ ' '+ str(float(artefactsList[cnt+1][0]))+ ' '+str(float(artefactsList[cnt+1][1]))+' '+ str(float(artefactsList[cnt+2][0]))+ ' '+ str(float(artefactsList[cnt+2][1])))
        textfile.write('\n')
        cnt = cnt+3
    
    textfile.close()
    
    
    # [0][1][2]: class, top, bottom
    # write to the txt file
    # print(classes[1])

    # parser = argparse.ArgumentParser()
    # parser.add_argument('-jsonFile', action='store', help='filepath/filename', type=str)
    # parser.add_argument('-cocoFormatFile', action='store', help='foldername here')
    # args = parser.parse_args()
