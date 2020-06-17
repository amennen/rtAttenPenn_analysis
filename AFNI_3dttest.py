# PURPOSE: run AFNI noise regression

import os
import glob
from shutil import copyfile
import pandas as pd
import json
import numpy as np
from subprocess import call
import sys
fmriprep_out="/data/jux/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/fmriprep"
reg_save_dir='/data/jux/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/resting/confound_EVs'
trunc_save_dir = '/data/jux/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/resting/trunc'
noise_save_dir = '/data/jux/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/resting/clean'
second_level = noise_save_dir + '/' + 'group_level'

FP_mask = '/data/jux/cnds/amennen/rtAttenPenn/MNI_things/Yeo2011_6Network_mask_reoriented_resampled.nii.gz'
COMMON_DIR='/data/jux/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/mni_anat'
#common_base = 'dlPFC_in_MNI'
#dlPFC_mask = COMMON_DIR + '/' + common_base + '_overlapping' + '.nii.gz'
dlPFC_mask = '/data/jux/cnds/amennen/rtAttenPenn/MNI_things/mni_GM_ACC_MFG_IFG_intersect.nii.gz'
subjectDay=1
ses_id = 'ses-{0:02d}'.format(subjectDay)
covar_file = second_level + '/' + 'FD_covar_{0}.txt'.format(ses_id)


HC_subjects = [3 ,4 ,5 ,6,7,8,9,10,11]
n_HC = len(HC_subjects)
HC_subj_str = 'HC'
for s in np.arange(n_HC):
	bids_id = 'sub-{0:03d}'.format(HC_subjects[s])
	clean_path = noise_save_dir + '/' + bids_id + '/' + ses_id
	subject_saved_z = "{0}/{1}_{2}_task_rest_corr_r2z_LAMYG.nii.gz".format(clean_path,bids_id,ses_id)
	HC_subj_str = HC_subj_str + ' ' + bids_id + ' ' + subject_saved_z
MDD_subjects = [106 ,107 ,108 ,109,110,111,112,113]
n_MDD = len(MDD_subjects)
MDD_subj_str = 'MDD'
for s in np.arange(n_MDD):
	bids_id = 'sub-{0:03d}'.format(MDD_subjects[s])
	clean_path = noise_save_dir + '/' + bids_id + '/' + ses_id
	subject_saved_z = "{0}/{1}_{2}_task_rest_corr_r2z_LAMYG.nii.gz".format(clean_path,bids_id,ses_id)
	MDD_subj_str = MDD_subj_str + ' ' + bids_id + ' ' + subject_saved_z

move_to_dir = "{0}/{1}/".format(second_level,ses_id)
if not os.path.exists(move_to_dir): # if haven't run this already
        cmd = 'mkdir -pv {0}'.format(move_to_dir)
        call(cmd,shell=True)
os.chdir(move_to_dir)

# command = ("3dttest++ -unpooled -setA {0} ".format(MDD_subj_str) +
# 			"-setB {0} ".format(HC_subj_str) +
# 			"-prefix {0}/{1}/stats_dlPFC_OPTIONS_REM.nii.gz ".format(second_level,ses_id) +
# 			"-AminusB " 
# 			"-covariates {0} ".format(covar_file) +
# 			"-prefix_clustsim {0}_stats_ACC_OPTIONS_REM ".format(ses_id) +
# 			"-ETAC " +
# 			"-mask {0}".format(dlPFC_mask)
# 			)

command = ("3dttest++ -unpooled -setA {0} ".format(MDD_subj_str) +
			"-setB {0} ".format(HC_subj_str) +
			"-prefix {0}/{1}/stats_dlPFC_noBLUR.nii.gz ".format(second_level,ses_id) +
			"-AminusB " 
			"-covariates {0} ".format(covar_file) +
			"-prefix_clustsim {0}_stats_dlPFC_noBLUR ".format(ses_id) +
			"-ETAC " +
            "-ETAC_opt NN=2:sid=1:hpow=0:name=test1:pthr=0.01/0.001/10:fpr=9 " +
			"-mask {0}".format(dlPFC_mask)
			)
call(command,shell=True)

