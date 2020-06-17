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


# -- At sub-brick #0 'neutral_F#0_Coef' datum type is float:     -1.35965 to       1.35067
# -- At sub-brick #1 'neutral_L#0_Coef' datum type is float:     -1.38689 to      0.858945
# -- At sub-brick #2 'happy_F#0_Coef' datum type is float:     -1.04092 to       1.35203
# -- At sub-brick #3 'happy_L#0_Coef' datum type is float:      -1.1896 to       1.28563
# -- At sub-brick #4 'fearful_F#0_Coef' datum type is float:     -1.28702 to       1.10611
# -- At sub-brick #5 'fearful_L#0_Coef' datum type is float:     -1.43598 to       1.18876
# -- At sub-brick #6 'happyLvF#0_Coef' datum type is float:     -1.57109 to        1.6465
# -- At sub-brick #7 'fearfulLvF#0_Coef' datum type is float:     -1.49013 to       1.50785
# -- At sub-brick #8 'fearfulvneutralL#0_Coef' datum type is float:     -1.48663 to       1.42359
# -- At sub-brick #9 'fearfulvneutralL#0_Coef' datum type is float:     -1.48663 to       1.42359
# -- At sub-brick #10 'fearfulvneutralF#0_Coef' datum type is float:     -1.67349 to       1.67527
# -- At sub-brick #11 'happyvneutralF#0_Coef' datum type is float:     -1.36445 to       1.66251
# -- At sub-brick #12 'happyvneutralL#0_Coef' datum type is float:     -1.32911 to       1.90298


# we want to average amygdla activity for:
# negative last - negagtive first --> 7
# negative last - neutral last --> repeated oh well -- 8
# negative first -  neutral first --> 10
# positive last - positive first --> 6
# postiive last - neutral last --> 12
# positive first -  neutral first --> 11

#allsubjects = [1,3,4,5,6,7,8,9,10,11,101,102,103,104,105,106,107,108,109,110,111,112,113,114]
allsubjects = [1]
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

        stats_file = "{0}/{1}_{2}_task-faces_glm_coefs_separate_REML.nii.gz'[7]'".format(output_path, bids_id, ses_id)
        output_text = "{0}/{1}_{2}_task-faces_negL_negF_amgyavg.txt".format(output_path,bids_id,ses_id)
        cmd = "3dmaskave -mask {0} -quiet {1} > {2}".format(amygdala_mask,stats_file,output_text)
        if not os.path.isfile(output_text):
            print('AVERAGING AMYGDALA MASK NEG')
            call(cmd,shell=True)
        else:
            print('SKIPPING 7')
        stats_file = "{0}/{1}_{2}_task-faces_glm_coefs_separate_REML.nii.gz'[8]'".format(output_path, bids_id, ses_id)
        output_text = "{0}/{1}_{2}_task-faces_negL_neutL_amgyavg.txt".format(output_path,bids_id,ses_id)
        cmd = "3dmaskave -mask {0} -quiet {1} > {2}".format(amygdala_mask,stats_file,output_text)
        if not os.path.isfile(output_text):
            print('AVERAGING AMYGDALA MASK NEG')
            call(cmd,shell=True)
        else:
            print('SKIPPING 8')
        stats_file = "{0}/{1}_{2}_task-faces_glm_coefs_separate_REML.nii.gz'[10]'".format(output_path, bids_id, ses_id)
        output_text = "{0}/{1}_{2}_task-faces_negF_neutF_amgyavg.txt".format(output_path,bids_id,ses_id)
        cmd = "3dmaskave -mask {0} -quiet {1} > {2}".format(amygdala_mask,stats_file,output_text)
        if not os.path.isfile(output_text):
            print('AVERAGING AMYGDALA MASK NEG')
            call(cmd,shell=True)
        else:
            print('SKIPPING 10')
        stats_file = "{0}/{1}_{2}_task-faces_glm_coefs_separate_REML.nii.gz'[6]'".format(output_path, bids_id, ses_id)
        output_text = "{0}/{1}_{2}_task-faces_posL_posF_amgyavg.txt".format(output_path,bids_id,ses_id)
        cmd = "3dmaskave -mask {0} -quiet {1} > {2}".format(amygdala_mask,stats_file,output_text)
        if not os.path.isfile(output_text):
            print('AVERAGING AMYGDALA MASK NEG')
            call(cmd,shell=True)
        else:
            print('SKIPPING 6')
        stats_file = "{0}/{1}_{2}_task-faces_glm_coefs_separate_REML.nii.gz'[12]'".format(output_path, bids_id, ses_id)
        output_text = "{0}/{1}_{2}_task-faces_posL_neutL_amgyavg.txt".format(output_path,bids_id,ses_id)
        cmd = "3dmaskave -mask {0} -quiet {1} > {2}".format(amygdala_mask,stats_file,output_text)
        if not os.path.isfile(output_text):
            print('AVERAGING AMYGDALA MASK NEG')
            call(cmd,shell=True)
        else:
            print('SKIPPING 12')
        stats_file = "{0}/{1}_{2}_task-faces_glm_coefs_separate_REML.nii.gz'[11]'".format(output_path, bids_id, ses_id)
        output_text = "{0}/{1}_{2}_task-faces_posF_neutF_amgyavg.txt".format(output_path,bids_id,ses_id)
        cmd = "3dmaskave -mask {0} -quiet {1} > {2}".format(amygdala_mask,stats_file,output_text)
        if not os.path.isfile(output_text):
            print('AVERAGING AMYGDALA MASK NEG')
            call(cmd,shell=True)
        else:
            print('SKIPPING 8')

