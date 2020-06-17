# PURPOSE: run AFNI noise regression
# first delete first 10 TRs and then resave
import os
import glob
from shutil import copyfile
import pandas as pd
import json
import numpy as np
from subprocess import call
import sys
fmriprep_out="/data/jux/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/fmriprep"
trunc_save_dir = '/data/jux/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/afni/first_level/neurofeedback/trunc'
noise_save_dir = '/data/jux/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/afni/first_level/neurofeedback/clean'
confounds_dir = '/data/jux/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/fsl/first_level/confound_EVs'
whole_brain_mask = '/data/jux/cnds/amennen/rtAttenPenn/MNI_things/mni_icbm152_t1_tal_nlin_asym_09c_BOLD_mask_Penn.nii'

# subjects 106,3,107,4,108 got resting state
#subjectNum = 106
subjectNum = np.int(sys.argv[1])
bids_id = 'sub-{0:03d}'.format(subjectNum)
print(bids_id)
sessions = [1,2,3]
nToDelete=10
for s in sessions:
	subjectDay = s
	ses_id = 'ses-{0:02d}'.format(subjectDay)
	print(ses_id)
	# now get the number of neurofeedback runs by looking in the confounds folder
	confounds_path = confounds_dir + '/' + bids_id + '/' + ses_id
	fmriprep_path = fmriprep_out + '/' + bids_id + '/' + ses_id + '/' +'func'
	if subjectNum==110 and subjectDay==1:
		# change the day path manually
		fmriprep_path = os.path.join(fmriprep_out,bids_id,'ses-10') + '/' + 'func'
	# now get all the nf runs
	all_NF_runs = glob.glob(os.path.join(confounds_path, '*task-gonogo_rec-uncorrected*.1D'))
	n_runs = len(all_NF_runs)

	for r in np.arange(n_runs):
		run_id = 'run-{0:02d}'.format(r+1)
		confound_fn = glob.glob(os.path.join(confounds_path, '*gonogo_rec-uncorrected_'+run_id+'*.1D'))[0]
		fmriprep_fn = glob.glob(os.path.join(fmriprep_path,'*task-gonogo_rec-uncorrected_' + run_id +'_bold_space-MNI*preproc*'))[0]

		NAMETOSAVE = os.path.split(fmriprep_fn)[-1]
		dest_path = trunc_save_dir + '/' + bids_id + '/' + ses_id
		if not os.path.exists(dest_path):
			os.makedirs(dest_path)
		full_save_path = os.path.join(dest_path, NAMETOSAVE)
		# now run fslroi command to remove first 4 TRs
		#print('fslroi %s %s %i' % (rest_nifti,full_save_path,nToDelete))
		command = 'fslroi %s %s %i %i' % (fmriprep_fn,full_save_path,nToDelete,232)
		print(command)
		call(command,shell=True)

		# specify where to save cleaned version
		clean_path = noise_save_dir + '/' + bids_id + '/' + ses_id
		if not os.path.exists(clean_path):
			os.makedirs(clean_path)

		command = ("3dTproject -blur 5 -stopband 0 0.005 "
				"-input {0} ".format(full_save_path) +
				"-ort {0} -mask {1} ".format(confound_fn,whole_brain_mask) +
				"-prefix {0}/{1}_{2}_task-gonogo_{3}_glm.nii.gz".format(clean_path,bids_id,ses_id,run_id))
		print(command)
		call(command,shell=True)
