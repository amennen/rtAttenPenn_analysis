
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
subjectNum = np.int(sys.argv[1])
bids_id = 'sub-{0:03d}'.format(subjectNum)
all_categories = ['fearful','happy', 'neutral', 'object']
nhalves=2
# concatenate confound EVS
print(bids_id)
sessions = [1,3]
nRuns = 2
for s in sessions:
    subjectDay = s
    ses_id = 'ses-{0:02d}'.format(subjectDay)
    print(ses_id)
    confounds_dir = cf_dir + '/' + bids_id + '/' + ses_id
    run1_cf = confounds_dir + '/' + bids_id + '_' + ses_id + '_' + 'task-faces_rec-uncorrected_run-01_bold_confounds.tsv'
    run2_cf = confounds_dir + '/' + bids_id + '_' + ses_id + '_' + 'task-faces_rec-uncorrected_run-02_bold_confounds.tsv'

    r1_tsv = pd.read_csv(run1_cf, sep='\t')
    r2_tsv = pd.read_csv(run2_cf, sep='\t')
    frames = [r1_tsv,r2_tsv]
    newdf = pd.concat(frames)
    full_save_path = confounds_dir + '/' + bids_id + '_' + ses_id + '_' + 'task-faces_rec-uncorrected_COMBINED_bold_confounds.1D'
    if not os.path.exists(full_save_path): 
        newdf.to_csv(full_save_path, sep='\t',index=False,header=False)

    # we have 6 types PER condition and 3 conditions so 18 regressors
    reg_counter=1
    all_reg = ''
    for category in all_categories:
        for h in np.arange(nhalves):
            this_reg = "-stim_times {0} {1}/{2}_half_{3}.txt 'BLOCK(3,1)' -stim_label {0} {2}_{3} ".format(reg_counter,os.path.join(timing_path, bids_id,ses_id),category,h)
            all_reg = all_reg + this_reg
            reg_counter += 1
    output_path = "{0}/{1}/{2}".format(analyses_out,bids_id,ses_id)
    if not os.path.exists(output_path):
        cmd = 'mkdir -pv {0}'.format(output_path)
        call(cmd,shell=True)
    # look at how many jobs it's using bc it might be trying to use all CPUs/jobs that are available
    # put a mask *****-- some brain mask for the template space to be used for every subject
    # automask will only run for each person with what it sense is the brain
    cmd = ("3dDeconvolve -polort A "
                "-input "
                "{0}/{1}/{2}/{1}_{2}_task-faces_rec-uncorrected_run-01_bold_space-MNI152NLin2009cAsym_preproc.nii.gz "
                "{0}/{1}/{2}/{1}_{2}_task-faces_rec-uncorrected_run-02_bold_space-MNI152NLin2009cAsym_preproc.nii.gz "
                "-mask {5} "
                "-num_glt 5 "
                "-gltsym 'SYM: +fearful_1 -neutral_1' -glt_label 1 'fearful_minus_neut_1' "
                "-gltsym 'SYM: +fearful_0 -neutral_0' -glt_label 2 'fearful_minus_neut_0' "
                "-gltsym 'SYM: +happy_1 -neutral_1' -glt_label 3 'happy_minus_neut_1' "
                "-gltsym 'SYM: +happy_0 -neutral_0' -glt_label 4 'happy_minus_neut_0' "
                "-gltsym 'SYM: +fearful_0 +neutral_0 +happy_0 -3*object_0 +fearful_1 +neutral_1 +happy_1 -3*object_1' -glt_label 5 'faces_minus_object' "
                "-local_times -num_stimts 8 {3} "
                "-ortvec {4} -fout -tout "
                "-x1D {6}/{1}/{2}/{1}_{2}_task-faces_glm_half_xmat_ALL_OPTIONS.1D "
                "-bucket {6}/{1}/{2}/{1}_{2}_task-faces_glm_half_ALL_OPTIONS.stats ".format(run_path, 
                    bids_id, ses_id,all_reg,full_save_path,whole_brain_mask,analyses_out))

    call(cmd,shell=True)
    # prints and write to file 3dreml fit command
    # runs glm like this too

    # can use -x1D_stop to say don't bother fitting first, use reml fit only
    with open(os.path.join(output_path, '{0}_{1}_task-faces_glm_half_ALL_OPTIONS.REML_cmd'.format(bids_id, ses_id))) as f: 
        reml_cmd = '3dREMLfit' + f.read().split('3dREMLfit')[-1]
    call(reml_cmd, shell=True)

    cmd = ("3dbucket -prefix {0}/{1}_{2}_task-faces_glm_coefs_half_ALL_OPTIONS_REML.nii.gz "
                "{0}/{1}_{2}_task-faces_glm_half_ALL_OPTIONS.stats_REML+tlrc.BRIK'[1..25(2)]'".format(output_path, bids_id, ses_id))
    call(cmd,shell=True)
