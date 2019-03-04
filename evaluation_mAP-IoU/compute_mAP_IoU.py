# =============================================================================
#   Evaluates mAP and IoU 
#
#   Requires bounding boxes to be given in the VOC format i.e:
#       ground-truth boxes: class_name, x1, y1, x2, y2
#       predicted boxes: class_name, confidence, x1, y1, x2, y2 
# EAD 2019 Challenge (https://ead2019.grand-challenge.org)
# If you encounter any error please contact us. Thank you for your participation.
# Contact: sharib[dot]ali[at]eng[dot]ox[dot]ac.uk or felix.zhou[at]ludwig.ox.ac.uk
# =============================================================================

import glob
import json
import os
import shutil
import operator
import sys
import numpy as np 

MINOVERLAP = 0.25 # default value 

debug = 0
# fetch the folders 
if debug:
    predictfolder ='../mAP-IoU_testdata/predicted'
    gtfolder ='../mAP-IoU_testdata/ground-truth'
    resultsfolder ='../mAP-IoU_testdata/results'
else:    
    predictfolder = sys.argv[1]
    gtfolder = sys.argv[2]
    resultsfolder = sys.argv[3]
    jsonFileName = sys.argv[4]

"""
Series of helper functions. 
"""

"""
 throw error and exit
"""
def error(msg):
  print(msg)
  sys.exit(0)

"""
 function to check if the number is a float between 0.0 and 1.0
"""
def is_float_between_0_and_1(value):
  try:
    val = float(value)
    if val > 0.0 and val < 1.0:
      return True
    else:
      return False
  except ValueError:
    return False

"""
 Calculate the AP given the recall and precision array
  1st) We compute a version of the measured precision/recall curve with
       precision monotonically decreasing
  2nd) We compute the AP as the area under this curve by numerical integration.
"""
def voc_ap(rec, prec):
  """
  --- Official matlab code VOC2012---
  mrec=[0 ; rec ; 1];
  mpre=[0 ; prec ; 0];
  for i=numel(mpre)-1:-1:1
      mpre(i)=max(mpre(i),mpre(i+1));
  end
  i=find(mrec(2:end)~=mrec(1:end-1))+1;
  ap=sum((mrec(i)-mrec(i-1)).*mpre(i));
  """
  rec.insert(0, 0.0) # insert 0.0 at begining of list
  rec.append(1.0) # insert 1.0 at end of list
  mrec = rec[:]
  prec.insert(0, 0.0) # insert 0.0 at begining of list
  prec.append(0.0) # insert 0.0 at end of list
  mpre = prec[:]
  """
   This part makes the precision monotonically decreasing
    (goes from the end to the beginning)
  """
  # matlab indexes start in 1 but python in 0, so I have to do:
  #   range(start=(len(mpre) - 2), end=0, step=-1)
  # also the python function range excludes the end, resulting in:
  #   range(start=(len(mpre) - 2), end=-1, step=-1)
  for i in range(len(mpre)-2, -1, -1):
    mpre[i] = max(mpre[i], mpre[i+1])
  """
   This part creates a list of indexes where the recall changes
  """
  # matlab: i=find(mrec(2:end)~=mrec(1:end-1))+1;
  i_list = []
  for i in range(1, len(mrec)):
    if mrec[i] != mrec[i-1]:
      i_list.append(i) # if it was matlab would be i + 1
  """
   The Average Precision (AP) is the area under the curve
    (numerical integration)
  """
  # matlab: ap=sum((mrec(i)-mrec(i-1)).*mpre(i));
  ap = 0.0
  for i in i_list:
    ap += ((mrec[i]-mrec[i-1])*mpre[i])
  return ap, mrec, mpre


"""
 Convert the lines of a file to a list
"""
def file_lines_to_list(path):
  # open txt file lines to a list
  with open(path) as f:
    content = f.readlines()
  # remove whitespace characters like `\n` at the end of each line
  content = [x.strip() for x in content]
  return content


"""
 Create a "tmp_files/" and "results/" directory
"""
tmp_files_path = "tmp_files"
if not os.path.exists(tmp_files_path): # if it doesn't exist already
  os.makedirs(tmp_files_path, exist_ok=True)
  
