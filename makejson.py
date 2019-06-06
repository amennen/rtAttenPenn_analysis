# purpose: make json files for bids experiment

import os
import glob
from shutil import copyfile
import pandas as pd
import json
import numpy as np

bids_dir = '/data/jag/cnds/amennen/rtAttenPenn/fmridata/Nifti'

description_fn = os.path.join(bids_dir, 'dataset_description.json')
description = {u'Funding': [u'TODO'], 
			   u'Name': u'rtAttenPenn',
			   u'License': u'PDDL (http://opendatacommons.org/licenses/pddl/)',
			   u'HowToAcknowledge': u'TODO',
			   u'Authors': [u'TODO'],
			   u'ReferencesAndLinks': [u'TODO'],
			   u'DatasetDOI': u'TODO',
			   u'BIDSVersion': u'1.1.0',
			   u'Acknowledgements': u'We thank the administrative staff of the Princeton Neuroscience Institute and Penn Medicine.'}
with open(description_fn, 'w') as f:
	json.dump(description, f,indent=4)
        
# in root direcotry of dataset
task_fn = os.path.join(bids_dir, 'task-exfunc_rec-corrected_bold.json')
task = {'TaskName': 'exfunc', 
		'EchoTime': 0.028, 'RepetitionTime': 2, 
		'FlipAngle': 90, 
		'SliceTiming': [ 0.99,0,1.045,0.055,1.1,0.11,1.155,0.165,1.21,0.22,1.265,0.275,1.32,
                        0.33,1.375,0.385,1.43,0.44,1.485,0.495,1.54,0.55,1.595,0.605,1.65,0.66,1.705,
                        0.715, 1.76,0.77,1.815,0.825,1.87,0.88,1.925,0.935  ], 
		'MagneticFieldStrength': 3,
		'Instructions': 'No instructions.',
		'Task description': 'Siemens MoCo Series - Quick 10-TR scan to register previously-collected ROI to a new day of scanning.',
		'Institution Name': 'SC3T',
		'InstitutionAddress': 'Curie_Blvd._422_Philadelphia_PA_US_19104',
		'PhaseEncodingDirection': 'j-',
		'DeviceSerialNumber': '66044',
		'Manufacturer': 'Prisma',
		'EffectiveEchoSpacing': 0.000284998 }
with open(task_fn, 'w') as f:
	json.dump(task, f,indent=4)

task_fn = os.path.join(bids_dir, 'task-exfunc_rec-uncorrected_bold.json')
task = {'TaskName': 'exfunc', 
		'EchoTime': 0.028, 'RepetitionTime': 2, 
		'FlipAngle': 90, 
		'SliceTiming': [0.99,0,1.045,0.055,1.1,0.11,1.155,0.165,1.21,0.22,1.265,0.275,1.32,
			0.33,1.375,0.385,1.43,0.44,1.485,0.495,1.54,0.55,1.595,0.605,1.65,0.66,1.705,
			0.715, 1.76,0.77,1.815,0.825,1.87,0.88,1.925,0.935   ], 
		'MagneticFieldStrength': 3,
		'Instructions': 'No instructions.',
		'Task description': 'Quick 10-TR scan to register previously-collected ROI to a new day of scanning.',
		'Institution Name': 'SC3T',
		'InstitutionAddress': 'Curie_Blvd._422_Philadelphia_PA_US_19104',
		'PhaseEncodingDirection': 'j-',
		'DeviceSerialNumber': '66044',
		'Manufacturer': 'Prisma',
		'EffectiveEchoSpacing': 0.000284998}
with open(task_fn, 'w') as f:
	json.dump(task, f,indent=4)


