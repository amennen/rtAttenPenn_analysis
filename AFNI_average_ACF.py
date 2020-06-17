# purpose: average all acf params -- make 1 for ses 1, 1 for ses 3 and then 1 that averages all of them


import os
import glob
from shutil import copyfile
import pandas as pd
import json
import numpy as np
from subprocess import call
import sys
import scipy.stats
import nibabel as nib
import nilearn

## Frame wise displacement isn't here
fmriprep_out="/data/jux/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/fmriprep"
task_path = '/data/jux/cnds/amennen/rtAttenPenn/fmridata/behavdata/faces'
run_path = '/data/jux/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/afni/first_level/normalized_runs'
cf_dir = '/data/jux/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/fsl/first_level/confound_EVs'
timing_path = '/data/jux/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/afni/first_level/timing_files'
analyses_out = '/data/jux/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/afni/first_level/stats'
whole_brain_mask = '/data/jux/cnds/amennen/rtAttenPenn/MNI_things/mni_icbm152_t1_tal_nlin_asym_09c_BOLD_mask_Penn.nii'
second_level = '/data/jux/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/afni/group_level/'

allsubjects = [1,2,3,4,5 ,6,7,8,9,10,11,101,102,103,104,105,106 ,107 ,108 ,109,110,111,112]
nSub = len(allsubjects)
nParams = 4
ses_1_ACF_params = np.zeros((nSub,nParams))
ses_3_ACF_params = np.zeros((nSub,nParams))
for sub in np.arange(nSub):
    subjectNum = allsubjects[sub]
    bids_id = 'sub-{0:03d}'.format(subjectNum)
    # concatenate confound EVS
    print(bids_id)
    sessions = [1,3]
    nRuns = 2
    for s in sessions:
        subjectDay = s
        ses_id = 'ses-{0:02d}'.format(subjectDay)
        print(ses_id)
        output_path = "{0}/{1}/{2}".format(analyses_out,bids_id,ses_id)
        this_file = output_path + '/' + 'params.txt'
        data = pd.read_fwf(this_file)
        if s == 1:
            for p in np.arange(nParams):
                ses_1_ACF_params[sub,p] = float(data.columns[p])
        elif s == 3:
            for p in np.arange(nParams):
                ses_3_ACF_params[sub,p] = float(data.columns[p])


# now average everything
average_ses_1 = np.mean(ses_1_ACF_params,axis=0)
average_ses_3 = np.mean(ses_3_ACF_params,axis=0)

concat_averages = np.concatenate((average_ses_1[:,np.newaxis],average_ses_3[:,np.newaxis]),axis=1).T
total_average = np.mean(concat_averages,axis=0)

ses_1_filename = '{0}/ses-{1:02d}/ses-{1:02d}_ACF_params.npy'.format(second_level,1)
np.save(ses_1_filename,average_ses_1)
ses_3_filename = '{0}/ses-{1:02d}/ses-{1:02d}_ACF_params.npy'.format(second_level,3)
np.save(ses_3_filename,average_ses_3)
all_average_filename = '{0}/ses-{1:02d}_minus_ses-{2:02d}/ses-{1:02d}_minus_ses-{2:02d}_ACF_params.npy'.format(second_level,3,1)
np.save(all_average_filename,total_average)