#if resultsfolder is not None:
results_files_path = resultsfolder
#else:
#    results_files_path = "results"
# if os.path.exists(results_files_path): # if it exist already
#   # reset the results directory
#   shutil.rmtree(results_files_path)
os.makedirs(results_files_path, exist_ok=True)


"""
 Ground-Truth
   Load each of the ground-truth files into a temporary ".json" file.
   Create a list of all the class names present in the ground-truth (gt_classes).
"""
# get a list with the ground-truth files
ground_truth_files_list = glob.glob(os.path.join(gtfolder,'*.txt'))

if len(ground_truth_files_list) == 0:
    error("Error: No ground-truth files found!")
ground_truth_files_list.sort()
# dictionary with counter per class
gt_counter_per_class = {}

for txt_file in ground_truth_files_list:
  #print(txt_file)
  file_id = txt_file.split(".txt",1)[0]
  file_id = os.path.basename(os.path.normpath(file_id))
  # check if there is a correspondent predicted objects file
  if not os.path.exists(os.path.join(predictfolder , file_id + ".txt")):
    error_msg = "Error. File not found: predicted/" +  file_id + ".txt\n"
#    error_msg += "(You can avoid this error message by running extra/intersect-gt-and-pred.py)"
    error(error_msg)
  lines_list = file_lines_to_list(txt_file)
  # create ground-truth dictionary
  bounding_boxes = []
  for line in lines_list:
    try:
      class_name, left, top, right, bottom = line.split()
    except ValueError:
      error_msg = "Error: File " + txt_file + " in the wrong format.\n"
      error_msg += " Expected: <class_name> <left> <top> <right> <bottom>\n"
      error_msg += " Received: " + line
      error_msg += "\n\nIf you have a <class_name> with spaces between words you should remove them\n"
      error_msg += "by running the script \"rename_class.py\" in the \"extra/\" folder."
      error(error_msg)
    # check if class is in the ignore list, if yes skip

    bbox = left + " " + top + " " + right + " " +bottom
    bounding_boxes.append({"class_name":class_name, "bbox":bbox, "used":False})
    # count that object
    if class_name in gt_counter_per_class:
      gt_counter_per_class[class_name] += 1
    else:
      # if class didn't exist yet
      gt_counter_per_class[class_name] = 1
  # dump bounding_boxes into a ".json" file
  with open(os.path.join(tmp_files_path, file_id + "_ground_truth.json"), 'w') as outfile:
    json.dump(bounding_boxes, outfile)

gt_classes = list(gt_counter_per_class.keys())
# let's sort the classes alphabetically
gt_classes = sorted(gt_classes)
n_classes = len(gt_classes)


"""
 Predicted
   Load each of the predicted files into a temporary ".json" file.
"""
# get a list with the predicted files
predicted_files_list = glob.glob(os.path.join(predictfolder, '*.txt'))
predicted_files_list.sort()

for class_index, class_name in enumerate(gt_classes):
  bounding_boxes = []
  for txt_file in predicted_files_list:
    #print(txt_file)
    # the first time it checks if all the corresponding ground-truth files exist
    file_id = txt_file.split(".txt",1)[0]
    file_id = os.path.basename(os.path.normpath(file_id))
    if class_index == 0:
      if not os.path.exists(os.path.join(gtfolder, file_id + ".txt")):
        error_msg = "Error. File not found: ground-truth/" +  file_id + ".txt\n"
#        error_msg += "(You can avoid this error message by running extra/intersect-gt-and-pred.py)"
        error(error_msg)
    lines = file_lines_to_list(txt_file)
    for line in lines:
      try:
        tmp_class_name, confidence, left, top, right, bottom = line.split()
      except ValueError:
        error_msg = "Error: File " + txt_file + " in the wrong format.\n"
        error_msg += " Expected: <class_name> <confidence> <left> <top> <right> <bottom>\n"
        error_msg += " Received: " + line
        error(error_msg)
      if tmp_class_name == class_name:
        #print("match")
        bbox = left + " " + top + " " + right + " " +bottom
        bounding_boxes.append({"confidence":confidence, "file_id":file_id, "bbox":bbox})
        #print(bounding_boxes)
  # sort predictions by decreasing confidence
  bounding_boxes.sort(key=lambda x:x['confidence'], reverse=True)
  with open(os.path.join(tmp_files_path, class_name + "_predictions.json"), 'w') as outfile:
    json.dump(bounding_boxes, outfile)

