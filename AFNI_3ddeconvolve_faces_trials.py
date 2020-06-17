
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
ntrials=6
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
    newdf.to_csv(full_save_path, sep='\t',index=False,header=False)
    if not os.path.exists(full_save_path): 
        newdf.to_csv(full_save_path, sep='\t',index=False,header=False)

    # we have 6 types PER condition and 3 conditions so 18 regressors
    reg_counter=1
    all_reg = ''
    for category in all_categories:
        for trial in np.arange(ntrials):
            this_reg = "-stim_times {0} {1}/{2}_trial_{3}.txt 'BLOCK(3,1)' -stim_label {0} {2}_{3} ".format(reg_counter,os.path.join(timing_path, bids_id,ses_id),category,trial)
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
                "-num_glt 1 "
                "-gltsym 'SYM: +fearful_5 +fearful_4 + fearful_3 -fearful_2 -fearful_1 -fearful_0' -glt_label 1 'fearful_diff' "
                "-local_times -num_stimts 24 {3} "
                "-ortvec {4} -fout -tout "
                "-x1D {6}/{1}/{2}/{1}_{2}_task-faces_glm_trials_xmat.1D "
                "-bucket {6}/{1}/{2}/{1}_{2}_task-faces_glm_trials.stats ".format(run_path, 
                    bids_id, ses_id,all_reg,full_save_path,whole_brain_mask,analyses_out))

    call(cmd,shell=True)
    # prints and write to file 3dreml fit command
    # runs glm like this too

    # can use -x1D_stop to say don't bother fitting first, use reml fit only
    with open(os.path.join(output_path, '{0}_{1}_task-faces_glm_trials.REML_cmd'.format(bids_id, ses_id))) as f: 
        reml_cmd = '3dREMLfit' + f.read().split('3dREMLfit')[-1]
    call(reml_cmd, shell=True)

    cmd = ("3dbucket -prefix {0}/{1}_{2}_task-faces_glm_coefs_trials_REML.nii.gz "
                "{0}/{1}_{2}_task-faces_glm_trials.stats_REML+tlrc.BRIK'[1..37(2)]'".format(output_path, bids_id, ses_id))
    call(cmd,shell=True)

    # this makes a nifti file with the following 13 sub-briks:
# Number of values stored at each pixel = 37
#   -- At sub-brick #0 'Full_Fstat' datum type is float:            0 to       13.9383
#      statcode = fift;  statpar = 18 253
#   -- At sub-brick #1 'fearful_0#0_Coef' datum type is float:     -1.90121 to       1.55708
#   -- At sub-brick #2 'fearful_0#0_Tstat' datum type is float:     -4.26038 to       4.51082
#      statcode = fitt;  statpar = 253
#   -- At sub-brick #3 'fearful_1#0_Coef' datum type is float:      -2.2784 to       2.09285
#   -- At sub-brick #4 'fearful_1#0_Tstat' datum type is float:     -4.51886 to       4.31511
#      statcode = fitt;  statpar = 253
#   -- At sub-brick #5 'fearful_2#0_Coef' datum type is float:     -2.40743 to       2.15495
#   -- At sub-brick #6 'fearful_2#0_Tstat' datum type is float:     -4.33171 to        5.2758
#      statcode = fitt;  statpar = 253
#   -- At sub-brick #7 'fearful_3#0_Coef' datum type is float:     -1.89531 to        2.4919
#   -- At sub-brick #8 'fearful_3#0_Tstat' datum type is float:     -3.82591 to       5.48598
#      statcode = fitt;  statpar = 253
#   -- At sub-brick #9 'fearful_4#0_Coef' datum type is float:     -2.71296 to       1.53727
#   -- At sub-brick #10 'fearful_4#0_Tstat' datum type is float:     -5.65024 to       4.02805
#      statcode = fitt;  statpar = 253
#   -- At sub-brick #11 'fearful_5#0_Coef' datum type is float:      -1.2813 to       2.14288
#   -- At sub-brick #12 'fearful_5#0_Tstat' datum type is float:     -3.44173 to       5.54898
#      statcode = fitt;  statpar = 253
#   -- At sub-brick #13 'happy_0#0_Coef' datum type is float:     -1.59698 to       1.54195
#   -- At sub-brick #14 'happy_0#0_Tstat' datum type is float:     -3.88754 to       4.12133
#      statcode = fitt;  statpar = 253
#   -- At sub-brick #15 'happy_1#0_Coef' datum type is float:     -1.93512 to       1.93964
#   -- At sub-brick #16 'happy_1#0_Tstat' datum type is float:     -3.88422 to       4.21983
#      statcode = fitt;  statpar = 253
#   -- At sub-brick #17 'happy_2#0_Coef' datum type is float:     -2.27916 to       2.10593
#   -- At sub-brick #18 'happy_2#0_Tstat' datum type is float:     -4.01674 to       4.61629
#      statcode = fitt;  statpar = 253
#   -- At sub-brick #19 'happy_3#0_Coef' datum type is float:     -2.33265 to       2.27278
#   -- At sub-brick #20 'happy_3#0_Tstat' datum type is float:     -3.95473 to        4.7334
#      statcode = fitt;  statpar = 253
#   -- At sub-brick #21 'happy_4#0_Coef' datum type is float:     -2.00524 to       2.17064
#   -- At sub-brick #22 'happy_4#0_Tstat' datum type is float:      -4.1737 to       4.77581
#      statcode = fitt;  statpar = 253
#   -- At sub-brick #23 'happy_5#0_Coef' datum type is float:     -1.47019 to       1.77708
#   -- At sub-brick #24 'happy_5#0_Tstat' datum type is float:     -3.51689 to       5.58311
#      statcode = fitt;  statpar = 253
#   -- At sub-brick #25 'neutral_0#0_Coef' datum type is float:     -1.47353 to       1.84388
#   -- At sub-brick #26 'neutral_0#0_Tstat' datum type is float:     -3.94696 to       5.99284
#      statcode = fitt;  statpar = 253
#   -- At sub-brick #27 'neutral_1#0_Coef' datum type is float:     -2.07753 to       1.90099
#   -- At sub-brick #28 'neutral_1#0_Tstat' datum type is float:      -4.4099 to       4.67036
#      statcode = fitt;  statpar = 253
#   -- At sub-brick #29 'neutral_2#0_Coef' datum type is float:     -1.81797 to       2.27328
#   -- At sub-brick #30 'neutral_2#0_Tstat' datum type is float:     -3.37905 to        4.3074
#      statcode = fitt;  statpar = 253
#   -- At sub-brick #31 'neutral_3#0_Coef' datum type is float:     -1.95104 to       2.14175
#   -- At sub-brick #32 'neutral_3#0_Tstat' datum type is float:     -3.45685 to       5.56816
#      statcode = fitt;  statpar = 253
#   -- At sub-brick #33 'neutral_4#0_Coef' datum type is float:     -2.01329 to       1.61303
#   -- At sub-brick #34 'neutral_4#0_Tstat' datum type is float:     -3.75077 to       3.96994
#      statcode = fitt;  statpar = 253
#   -- At sub-brick #35 'neutral_5#0_Coef' datum type is float:     -1.56606 to       1.58366
#   -- At sub-brick #36 'neutral_5#0_Tstat' datum type is float:     -4.11961 to       4.98896
#      statcode = fitt;  statpar = 253

