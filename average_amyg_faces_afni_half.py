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
ROI_DIR = '/data/jux/cnds/amennen/rtAttenPenn/MNI_things/clusters'
nClusters = 13
#all_categories = ['fearful','happy', 'neutral']
all_categories = ['fearful','happy', 'neutral', 'object']
all_contrasts = ['f_m_n_1', 'f_m_n_0', 'h_m_n_1', 'h_m_n_0', 'f_m_o']
# Number of values stored at each pixel = 19
  # -- At sub-brick #0 'fearful_0#0_Coef' datum type is float:    -0.608366 to      0.727068
  # -- At sub-brick #1 'fearful_1#0_Coef' datum type is float:    -0.765667 to       0.56305
  # -- At sub-brick #2 'happy_0#0_Coef' datum type is float:    -0.577456 to        1.0575
  # -- At sub-brick #3 'happy_1#0_Coef' datum type is float:    -0.619488 to      0.858261
  # -- At sub-brick #4 'neutral_0#0_Coef' datum type is float:    -0.826832 to      0.982332
  # -- At sub-brick #5 'neutral_1#0_Coef' datum type is float:    -0.853766 to      0.669537
  # -- At sub-brick #6 'fearful_diff_half#0_Coef' datum type is float:    -0.854376 to       0.67483
  # -- At sub-brick #7 'fearful_neut_1#0_Coef' datum type is float:    -0.791528 to      0.874809

# new version: doing contrasts instead and including objects -- just look for neg - neutral, faces - object
# Number of values stored at each pixel = 13
#   -- At sub-brick #0 'fearful_0#0_Coef' datum type is float:    -0.652538 to      0.735138
#   -- At sub-brick #1 'fearful_1#0_Coef' datum type is float:    -0.751652 to      0.611238
#   -- At sub-brick #2 'happy_0#0_Coef' datum type is float:    -0.562919 to       1.07611
#   -- At sub-brick #3 'happy_1#0_Coef' datum type is float:    -0.646672 to      0.858241
#   -- At sub-brick #4 'neutral_0#0_Coef' datum type is float:    -0.809451 to      0.980771
#   -- At sub-brick #5 'neutral_1#0_Coef' datum type is float:     -0.91532 to      0.762976
#   -- At sub-brick #6 'object_0#0_Coef' datum type is float:    -0.665103 to       1.01407
#   -- At sub-brick #7 'object_1#0_Coef' datum type is float:     -0.55497 to      0.788019
#   -- At sub-brick #8 'fearful_minus_neut_1#0_Coef' datum type is float:    -0.799642 to      0.855844
#   -- At sub-brick #9 'fearful_minus_neut_0#0_Coef' datum type is float:    -0.888685 to       1.14895
#   -- At sub-brick #10 'happy_minus_neut_1#0_Coef' datum type is float:    -0.898385 to       1.22493
#   -- At sub-brick #11 'happy_minus_neut_0#0_Coef' datum type is float:    -0.776683 to       1.07859
#   -- At sub-brick #12 'faces_minus_object#0_Coef' datum type is float:     -3.42583 to       3.89806

nhalves =2
allsubjects = [1,2,3,4,5,6,7,8,9,10,11,101,102,103,104,105,106,107,108,109,110,111,112,113,114]
n_contrasts = len(all_contrasts)
#allsubjects = [1]
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
        reg_counter=0
        for category in all_categories:
            for h in np.arange(nhalves):
                #stats_file = "{0}/{1}_{2}_task-faces_glm_coefs_half_REML.nii.gz'[{3}]'".format(output_path, bids_id, ses_id,reg_counter)
                stats_file = "{0}/{1}_{2}_task-faces_glm_coefs_half_ALL_OPTIONS_REML.nii.gz'[{3}]'".format(output_path, bids_id, ses_id,reg_counter)
                for cluster in np.arange(nClusters):
                  ROI = "{0}/cluster{1}sphere.nii.gz".format(ROI_DIR,cluster+1) # because clusters are numbered from 1 - 13 NOT 0 - 12
                  output_text = "{0}/{1}_{2}_task-faces_{3}_{4}_half_amgyavg_ALL_OPTIONS_cluster{5}.txt".format(output_path,bids_id,ses_id,category,h,cluster)
                  cmd = "3dmaskave -mask {0} -quiet {1} > {2}".format(ROI,stats_file,output_text)
                  #print(cmd)
                  if not os.path.isfile(output_text):
                      print('AVERAGING AMYGDALA MASK NEG')
                      call(cmd,shell=True)
                  else:
                      print('SKIPPING 7')
                reg_counter+=1

        # now get the contrasts
        for con in np.arange(n_contrasts):
          stats_file = "{0}/{1}_{2}_task-faces_glm_coefs_half_ALL_OPTIONS_REML.nii.gz'[{3}]'".format(output_path, bids_id, ses_id,reg_counter)
          for cluster in np.arange(nClusters):
            ROI = "{0}/cluster{1}sphere.nii.gz".format(ROI_DIR,cluster+1)
            output_text = "{0}/{1}_{2}_task-faces_{3}_half_amgyavg_ALL_OPTIONS_cluster{4}.txt".format(output_path,bids_id,ses_id,all_contrasts[con],cluster)
            cmd = "3dmaskave -mask {0} -quiet {1} > {2}".format(ROI,stats_file,output_text)
            #print(cmd)
            if not os.path.isfile(output_text):
                print('AVERAGING AMYGDALA MASK NEG')
                call(cmd,shell=True)
            else:
                print('SKIPPING 7')
          reg_counter += 1 
