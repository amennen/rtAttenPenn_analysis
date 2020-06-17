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
ntrials=6
  # -- At sub-brick #0 'fearful_0#0_Coef' datum type is float:     -1.90121 to       1.55708
  # -- At sub-brick #1 'fearful_1#0_Coef' datum type is float:      -2.2784 to       2.09285
  # -- At sub-brick #2 'fearful_2#0_Coef' datum type is float:     -2.40743 to       2.15495
  # -- At sub-brick #3 'fearful_3#0_Coef' datum type is float:     -1.89531 to        2.4919
  # -- At sub-brick #4 'fearful_4#0_Coef' datum type is float:     -2.71296 to       1.53727
  # -- At sub-brick #5 'fearful_5#0_Coef' datum type is float:      -1.2813 to       2.14288
  # -- At sub-brick #6 'happy_0#0_Coef' datum type is float:     -1.59698 to       1.54195
  # -- At sub-brick #7 'happy_1#0_Coef' datum type is float:     -1.93512 to       1.93964
  # -- At sub-brick #8 'happy_2#0_Coef' datum type is float:     -2.27916 to       2.10593
  # -- At sub-brick #9 'happy_3#0_Coef' datum type is float:     -2.33265 to       2.27278
  # -- At sub-brick #10 'happy_4#0_Coef' datum type is float:     -2.00524 to       2.17064
  # -- At sub-brick #11 'happy_5#0_Coef' datum type is float:     -1.47019 to       1.77708
  # -- At sub-brick #12 'neutral_0#0_Coef' datum type is float:     -1.47353 to       1.84388
  # -- At sub-brick #13 'neutral_1#0_Coef' datum type is float:     -2.07753 to       1.90099
  # -- At sub-brick #14 'neutral_2#0_Coef' datum type is float:     -1.81797 to       2.27328
  # -- At sub-brick #15 'neutral_3#0_Coef' datum type is float:     -1.95104 to       2.14175
  # -- At sub-brick #16 'neutral_4#0_Coef' datum type is float:     -2.01329 to       1.61303
  # -- At sub-brick #17 'neutral_5#0_Coef' datum type is float:     -1.56606 to       1.58366


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
            for trial in np.arange(ntrials):
                stats_file = "{0}/{1}_{2}_task-faces_glm_coefs_trials_REML.nii.gz'[{3}]'".format(output_path, bids_id, ses_id,reg_counter)
                output_text = "{0}/{1}_{2}_task-faces_{3}_{4}_amgyavg.txt".format(output_path,bids_id,ses_id,category,trial)
                cmd = "3dmaskave -mask {0} -quiet {1} > {2}".format(amygdala_mask,stats_file,output_text)
                print(cmd)
                reg_counter+=1
                if not os.path.isfile(output_text):
                    print('AVERAGING AMYGDALA MASK NEG')
                    call(cmd,shell=True)
                else:
                    print('SKIPPING 7')
        
