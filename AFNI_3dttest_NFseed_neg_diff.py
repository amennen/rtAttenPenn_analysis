# PURPOSE: run AFNI noise regression

import os
import glob
from shutil import copyfile
import pandas as pd
import json
import numpy as np
from subprocess import call
import sys

second_level = '/data/jux/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/afni/group_level/neurofeedback/'
noise_save_dir = '/data/jux/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/afni/first_level/neurofeedback/clean'

FP_mask = '/data/jux/cnds/amennen/rtAttenPenn/MNI_things/Yeo2011_6Network_mask_reoriented_resampled.nii.gz'
COMMON_DIR='/data/jux/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/mni_anat'
#wholebrain_mask = COMMON_DIR + '/' + 'whole_brain_overlapping.nii.gz'
wholebrain_mask='/data/jux/cnds/amennen/rtAttenPenn/MNI_things/whole_brain_overlapping_gm_intersect.nii.gz'
dlPFC_mask = '/data/jux/cnds/amennen/rtAttenPenn/MNI_things/mni_GM_ACC_MFG_IFG_intersect.nii.gz'
dmn_yeo_mask = '/data/jux/cnds/amennen/rtAttenPenn/MNI_things/Yeo2011_7Network_mask_reoriented_resampled.nii.gz'
dmn_gm_mask = '/data/jux/cnds/amennen/rtAttenPenn/MNI_things/mni_YEO_DMN_intersect.nii.gz'


# FIRST: we have to calculate the average correlation per voxel over the three runs at the beginning and end
calculate_average=0
sessions = [1,3]
allsubjects = [1,2,3,4,5,6,7,8,9,10,11,101,102,103,104,105,106,107,108,109,110,111,112,113,114]
if calculate_average:
  for s in allsubjects:
    for ses in sessions:
      bids_id = 'sub-{0:03d}'.format(s)
      ses_id = 'ses-{0:02d}'.format(ses)
      if ses == 1:
        subject_stats_1 = "{0}/{1}/{2}/CATEGSEP_seed_correlation_NEG_run-02.nii.gz".format(noise_save_dir,bids_id,ses_id)
        subject_stats_2 = "{0}/{1}/{2}/CATEGSEP_seed_correlation_NEG_run-03.nii.gz".format(noise_save_dir,bids_id,ses_id)
        subject_stats_3 = "{0}/{1}/{2}/CATEGSEP_seed_correlation_NEG_run-04.nii.gz".format(noise_save_dir,bids_id,ses_id)
      elif ses == 3:
        subject_stats_1 = "{0}/{1}/{2}/CATEGSEP_seed_correlation_NEG_run-06.nii.gz".format(noise_save_dir,bids_id,ses_id)
        subject_stats_2 = "{0}/{1}/{2}/CATEGSEP_seed_correlation_NEG_run-07.nii.gz".format(noise_save_dir,bids_id,ses_id)
        subject_stats_3 = "{0}/{1}/{2}/CATEGSEP_seed_correlation_NEG_run-08.nii.gz".format(noise_save_dir,bids_id,ses_id)
      command = "3dcalc -a {3} -b {4} -c {5} -expr '(a+b+c)/3' -prefix {0}/{1}/{2}/CATEGSEP_seed_correlation_NEG_runAVG.nii.gz".format(noise_save_dir,bids_id,ses_id,subject_stats_1,subject_stats_2,subject_stats_3)
      call(command,shell=True)

# now calculate differences
calculate_diff=0
sessions = [1,3]
allsubjects = [1,2,3,4,5,6,7,8,9,10,11,101,102,103,104,105,106,107,108,109,110,111,112,113,114]
if calculate_diff:
  for s in allsubjects:
    bids_id = 'sub-{0:03d}'.format(s)
    avg_3 = "{0}/{1}/ses-03/CATEGSEP_seed_correlation_NEG_runAVG.nii.gz".format(noise_save_dir,bids_id)
    avg_1 = "{0}/{1}/ses-01/CATEGSEP_seed_correlation_NEG_runAVG.nii.gz".format(noise_save_dir,bids_id)
    output_path = "{0}/{1}/ses-03_minus_ses-01".format(noise_save_dir,bids_id)
    if not os.path.exists(output_path):
      os.makedirs(output_path)
    command = "3dcalc -a {2} -b {3} -expr 'b-a' -prefix {0}/{1}/ses-03_minus_ses-01/CATEGSEP_seed_correlation_NEG_runAVG_DIFF.nii.gz".format(noise_save_dir,bids_id,avg_1,avg_3)
    call(command,shell=True)


HC_subjects = [1,2,3,4,5 ,6,7,8,9,10,11]
n_HC = len(HC_subjects)
HC_subj_str = 'HC'
for s in np.arange(n_HC):
    bids_id = 'sub-{0:03d}'.format(HC_subjects[s])
    subject_stats = "{0}/{1}/ses-03_minus_ses-01/CATEGSEP_seed_correlation_NEG_runAVG_DIFF.nii.gz".format(noise_save_dir,bids_id)
    HC_subj_str = HC_subj_str + ' ' + bids_id + ' ' + subject_stats
MDD_subjects = [101,102,103,104,105,106 ,107 ,108 ,109,110,111,112,113,114]
n_MDD = len(MDD_subjects)
MDD_subj_str = 'MDD'
for s in np.arange(n_MDD):
    bids_id = 'sub-{0:03d}'.format(MDD_subjects[s])
    subject_stats = "{0}/{1}/ses-03_minus_ses-01/CATEGSEP_seed_correlation_NEG_runAVG_DIFF.nii.gz".format(noise_save_dir,bids_id)
    MDD_subj_str = MDD_subj_str + ' ' + bids_id + ' ' + subject_stats
# TEST -- move to the directory where you want to save everything
move_to_dir = "{0}/ses-03_minus_ses-01/".format(second_level)
os.chdir(move_to_dir)
command = ("3dttest++ -setA {0} ".format(MDD_subj_str) +
            "-setB {0} ".format(HC_subj_str) +
            "-prefix {0}/ses-03_minus_ses-01/stats_CATEGSEP_correlation_dlPFC.ttest.nii.gz ".format(second_level) +
            "-AminusB " 
            "-prefix_clustsim ses-03_minus_ses-01_stats_CATEGSEP_correlation_dlPFC " 
            "-mask {0} ".format(dlPFC_mask) +
            "-Clustsim "
            )


print(command)
call(command,shell=True)