# old way (without including objects was 1..15(2))

    # this makes a nifti file with the following 13 sub-briks:
# # Number of values stored at each pixel = 37
# Number of values stored at each pixel = 15
  # -- At sub-brick #1 'fearful_0#0_Coef' datum type is float:    -0.652538 to      0.735138
  # -- At sub-brick #2 'fearful_0#0_Tstat' datum type is float:     -4.32003 to       3.98017
  #    statcode = fitt;  statpar = 263
  # -- At sub-brick #3 'fearful_1#0_Coef' datum type is float:    -0.751652 to      0.611238
  # -- At sub-brick #4 'fearful_1#0_Tstat' datum type is float:     -3.90417 to       3.76123
  #    statcode = fitt;  statpar = 263
  # -- At sub-brick #5 'happy_0#0_Coef' datum type is float:    -0.562919 to       1.07611
  # -- At sub-brick #6 'happy_0#0_Tstat' datum type is float:     -3.29259 to       5.21842
  #    statcode = fitt;  statpar = 263
  # -- At sub-brick #7 'happy_1#0_Coef' datum type is float:    -0.646672 to      0.858241
  # -- At sub-brick #8 'happy_1#0_Tstat' datum type is float:     -3.93541 to       5.44093
  #    statcode = fitt;  statpar = 263
  # -- At sub-brick #9 'neutral_0#0_Coef' datum type is float:    -0.809451 to      0.980771
  # -- At sub-brick #10 'neutral_0#0_Tstat' datum type is float:     -4.42642 to       5.22644
  #    statcode = fitt;  statpar = 263
  # -- At sub-brick #11 'neutral_1#0_Coef' datum type is float:     -0.91532 to      0.762976
  # -- At sub-brick #12 'neutral_1#0_Tstat' datum type is float:     -4.02603 to       5.12823
  #    statcode = fitt;  statpar = 263
  # -- At sub-brick #13 'object_0#0_Coef' datum type is float:    -0.665103 to       1.01407
  # -- At sub-brick #14 'object_0#0_Tstat' datum type is float:     -3.50966 to       5.40363
  #    statcode = fitt;  statpar = 263
  # -- At sub-brick #15 'object_1#0_Coef' datum type is float:     -0.55497 to      0.788019
  # -- At sub-brick #16 'object_1#0_Tstat' datum type is float:      -3.5248 to       4.00635
  #    statcode = fitt;  statpar = 263
  # -- At sub-brick #17 'fearful_minus_neut_1#0_Coef' datum type is float:    -0.799642 to      0.855844
  # -- At sub-brick #18 'fearful_minus_neut_1#0_Tstat' datum type is float:     -3.20625 to        3.9549
  #    statcode = fitt;  statpar = 263
  # -- At sub-brick #19 'fearful_minus_neut_0#0_Coef' datum type is float:    -0.888685 to       1.14895
  # -- At sub-brick #20 'fearful_minus_neut_0#0_Tstat' datum type is float:      -3.7035 to       3.59442
  #    statcode = fitt;  statpar = 263
  # -- At sub-brick #21 'happy_minus_neut_1#0_Coef' datum type is float:    -0.898385 to       1.22493
  # -- At sub-brick #22 'happy_minus_neut_1#0_Tstat' datum type is float:     -3.55061 to       4.75087
  #    statcode = fitt;  statpar = 263
  # -- At sub-brick #23 'happy_minus_neut_0#0_Coef' datum type is float:    -0.776683 to       1.07859
  # -- At sub-brick #24 'happy_minus_neut_0#0_Tstat' datum type is float:     -3.18022 to       4.36335
  #    statcode = fitt;  statpar = 263
  # -- At sub-brick #25 'faces_minus_object#0_Coef' datum type is float:     -3.42583 to       3.89806
  # -- At sub-brick #26 'faces_minus_object#0_Tstat' datum type is float:     -3.59358 to       4.80634
