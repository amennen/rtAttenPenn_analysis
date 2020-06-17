# PURPOSE: run AFNI noise regression

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
dlPFC_mask = '/data/jux/cnds/amennen/rtAttenPenn/MNI_things/mni_GM_ACC_MFG_IFG_intersect.nii.gz'
covar_file = second_level + '/' + 'FD_covar_SES_mean.txt'

# this makes a nifti file with the following 6 sub-briks:
# sub-brick 0: neutral
# sub-brick 1: object
# sub-brick 2: happy
# sub-brick 3: feaful
# sub-brick 4: happy - neut
# sub-brick 5: negative - neut

BRIK_KEY = {}
BRIK_KEY[0] = 'neutral'
BRIK_KEY[1] = 'object'
BRIK_KEY[2] = 'happy'
BRIK_KEY[3] = 'fearful'
BRIK_KEY[4] = 'happyminusneut'
BRIK_KEY[5] = 'fearfulminusneut'
BRIK = 5
HC_subjects = [1,2,3,4,5 ,6,7,8,9,10,11]
n_HC = len(HC_subjects)
HC_subj_str = 'HC'
for s in np.arange(n_HC):
    bids_id = 'sub-{0:03d}'.format(HC_subjects[s])
    subject_stats = "{0}/{1}/ses-03_minus_ses-01/{1}_ses-03_minus_ses-01_task-faces_glm_coefs_BRIK_{2}.nii.gz".format(first_level,bids_id,BRIK)
    HC_subj_str = HC_subj_str + ' ' + bids_id + ' ' + subject_stats
MDD_subjects = [101,102,103,104,105,106 ,107 ,108 ,109,110,111,112]
n_MDD = len(MDD_subjects)
MDD_subj_str = 'MDD'
for s in np.arange(n_MDD):
    bids_id = 'sub-{0:03d}'.format(MDD_subjects[s])
    subject_stats = "{0}/{1}/ses-03_minus_ses-01/{1}_ses-03_minus_ses-01_task-faces_glm_coefs_BRIK_{2}.nii.gz".format(first_level,bids_id,BRIK)
    MDD_subj_str = MDD_subj_str + ' ' + bids_id + ' ' + subject_stats
# TEST -- move to the directory where you want to save everything
move_to_dir = "{0}/ses-03_minus_ses-01/".format(second_level)
if not os.path.exists(move_to_dir): # if haven't run this already
        cmd = 'mkdir -pv {0}'.format(move_to_dir)
        call(cmd,shell=True)
os.chdir(move_to_dir)
# command = ("3dttest++ -unpooled -setA {0} ".format(MDD_subj_str) +
#             "-setB {0} ".format(HC_subj_str) +
#             "-prefix {0}/ses-03_minus_ses-01/ses-03_minus_ses-01_stats_{1}_ACC_dlPFC_mask.ttest.nii.gz ".format(second_level,BRIK_KEY[BRIK]) +
#             "-AminusB " 
#             "-mask {0} ".format(dlPFC_mask) +
#             "-covariates {0} ".format(covar_file) +
#             "-prefix_clustsim ses-03_minus_ses-01_stats_{0}_ACC_dlPFC_mask ".format(BRIK_KEY[BRIK]) +
#             "-ETAC -ETAC_blur 0 4 6 8 " +
#             "-ETAC_opt NN=2:sid=1:hpow=0:name=test1:pthr=0.01/0.001/10:fpr=5"
#             )

command = ("3dttest++ -setA {0} ".format(MDD_subj_str) +
            "-setB {0} ".format(HC_subj_str) +
            "-prefix {0}/ses-03_minus_ses-01/ses-03_minus_ses-01_stats_{1}_ACC_dlPFC_mask_clustsim_noBLUR.nii.gz ".format(second_level,BRIK_KEY[BRIK]) +
            "-AminusB " 
            "-mask {0} ".format(dlPFC_mask) +
            "-covariates {0} ".format(covar_file) +
            "-prefix_clustsim ses-03_minus_ses-01_stats_{0}_ACC_dlPFC_mask_clustsim_noBLUR ".format(BRIK_KEY[BRIK]) +
            "-Clustsim "
            )

print(command)
call(command,shell=True)