"""
 Calculate the AP for each class
"""
sum_AP = 0.0
ap_dictionary = {}
sum_iou = 0.0
iou_dictionary = {}

# open file to store the results
with open(os.path.join(results_files_path, "results.txt"), 'w') as results_file:
  results_file.write("# AP and precision/recall per class\n")
  count_true_positives = {}
  for class_index, class_name in enumerate(gt_classes):
    count_true_positives[class_name] = 0
    """
     Load predictions of that class
    """
    predictions_file = os.path.join(tmp_files_path, class_name + "_predictions.json")
    predictions_data = json.load(open(predictions_file))

    """
     Assign predictions to ground truth objects
    """
    nd = len(predictions_data)
    tp = [0] * nd # creates an array of zeros of size nd
    fp = [0] * nd
    iou = [0] * nd
    for idx, prediction in enumerate(predictions_data):
      file_id = prediction["file_id"]
      
      # assign prediction to ground truth object if any
      #   open ground-truth with that file_id
      gt_file = os.path.join(tmp_files_path, file_id + "_ground_truth.json")
      ground_truth_data = json.load(open(gt_file))
      ovmax = -1
      gt_match = -1
      # load prediction bounding-box
      bb = [ float(x) for x in prediction["bbox"].split() ]
      for obj in ground_truth_data:
        # look for a class_name match
        if obj["class_name"] == class_name:
          bbgt = [ float(x) for x in obj["bbox"].split() ]
          bi = [max(bb[0],bbgt[0]), max(bb[1],bbgt[1]), min(bb[2],bbgt[2]), min(bb[3],bbgt[3])]
          iw = bi[2] - bi[0] + 1
          ih = bi[3] - bi[1] + 1
          if iw > 0 and ih > 0:
            # compute overlap (IoU) = area of intersection / area of union
            ua = (bb[2] - bb[0] + 1) * (bb[3] - bb[1] + 1) + (bbgt[2] - bbgt[0]
                    + 1) * (bbgt[3] - bbgt[1] + 1) - iw * ih
            ov = iw * ih / ua
            if ov > ovmax:
              ovmax = ov
              gt_match = obj

      # set minimum overlap
      min_overlap = MINOVERLAP
      
      if ovmax >= min_overlap:
        if not bool(gt_match["used"]):
          # true positive
          tp[idx] = 1
          iou[idx] = ovmax
          gt_match["used"] = True
          count_true_positives[class_name] += 1
          # update the ".json" file
          with open(gt_file, 'w') as f:
              f.write(json.dumps(ground_truth_data))
        else:
          # false positive (multiple detection)
          fp[idx] = 1
      else:
        # false positive
        fp[idx] = 1
        if ovmax > 0:
          status = "INSUFFICIENT OVERLAP"

    #print(tp)
    # compute precision/recall
    cumsum = 0
    for idx, val in enumerate(fp):
      fp[idx] += cumsum
      cumsum += val
    cumsum = 0
    for idx, val in enumerate(tp):
      tp[idx] += cumsum
      cumsum += val
    #print(tp)
    rec = tp[:]
    for idx, val in enumerate(tp):
      rec[idx] = float(tp[idx]) / gt_counter_per_class[class_name]
    prec = tp[:]
    for idx, val in enumerate(tp):
      prec[idx] = float(tp[idx]) / (fp[idx] + tp[idx])

    ap, mrec, mprec = voc_ap(rec, prec)
    sum_AP += ap
    text = "{0:.2f}%".format(ap*100) + " = " + class_name + " AP  " #class_name + " AP = {0:.2f}%".format(ap*100)
    """
     Write to results.txt
    """
    rounded_prec = [ '%.2f' % elem for elem in prec ]
    rounded_rec = [ '%.2f' % elem for elem in rec ]
    results_file.write(text + "\n Precision: " + str(rounded_prec) + "\n Recall   :" + str(rounded_rec) + "\n\n")
    
    
    ap_dictionary[class_name] = ap
    iou_dictionary[class_name] = np.mean(iou)
    sum_iou += np.mean(iou)
    
  results_file.write("\n# mAP of all classes\n")
  mAP = sum_AP / n_classes
  mIoU = sum_iou / n_classes
  text = "mAP_{0:.0f}".format(MINOVERLAP*100) +" = {0:.2f}%".format(mAP*100) 
  results_file.write(text + "\n")

  textiou = "mIoU_{0:.0f}".format(MINOVERLAP*100) +" = {0:.2f}%".format(mIoU*100)
  results_file.write(textiou + "\n")

