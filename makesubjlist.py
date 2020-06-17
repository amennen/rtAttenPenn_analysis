# get subject info

# values: 
# subjectnumber
# sex
# age
# group


import os
from os.path import exists, join
from os import makedirs
from glob import glob
from shutil import copyfile
import pandas as pd
import nibabel as nib
import json
import pydicom
import pandas as pd
import numpy as np
import glob

bids_dir = '/data/jux/cnds/amennen/rtAttenPenn/fmridata/Nifti'
file_name='participants.tsv'
columns=['participant_id', 'age', 'sex', 'group']
data=[]
# script should just loop over all subjects possible
allsubjects = np.array([1,2,3,4,5,6,7,8,9,10,11,12,101,102, 103, 104,105, 106,107,108,109,110,111,112,113,114,115])
nsub = len(allsubjects)

for s in np.arange(nsub):
	subjectNum=allsubjects[s]
	bids_id = 'sub-{0:03d}'.format(subjectNum)
	dicom_out="/data/jux/cnds/amennen/rtAttenPenn/fmridata/Dicom"
	bids_id = 'sub-{0:03d}'.format(subjectNum)
	ses_id = 'ses-{0:02d}'.format(1)
	day_path=os.path.join(dicom_out,bids_id,ses_id)
	if subjectNum<=100:
		group = 'HC'
	else:
		group = 'MDD'
	

	# go to an example file name for that person
	# changed this on 10/3 because syncing the dicoms over from jag must have failed so now it's just reading any dicoms
	dicomfile= day_path + '/func' + '/task-faces_rec-uncorrected_run-01_bold' + '/001_*.dcm'
	print(dicomfile)
	fn = glob.glob(dicomfile)[0]
	d = pydicom.read_file(fn)
	subjectAge = int(d.PatientAge[0:-1])
	subjectSex = d.PatientSex
	data.append((bids_id,subjectAge,subjectSex,group))

df = pd.DataFrame(data=data,columns=columns)
df.to_csv(join(bids_dir, 'participants.tsv'), sep='\t', index=False)

#df = df.append({'paticipant_id':bids_id,'age':subjectAge,'sex':subjectSex,'group':group})
