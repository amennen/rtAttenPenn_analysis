# PURPOSE: this just subtracts session 3 faces output minutes session 1 faces output (does for each BRIK separately)

import os
import glob
from shutil import copyfile
import pandas as pd
import json
import numpy as np
from subprocess import call
import sys

first_level = '/data/jux/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/afni/first_level/stats'
second_level = '/data/jux/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/afni/group_level/'

FP_mask = '/data/jux/cnds/amennen/rtAttenPenn/MNI_things/Yeo2011_6Network_mask_reoriented_resampled.nii.gz'
COMMON_DIR='/data/jux/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/mni_anat'
dlPFC_mask = '/data/jux/cnds/amennen/rtAttenPenn/MNI_things/ACC_MFG_IFG_FSL_2mm_bin0p5_resampled.nii.gz'

# this makes a nifti file with the following 6 sub-briks:
# sub-brick 0: neutral
# sub-brick 1: object
# sub-brick 2: happy
# sub-brick 3: feaful
# sub-brick 4: happy - neut
# sub-brick 5: negative - neut


# for each subject and day, subtract session 3 data - session 1 data

BRIK_KEY = {}
BRIK_KEY[0] = 'neutral'
BRIK_KEY[1] = 'object'
BRIK_KEY[2] = 'happy'
BRIK_KEY[3] = 'fearful'
BRIK_KEY[4] = 'happyminusneut'
BRIK_KEY[5] = 'fearfulminusneut'
BRIK = 5
all_subjects = [1,2,3,4,5 ,6,7,8,9,10,11,101,102,103,104,105,106 ,107 ,108 ,109,110,111,112]
n = len(all_subjects)
for s in np.arange(n):
    bids_id = 'sub-{0:03d}'.format(all_subjects[s])
    ses_id = 'ses-{0:02d}'.format(1)
    subject_stats_1 = "{0}/{1}/{2}/{1}_{2}_task-faces_glm_coefs_REML.nii.gz'[{3}]'".format(first_level,bids_id,ses_id,BRIK)
    ses_id = 'ses-{0:02d}'.format(3)
    subject_stats_2 = "{0}/{1}/{2}/{1}_{2}_task-faces_glm_coefs_REML.nii.gz'[{3}]'".format(first_level,bids_id,ses_id,BRIK)
    output_path = "{0}/{1}/ses-03_minus_ses-01".format(first_level,bids_id)
    if not os.path.exists(output_path): # if haven't run this already
        cmd = 'mkdir -pv {0}'.format(output_path)
        call(cmd,shell=True)
        output = "{0}/{1}/ses-03_minus_ses-01/{1}_ses-03_minus_ses-01_task-faces_glm_coefs_BRIK_{2}.nii.gz".format(first_level,bids_id,BRIK)

        cmd = ("3dcalc -a {0} ".format(subject_stats_2) + 
            "-b {0} ".format(subject_stats_1) + 
            "-expr 'a-b' -prefix {0}".format(output))
        call(cmd,shell=True)



