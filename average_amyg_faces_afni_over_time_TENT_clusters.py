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
cf_dir = '/data/jux/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/fsl/first_level/confound_EVs'
timing_path = '/data/jux/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/afni/first_level/timing_files'
analyses_out = '/data/jux/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/afni/first_level/stats'
whole_brain_mask = '/data/jux/cnds/amennen/rtAttenPenn/MNI_things/mni_icbm152_t1_tal_nlin_asym_09c_BOLD_mask_Penn.nii'
ROI_DIR = '/data/jux/cnds/amennen/rtAttenPenn/MNI_things/clusters'

amygdala_mask = '/data/jux/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/mni_anat/LAMYG_in_MNI_overlapping.nii.gz'

nClusters = 13
#all_categories = ['fearful','happy', 'neutral']
all_categories = ['fearful','happy', 'neutral', 'object']
#all_contrasts = ['f_m_n_1', 'f_m_n_0', 'h_m_n_1', 'h_m_n_0', 'f_m_o']

# theres 40, we want 10/category in the order listed above
n_beta_per_category = 9

allsubjects = [1,2,3,4,5,6,7,8,9,10,11,101,102,103,104,105,106,107,108,109,110,111,112,113,114]
#allsubjects = [1]
#for s in np.arange(len(allsubjects)):
subjectNum = np.int(sys.argv[1])

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
    for n in np.arange(n_beta_per_category):
      stats_file = "{0}/{1}_{2}_task-faces_glm_coefs_trials_REML_TENT.nii.gz'[{3}]'".format(output_path, bids_id, ses_id,reg_counter)
      for cluster in np.arange(nClusters):
        ROI = "{0}/cluster{1}sphere.nii.gz".format(ROI_DIR,cluster+1) # because clusters are numbered from 1 - 13 NOT 0 - 12
        output_text = "{0}/{1}_{2}_task-faces_{3}_{4}_TENT_cluster{5}.txt".format(output_path,bids_id,ses_id,category,n,cluster)
        cmd = "3dmaskave -mask {0} -quiet {1} > {2}".format(ROI,stats_file,output_text)
        #print(cmd)
        if not os.path.isfile(output_text):
            print('AVERAGING AMYGDALA MASK NEG')
            call(cmd,shell=True)
        else:
            print('SKIPPING 7')
      # get regular amygdala
      output_text = "{0}/{1}_{2}_task-faces_{3}_{4}_TENT_LAMYG_overlapping.txt".format(output_path,bids_id,ses_id,category,n)
      cmd = "3dmaskave -mask {0} -quiet {1} > {2}".format(amygdala_mask,stats_file,output_text)
      if not os.path.isfile(output_text):
        print('AVERAGING AMYGDALA MASK NEG')
        call(cmd,shell=True)
      else:
        print('SKIPPING LA')
      
      reg_counter+=1




