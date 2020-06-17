# purpose: calculate ACF parameters for each subject to then use clustering on
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

allsubjects = [1,2,3,4,5 ,6,7,8,9,10,11,101,102,103,104,105,106 ,107 ,108 ,109,110,111,112]
for sub in allsubjects:
    subjectNum = sub
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
        cmd = ("3dFWHMx -acf NULL -mask {0} -input {1}/{2}/{3}/{2}_{3}_task-faces.errts+tlrc | tail -n1 > {1}/{2}/{3}/params.txt".format(whole_brain_mask,analyses_out,bids_id,ses_id))
        call(cmd,shell=True)


