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

all_categories = ['fearful','happy', 'neutral']
# Number of values stored at each pixel = 19
# Number of values stored at each pixel = 18
#   -- At sub-brick #0 'fearful_0_0#0_Coef' datum type is float:     -1.03408 to       1.19803
#   -- At sub-brick #1 'fearful_0_1#0_Coef' datum type is float:    -0.999183 to       1.05292
#   -- At sub-brick #2 'fearful_1_0#0_Coef' datum type is float:     -1.07788 to       1.07158
#   -- At sub-brick #3 'fearful_1_1#0_Coef' datum type is float:     -1.12629 to        1.2335
#   -- At sub-brick #4 'fearful_2_0#0_Coef' datum type is float:     -1.12702 to       1.86205
#   -- At sub-brick #5 'fearful_2_1#0_Coef' datum type is float:     -1.34127 to       1.11924
#   -- At sub-brick #6 'happy_0_0#0_Coef' datum type is float:    -0.972035 to       1.64382
#   -- At sub-brick #7 'happy_0_1#0_Coef' datum type is float:     -1.20752 to       1.25996
#   -- At sub-brick #8 'happy_1_0#0_Coef' datum type is float:     -1.08526 to       1.50406
#   -- At sub-brick #9 'happy_1_1#0_Coef' datum type is float:      -1.2433 to       1.11493
#   -- At sub-brick #10 'happy_2_0#0_Coef' datum type is float:     -1.06906 to       1.27176
#   -- At sub-brick #11 'happy_2_1#0_Coef' datum type is float:     -1.31209 to       1.45733
#   -- At sub-brick #12 'neutral_0_0#0_Coef' datum type is float:     -1.08011 to       1.30198
#   -- At sub-brick #13 'neutral_0_1#0_Coef' datum type is float:     -1.17224 to       1.20583
#   -- At sub-brick #14 'neutral_1_0#0_Coef' datum type is float:     -1.25101 to        1.4216
#   -- At sub-brick #15 'neutral_1_1#0_Coef' datum type is float:     -1.41156 to      0.894555
#   -- At sub-brick #16 'neutral_2_0#0_Coef' datum type is float:     -1.68936 to       1.43939
#   -- At sub-brick #17 'neutral_2_1#0_Coef' datum type is float:     -1.36118 to       1.45831


nreps=3
nhalves =2
allsubjects = [1,2,3,4,5,6,7,8,9,10,11,101,102,103,104,105,106,107,108,109,110,111,112,113,114]
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
          for r in np.arange(nreps):
            for h in np.arange(nhalves):
                stats_file = "{0}/{1}_{2}_task-faces_glm_coefs_over_time_REML.nii.gz'[{3}]'".format(output_path, bids_id, ses_id,reg_counter)
                output_text = "{0}/{1}_{2}_task-faces_{3}_{4}_{5}_over_time_amgyavg.txt".format(output_path,bids_id,ses_id,category,r,h)
                cmd = "3dmaskave -mask {0} -quiet {1} > {2}".format(amygdala_mask,stats_file,output_text)
                print(cmd)
                reg_counter+=1
                if not os.path.isfile(output_text):
                    print('AVERAGING AMYGDALA MASK NEG')
                    call(cmd,shell=True)
                else:
                    print('SKIPPING 7')
        
