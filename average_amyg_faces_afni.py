# purpose: average amygdala activity for each subject, compile and plot

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
amygdala_mask = '/data/jux/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/mni_anat/LAMYG_in_MNI_overlapping.nii.gz'


BRIK_KEY = {}
BRIK_KEY[0] = 'neutral'
BRIK_KEY[1] = 'object'
BRIK_KEY[2] = 'happy'
BRIK_KEY[3] = 'fearful'
BRIK_KEY[4] = 'happyminusneut'
BRIK_KEY[5] = 'fearfulminusneut'
BRIK = 5

allsubjects = [1,2,3,4,5,6,7,8,9,10,11,101,102,103,104,105,106,107,108,109,110,111,112]
for s in np.arange(len(allsubjects)):
    subjectNum = allsubjects[s]
    bids_id = 'sub-{0:03d}'.format(subjectNum)

    # concatenate confound EVS
    print(bids_id)
    sessions = [1,3]
    for ses in sessions:
        subjectDay = ses
        ses_id = 'ses-{0:02d}'.format(subjectDay)
        print(ses_id)
        output_path = "{0}/{1}/{2}".format(analyses_out,bids_id,ses_id)
        stats_file = "{0}/{1}_{2}_task-faces_glm_coefs_REML.nii.gz'[5]'".format(output_path, bids_id, ses_id)
        output_text = "{0}/{1}_{2}_task-faces_negminusneut_amgyavg.txt".format(output_path,bids_id,ses_id)
        cmd = "3dmaskave -mask {0} -quiet {1} > {2}".format(amygdala_mask,stats_file,output_text)
        if not os.path.isfile(output_text):
            print('AVERAGING AMYGDALA MASK NEG')
            call(cmd,shell=True)
        else:
            print('SKIPPING NEG')
        # now do the same thing for positive vs. neutral faces too
        stats_file = "{0}/{1}_{2}_task-faces_glm_coefs_REML.nii.gz'[4]'".format(output_path, bids_id, ses_id)
        output_text = "{0}/{1}_{2}_task-faces_posminusneut_amgyavg.txt".format(output_path,bids_id,ses_id)
        cmd = "3dmaskave -mask {0} -quiet {1} > {2}".format(amygdala_mask,stats_file,output_text)
        if not os.path.isfile(output_text):
            print('AVERAGING AMYGDALA MASK POS')
            call(cmd,shell=True)
        else:
            print('SKIPPING POS')

