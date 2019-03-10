## EAD2019 Leaderboard 
@ead2019 team

### Submission Styles

- ead2019_testSubmission.zip

		- detection_bbox
		- generalization_bbox
		- semantic_masks

  
- detection bbox/generalization bbox  - VOC format in  **.txt**
  
  	`` <class_name> <confidence> <x1> <y1> <x2> <y2> ``
  		
  	example1: specularity	0.92 268 414 292 438
  	example2: artifact	0.98 219 182 243 207
  		
  	Tips:
  		
  	- If you have a YOLO format (.txt) please convert to VOC format
  		- check our "scripts/run_yolo2voc.py"
  
- semantic masks
  	- **.tif** file with 5 channels
  		
	``<channel 1: Instrument> <channel 2: Specularity> <channel 3 Artefact> <channel 4: Bubbles> <channel 5: Saturation>``
  		
  	- <span style="color:red"> semantic bbox detection criteria has been removed. Now, the participants will be scored only on their semantic segmentation </span>

#### Allowed Submissions

- **Case 1:** only semantic is allowed
- **Case 2:** Only detection is allowed
- **Case 3:** All detection, generalization and semantic allowed
- **Case 4:** Detection and semantic allowed *Note: there is no detection for semantic now!*
- **Case 5:** Generalization only allowed with detection 
	 *Note: Generalization alone is not accepted as we need to compute the score deviation)*

### Evaluation Scoring

1. **Endoscopic Artefact Detection**
	- Final score: 0.6 * mAP + 0.4 * IOU
2. **Generalization of Artefact Detection**
	- Deviation score per class above or below tolerance (+/-5%) will be reported
	
	**Highest mAP with lowest deviation score will be declared winner of this sub-challenge***

	*For example: Lets say tolerance is 10%, then if your algorithm in detection gives an mAP/class of 30% then your generalization should be with in the tolerance range, i.e., 27%<=mAP/class<=33%, in this scenario your deviation will be zero. However, anything below or above will be penalized. Lets say if your algorithm scores 25% on generalization data then your deviation will be 2% which will be reported.*
	
3. **Semantic Segmentation**
	- Final score: 0.75 * overlap + 0.25 * F2-score (Type-II error)
	

  		
  	