task_fn = os.path.join(bids_dir, 'task-gonogo_rec-corrected_bold.json')
task = {'TaskName': 'gonogo', 
		'EchoTime': 0.028, 'RepetitionTime': 2, 
		'FlipAngle': 90, 
		'SliceTiming': [ 0.99,0,1.045,0.055,1.1,0.11,1.155,0.165,1.21,0.22,1.265,0.275,1.32,
                        0.33,1.375,0.385,1.43,0.44,1.485,0.495,1.54,0.55,1.595,0.605,1.65,0.66,1.705,
                        0.715, 1.76,0.77,1.815,0.825,1.87,0.88,1.925,0.935  ], 
		'MagneticFieldStrength': 3,
		'Instructions': 'What to press for the face or scene combination such as indoor places',
		'Task description': 'Siemens MoCo Series - Subjects see faces and scenes overlaid. The scenes are either indoor/outdoor and the faces are male or female. If they have to attend to scenes, they press when they see one cateogry and dont press when they see the other',
		'Institution Name': 'SC3T',
		'InstitutionAddress': 'Curie_Blvd._422_Philadelphia_PA_US_19104',
		'PhaseEncodingDirection': 'j-',
		'DeviceSerialNumber': '66044',
		'Manufacturer': 'Prisma',
		'EffectiveEchoSpacing': 0.000284998 }
with open(task_fn, 'w') as f:
	json.dump(task, f,indent=4)

task_fn = os.path.join(bids_dir, 'task-gonogo_rec-uncorrected_bold.json')
task = {'TaskName': 'gonogo', 
		'EchoTime': 0.028, 'RepetitionTime': 2, 
		'FlipAngle': 90, 
		'SliceTiming': [0.99,0,1.045,0.055,1.1,0.11,1.155,0.165,1.21,0.22,1.265,0.275,1.32,
			0.33,1.375,0.385,1.43,0.44,1.485,0.495,1.54,0.55,1.595,0.605,1.65,0.66,1.705,
			0.715, 1.76,0.77,1.815,0.825,1.87,0.88,1.925,0.935   ], 
		'MagneticFieldStrength': 3,
		'Instructions': 'What to press for the face or scene combination such as indoor places',
		'Task description': 'Subjects see faces and scenes overlaid. The scenes are either indoor/outdoor and the faces are male or female. If they have to attend to scenes, they press when they see one cateogry and dont press when they see the other',
		'Institution Name': 'SC3T',
		'InstitutionAddress': 'Curie_Blvd._422_Philadelphia_PA_US_19104',
		'PhaseEncodingDirection': 'j-',
		'DeviceSerialNumber': '66044',
		'Manufacturer': 'Prisma',
		'EffectiveEchoSpacing': 0.000284998}
with open(task_fn, 'w') as f:
	json.dump(task, f,indent=4)
        
task_fn = os.path.join(bids_dir, 'task-faces_rec-uncorrected_bold.json')
task = {'TaskName': 'faces', 
		'EchoTime': 0.028, 'RepetitionTime': 2, 
		'FlipAngle': 90, 
		'SliceTiming': [ 0 ], 
		'MagneticFieldStrength': 3,
		'Instructions': 'Match the top image with one of the bottom images',
		'Task description': 'Participants view a trio of images on the screen and are asked to select one of the two images on the bottom that is identical to the image on the top. From Clemens C.C. Bauer M.D., PhD.',
		'Institution Name': 'SC3T',
		'InstitutionAddress': 'Curie_Blvd._422_Philadelphia_PA_US_19104',
		'PhaseEncodingDirection': 'j-',
		'DeviceSerialNumber': '66044',
		'Manufacturer': 'Prisma',
		'EffectiveEchoSpacing': 0.000284998}
with open(task_fn, 'w') as f:
	json.dump(task, f,indent=4)
task_fn = os.path.join(bids_dir, 'task-faces_rec-corrected_bold.json')
task = {'TaskName': 'faces', 
		'EchoTime': 0.028, 'RepetitionTime': 2, 
		'FlipAngle': 90, 
		'SliceTiming': [0.99,0,1.045,0.055,1.1,0.11,1.155,0.165,1.21,0.22,1.265,0.275,1.32,
			0.33,1.375,0.385,1.43,0.44,1.485,0.495,1.54,0.55,1.595,0.605,1.65,0.66,1.705,
			0.715, 1.76,0.77,1.815,0.825,1.87,0.88,1.925,0.935   ], 
		'MagneticFieldStrength': 3,
		'Instructions': 'Match the top image with one of the bottom images',
		'Task description': 'Siemens MoCo Series - Participants view a trio of images on the screen and are asked to select one of the two images on the bottom that is identical to the image on the top. From Clemens C.C. Bauer M.D., PhD.',
		'Institution Name': 'SC3T',
		'InstitutionAddress': 'Curie_Blvd._422_Philadelphia_PA_US_19104',
		'PhaseEncodingDirection': 'j-',
		'DeviceSerialNumber': '66044',
		'Manufacturer': 'Prisma',
		'EffectiveEchoSpacing': 0.000284998}