# remove the tmp_files directory
#shutil.rmtree(tmp_files_path)

"""
 Count total of Predictions
"""
# iterate through all the files
pred_counter_per_class = {}
#all_classes_predicted_files = set([])
for txt_file in predicted_files_list:
  # get lines to list
  lines_list = file_lines_to_list(txt_file)
  for line in lines_list:
    class_name = line.split()[0]

    # count that object
    if class_name in pred_counter_per_class:
      pred_counter_per_class[class_name] += 1
    else:
      # if class didn't exist yet
      pred_counter_per_class[class_name] = 1
#print(pred_counter_per_class)
pred_classes = list(pred_counter_per_class.keys())


"""
 Write number of ground-truth objects per class to results.txt
"""
with open(os.path.join(results_files_path + "results.txt"), 'a') as results_file:
  results_file.write("\n# Number of ground-truth objects per class\n")
  for class_name in sorted(gt_counter_per_class):
    results_file.write(class_name + ": " + str(gt_counter_per_class[class_name]) + "\n")

"""
 Finish counting true positives
"""
for class_name in pred_classes:
  # if class exists in predictions but not in ground-truth then there are no true positives in that class
  if class_name not in gt_classes:
    count_true_positives[class_name] = 0

"""
 Write number of predicted objects per class to results.txt
"""
with open(os.path.join(results_files_path, "results.txt"), 'a') as results_file:
  results_file.write("\n# Number of predicted objects per class\n")
  for class_name in sorted(pred_classes):
    n_pred = pred_counter_per_class[class_name]
    text = class_name + ": " + str(n_pred)
    text += " (tp:" + str(count_true_positives[class_name]) + ""
    text += ", fp:" + str(n_pred - count_true_positives[class_name]) + ")\n"
    results_file.write(text)


print("Finished computing mAP and IoU. Results are saved in {}/results.txt".format(resultsfolder))


'''
creating json file
'''
import json
import os

# TODO: include class-wise map and IoU
# Note this is only for detection method of the challenge.
# Please comment this!!!! as this example did not have instrument detection we have to keep this value
ap_dictionary['instrument'] = 0
my_dictionary = {
    "EADChallenge2019":{
            "mAP":{
             "value":   (mAP*100) 
            },
            "IoU":{
              "value":       (mIoU*100)
            },
            "score":{
              "value":      (0.8*mAP*100+0.2*mIoU*100),  
            },
            "mAP_specularity": {
              "value": (ap_dictionary['specularity']*100)
            },
            "mAP_contrast": {
              "value": (ap_dictionary['contrast']*100)
            },
            "mAP_saturation": {
              "value": (ap_dictionary['saturation']*100)
            },
            "mAP_blur":{
              "value": (ap_dictionary['blur']*100)
            },
            "mAP_instrument":{
              "value": (ap_dictionary['instrument']*100)
            },
            "mAP_bubbles":{
              "value": (ap_dictionary['bubbles']*100)
            },
            "mAP_artifact":{
              "value": (ap_dictionary['artifact']*100)
            }
        }
}

jsonFileName=os.path.join(resultsfolder, jsonFileName)
    
try:
    os.remove(jsonFileName)
except OSError:
    pass

fileObj= open(jsonFileName, "w+")
json.dump(my_dictionary, fileObj)
fileObj.close()



