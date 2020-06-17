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
#wholebrain_mask = COMMON_DIR + '/' + 'whole_brain_overlapping.nii.gz'
wholebrain_mask='/data/jux/cnds/amennen/rtAttenPenn/MNI_things/whole_brain_overlapping_gm_intersect.nii.gz'
subjectDay=1
ses_id = 'ses-{0:02d}'.format(subjectDay)
covar_file = second_level + '/' + 'FD_covar_{0}.txt'.format(ses_id)
dlPFC_mask = '/data/jux/cnds/amennen/rtAttenPenn/MNI_things/mni_GM_ACC_MFG_IFG_intersect.nii.gz'
dmn_yeo_mask = '/data/jux/cnds/amennen/rtAttenPenn/MNI_things/Yeo2011_7Network_mask_reoriented_resampled.nii.gz'
dmn_gm_mask = '/data/jux/cnds/amennen/rtAttenPenn/MNI_things/mni_YEO_DMN_intersect.nii.gz'
# this makes a nifti file with the following 6 sub-briks:
# Number of values stored at each pixel = 19
# Number of values stored at each pixel = 7
  # -- At sub-brick #0 'fearful_0#0_Coef' datum type is float:    -0.608366 to      0.727068
  # -- At sub-brick #1 'fearful_1#0_Coef' datum type is float:    -0.765667 to       0.56305
  # -- At sub-brick #2 'happy_0#0_Coef' datum type is float:    -0.577456 to        1.0575
  # -- At sub-brick #3 'happy_1#0_Coef' datum type is float:    -0.619488 to      0.858261
  # -- At sub-brick #4 'neutral_0#0_Coef' datum type is float:    -0.826832 to      0.982332
  # -- At sub-brick #5 'neutral_1#0_Coef' datum type is float:    -0.853766 to      0.669537
  # -- At sub-brick #6 'fearful_diff_half#0_Coef' datum type is float:    -0.854376 to       0.67483
  # -- At sub-brick #7 'fearful_neut_1#0_Coef' datum type is float:    -0.791528 to      0.874809


BRIK = 6
sessions = [1,3]
HC_subjects = [1,2,3,4,5 ,6,7,8,9,10,11]
n_HC = len(HC_subjects)
HC_subj_str = 'HC'
for s in np.arange(n_HC):
    bids_id = 'sub-{0:03d}'.format(HC_subjects[s])
    subject_stats = "{0}/{1}/{2}/{1}_{2}_task-faces_glm_coefs_half_REML.nii.gz'[{3}]'".format(first_level,bids_id,ses_id,BRIK)
    HC_subj_str = HC_subj_str + ' ' + bids_id + ' ' + subject_stats
MDD_subjects = [101,102,103,104,105,106 ,107 ,108 ,109,110,111,112,113,114]
n_MDD = len(MDD_subjects)
MDD_subj_str = 'MDD'
for s in np.arange(n_MDD):
    bids_id = 'sub-{0:03d}'.format(MDD_subjects[s])
    subject_stats = "{0}/{1}/{2}/{1}_{2}_task-faces_glm_coefs_half_REML.nii.gz'[{3}]'".format(first_level,bids_id,ses_id,BRIK)
    MDD_subj_str = MDD_subj_str + ' ' + bids_id + ' ' + subject_stats
# TEST -- move to the directory where you want to save everything
move_to_dir = "{0}/{1}/".format(second_level,ses_id)
os.chdir(move_to_dir)
command = ("3dttest++ -setA {0} ".format(MDD_subj_str) +
            "-setB {0} ".format(HC_subj_str) +
            "-prefix {0}/{1}/{1}_stats_fearful_1_fearful_0_dmn_gm.ttest.nii.gz ".format(second_level,ses_id) +
            "-AminusB " 
            "-covariates {0} ".format(covar_file) +
            "-prefix_clustsim {0}_stats_fearful_1_fearful_0_dmn_gm ".format(ses_id) +
            "-mask {0} ".format(dmn_yeo_mask) +
            "-Clustsim "
            )


print(command)
call(command,shell=True)



