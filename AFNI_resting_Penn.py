# PURPOSE: run AFNI noise regression

import os
import glob
from shutil import copyfile
import pandas as pd
import json
import numpy as np
from subprocess import call
import sys
fmriprep_out="/data/jag/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/fmriprep"
reg_save_dir='/data/jag/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/resting/confound_EVs'
trunc_save_dir = '/data/jag/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/resting/trunc'
noise_save_dir = '/data/jag/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/resting/clean'
# subjects 106,3,107,4,108 got resting state
#subjectNum = 106
subjectNum = np.int(sys.argv[1])
bids_id = 'sub-{0:03d}'.format(subjectNum)
print(bids_id)
sessions = [1,3]
for s in sessions:
	subjectDay = s
	ses_id = 'ses-{0:02d}'.format(subjectDay)
	print(ses_id)
	# get regression file 
	confounds_path = reg_save_dir + '/' + bids_id + '/' + ses_id
	confound_fn = glob.glob(os.path.join(confounds_path, '*.1D'))
	confound_fn = confound_fn[0]

	# get nifti file
	nifti_path = trunc_save_dir + '/' + bids_id + '/' + ses_id
	nifti_fn = glob.glob(os.path.join(nifti_path, '*.nii.gz'))
	nifti_fn = nifti_fn[0]

	# specify where to save cleaned version
	clean_path = noise_save_dir + '/' + bids_id + '/' + ses_id
	if not os.path.exists(clean_path):
		os.makedirs(clean_path)

	command = ("3dTproject -polort 2 -blur 6 -passband 0.01 0.08 "
					"-input {0} ".format(nifti_fn) +
					"-ort {0} ".format(confound_fn) +
					"-prefix {0}/{1}_{2}_task_rest_glm.nii.gz".format(clean_path,bids_id,ses_id))

	call(command,shell=True)



	