with open(task_fn, 'w') as f:
	json.dump(task, f,indent=4)
# and then just make events tsv within that 


# now go through each subject's number and session fmap phasediff and add in the echo times
# then create empty tsv files
all_subjects = np.array([1,2])
nsub=len(all_subjects)
ndays=3
nifti_out="/data/jag/cnds/amennen/rtAttenPenn/fmridata/Nifti"
for subjectNum in all_subjects:
	bids_id = 'sub-{0:03d}'.format(subjectNum)
	for d in np.arange(ndays):
		subjectDay=d+1
		ses_id = 'ses-{0:02d}'.format(subjectDay)
		day_path=os.path.join(nifti_out,bids_id,ses_id)
		fmap_path = os.path.join(day_path,'fmap')
		fmap_fn = fmap_path + '/' + bids_id + '_' + ses_id + '_' + 'phasediff.json'
		with open(fmap_fn) as f:
			data=json.load(f)
		data['EchoTime1']=0.00412
		data['EchoTime2']=0.00658
		func_path = os.path.join(day_path,'func')
		all_func_scans = glob.glob(os.path.join(func_path, '*.nii.gz'))
		n_func = len(all_func_scans)
		longstring = []
		#print(all_func_scans)
		for i in np.arange(n_func):
			this_run = all_func_scans[i]
			str=os.path.split(this_run)[-1]
			str_parts = str.split('_')
			full_name = str_parts[1] + '_' + str_parts[2] + '_' + str_parts[3] +'_' + str_parts[4] + '_bold.nii.gz'
			#print(full_name)
			longstring.append(full_name)
		print(longstring)
		data['IntendedFor'] = longstring
		os.remove(fmap_fn)
		with open(fmap_fn, 'w') as f:
			json.dump(data, f,indent=4)
		
		mag_fn = fmap_path + '/' + bids_id + '_' + ses_id + '_' + 'magnitude1.json'	
		with open(fmap_fn) as f:
                        data=json.load(f)
		data['IntendedFor'] = longstring
		os.remove(mag_fn)
		with open(mag_fn, 'w') as f:
			json.dump(data,f,indent=4)
		# make empty .tsv files for all of the functional scans (for now)
		# read in all functional data and for each file make .tsv file
		for f in np.arange(n_func):
			this_run = all_func_scans[f]
			str = os.path.split(this_run)[-1]
			str_parts = str.split('_')
			# want to keep some parts of the name
			tsvname = str_parts[0] + '_' + str_parts[1] + '_' + str_parts[2] + '_' + str_parts[3] +'_' + str_parts[4] + '_events.tsv'
			full_path = os.path.join(func_path,tsvname)
			df=pd.DataFrame(columns=['onset', 'duration', 'trial_type', 'response_time', 'stim_file'])
			df.to_csv(full_path,sep='\t',index=False)
			#with open(full_path, "w") as my_empty_csv:
			#	pass  # or write something to it already
   			
			# we're also going to want to read in that functional corrected json file and change the slice timing
			if str_parts[3] == 'rec-corrected':
				thisjson = str_parts[0] + '_' + str_parts[1] + '_' + str_parts[2] + '_' + str_parts[3] +'_' + str_parts[4] + '_bold.json'
				#print(thisjson)
				json_fn = os.path.join(func_path,thisjson)
				with open(json_fn) as f:
					data=json.load(f)
				# now get slice timing we want
				json_fn_uncor = os.path.join(func_path,str_parts[0] + '_' + str_parts[1] + '_' + str_parts[2] + '_rec-uncorrected_' + str_parts[4] + '_bold.json')
				with open(json_fn_uncor) as f2:
					data_uncor=json.load(f2)
				st = data_uncor['SliceTiming']
				data['SliceTiming'] = st
				os.remove(json_fn)
				with open(json_fn, 'w') as f:
					json.dump(data,f,indent=4)
				#print(json_fn)
				#print(json_fn_uncor)
				#print(st)
				# data['SliceTiming'] = [slicetiming] 
