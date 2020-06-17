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
wholebrain_mask = COMMON_DIR + '/' + 'whole_brain_overlapping.nii.gz'
subjectDay=1
ses_id = 'ses-{0:02d}'.format(subjectDay)
covar_file = second_level + '/' + 'FD_covar_{0}.txt'.format(ses_id)

# this makes a nifti file with the following 6 sub-briks:
# Number of values stored at each pixel = 19
#   -- At sub-brick #0 'fearful_0#0_Coef' datum type is float:     -1.53413 to       1.94578
#   -- At sub-brick #1 'fearful_1#0_Coef' datum type is float:     -1.90816 to        1.6733
#   -- At sub-brick #2 'fearful_2#0_Coef' datum type is float:      -1.7612 to       2.01569
#   -- At sub-brick #3 'fearful_3#0_Coef' datum type is float:     -1.96247 to       2.13466
#   -- At sub-brick #4 'fearful_4#0_Coef' datum type is float:     -1.90552 to       1.72674
#   -- At sub-brick #5 'fearful_5#0_Coef' datum type is float:     -1.40985 to       1.35156
#   -- At sub-brick #6 'happy_0#0_Coef' datum type is float:     -1.37782 to       1.70649
#   -- At sub-brick #7 'happy_1#0_Coef' datum type is float:     -1.72388 to       1.94741
#   -- At sub-brick #8 'happy_2#0_Coef' datum type is float:      -1.8239 to       2.09532
#   -- At sub-brick #9 'happy_3#0_Coef' datum type is float:     -1.66571 to       1.99966
#   -- At sub-brick #10 'happy_4#0_Coef' datum type is float:     -1.89257 to          2.08
#   -- At sub-brick #11 'happy_5#0_Coef' datum type is float:     -1.31277 to       1.93948
#   -- At sub-brick #12 'neutral_0#0_Coef' datum type is float:     -1.65821 to       1.81096
#   -- At sub-brick #13 'neutral_1#0_Coef' datum type is float:     -1.84172 to       1.92837
#   -- At sub-brick #14 'neutral_2#0_Coef' datum type is float:     -1.83799 to        1.7618
#   -- At sub-brick #15 'neutral_3#0_Coef' datum type is float:     -1.77472 to       1.93142
#   -- At sub-brick #16 'neutral_4#0_Coef' datum type is float:     -1.64976 to       1.99883
#   -- At sub-brick #17 'neutral_5#0_Coef' datum type is float:     -1.56819 to       1.54069
#   -- At sub-brick #18 'fearful_diff#0_Coef' datum type is float:     -3.22231 to       2.67908
BRIK = 18
sessions = [1,3]
HC_subjects = [1,2,3,4,5 ,6,7,8,9,10,11]
n_HC = len(HC_subjects)
HC_subj_str = 'HC'
for s in np.arange(n_HC):
    bids_id = 'sub-{0:03d}'.format(HC_subjects[s])
    subject_stats = "{0}/{1}/{2}/{1}_{2}_task-faces_glm_coefs_trials_REML.nii.gz'[{3}]'".format(first_level,bids_id,ses_id,BRIK)
    HC_subj_str = HC_subj_str + ' ' + bids_id + ' ' + subject_stats
MDD_subjects = [101,102,103,104,105,106 ,107 ,108 ,109,110,111,112,113,114]
n_MDD = len(MDD_subjects)
MDD_subj_str = 'MDD'
for s in np.arange(n_MDD):
    bids_id = 'sub-{0:03d}'.format(MDD_subjects[s])
    subject_stats = "{0}/{1}/{2}/{1}_{2}_task-faces_glm_coefs_trials_REML.nii.gz'[{3}]'".format(first_level,bids_id,ses_id,BRIK)
    MDD_subj_str = MDD_subj_str + ' ' + bids_id + ' ' + subject_stats
# TEST -- move to the directory where you want to save everything
move_to_dir = "{0}/{1}/".format(second_level,ses_id)
os.chdir(move_to_dir)
command = ("3dttest++ -setA {0} ".format(MDD_subj_str) +
            "-setB {0} ".format(HC_subj_str) +
            "-prefix {0}/{1}/{1}_stats_fearful_diff_NOmask.ttest.nii.gz ".format(second_level,ses_id) +
            "-AminusB " 
            "-covariates {0} ".format(covar_file) +
            "-prefix_clustsim {0}_stats_fearful_diff_nomask ".format(ses_id) +
            "-mask {0} ".format(wholebrain_mask) +
            "-Clustsim "
            )


print(command)
call(command,shell=True)



