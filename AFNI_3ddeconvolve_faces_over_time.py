
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
all_categories = ['fearful','happy', 'neutral']
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
    newdf.to_csv(full_save_path, sep='\t',index=False,header=False)

    # we have 6 types PER condition and 3 conditions so 18 regressors
    reg_counter=1
    all_reg = ''
    nreps=3
    for category in all_categories:
        for r in np.arange(nreps):
            for h in np.arange(nhalves):
                this_reg = "-stim_times {0} {1}/{2}_rep_{3}_half_{4}.txt 'BLOCK(3,1)' -stim_label {0} {2}_{3}_{4} ".format(reg_counter,os.path.join(timing_path, bids_id,ses_id),category,r,h)
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
                "-local_times -num_stimts 18 {3} "
                "-ortvec {4} -fout -tout "
                "-x1D {6}/{1}/{2}/{1}_{2}_task-faces_glm_over_time_xmat.1D "
                "-bucket {6}/{1}/{2}/{1}_{2}_task-faces_glm_over_time.stats ".format(run_path, 
                    bids_id, ses_id,all_reg,full_save_path,whole_brain_mask,analyses_out))

    call(cmd,shell=True)
    # prints and write to file 3dreml fit command
    # runs glm like this too

    # can use -x1D_stop to say don't bother fitting first, use reml fit only
    with open(os.path.join(output_path, '{0}_{1}_task-faces_glm_over_time.REML_cmd'.format(bids_id, ses_id))) as f: 
        reml_cmd = '3dREMLfit' + f.read().split('3dREMLfit')[-1]
    call(reml_cmd, shell=True)

    cmd = ("3dbucket -prefix {0}/{1}_{2}_task-faces_glm_coefs_over_time_REML.nii.gz "
                "{0}/{1}_{2}_task-faces_glm_over_time.stats_REML+tlrc.BRIK'[1..35(2)]'".format(output_path, bids_id, ses_id))
    call(cmd,shell=True)

    # this makes a nifti file with the following 13 sub-briks:
# # Number of values stored at each pixel = 37
# Number of values stored at each pixel = 15
  # -- At sub-brick #0 'Full_Fstat' datum type is float:            0 to       3.75102
  #    statcode = fift;  statpar = 18 253
  # -- At sub-brick #1 'fearful_0_0#0_Coef' datum type is float:     -1.03408 to       1.19803
  # -- At sub-brick #2 'fearful_0_0#0_Tstat' datum type is float:     -3.99011 to       3.86907
  #    statcode = fitt;  statpar = 253
  # -- At sub-brick #3 'fearful_0_1#0_Coef' datum type is float:    -0.999183 to       1.05292
  # -- At sub-brick #4 'fearful_0_1#0_Tstat' datum type is float:      -3.6061 to       3.67299
  #    statcode = fitt;  statpar = 253
  # -- At sub-brick #5 'fearful_1_0#0_Coef' datum type is float:     -1.07788 to       1.07158
  # -- At sub-brick #6 'fearful_1_0#0_Tstat' datum type is float:     -3.66106 to       3.75968
  #    statcode = fitt;  statpar = 253
  # -- At sub-brick #7 'fearful_1_1#0_Coef' datum type is float:     -1.12629 to        1.2335
  # -- At sub-brick #8 'fearful_1_1#0_Tstat' datum type is float:     -3.69904 to       3.86984
  #    statcode = fitt;  statpar = 253
  # -- At sub-brick #9 'fearful_2_0#0_Coef' datum type is float:     -1.12702 to       1.86205
  # -- At sub-brick #10 'fearful_2_0#0_Tstat' datum type is float:     -4.31702 to       5.43639
  #    statcode = fitt;  statpar = 253
  # -- At sub-brick #11 'fearful_2_1#0_Coef' datum type is float:     -1.34127 to       1.11924
  # -- At sub-brick #12 'fearful_2_1#0_Tstat' datum type is float:     -4.29833 to       2.97044
  #    statcode = fitt;  statpar = 253
  # -- At sub-brick #13 'happy_0_0#0_Coef' datum type is float:    -0.972035 to       1.64382
  # -- At sub-brick #14 'happy_0_0#0_Tstat' datum type is float:     -3.57251 to       4.73988
  #    statcode = fitt;  statpar = 253
  # -- At sub-brick #15 'happy_0_1#0_Coef' datum type is float:     -1.20752 to       1.25996
  # -- At sub-brick #16 'happy_0_1#0_Tstat' datum type is float:     -4.36162 to       4.20405
  #    statcode = fitt;  statpar = 253
  # -- At sub-brick #17 'happy_1_0#0_Coef' datum type is float:     -1.08526 to       1.50406
  # -- At sub-brick #18 'happy_1_0#0_Tstat' datum type is float:     -3.64325 to        4.2142
  #    statcode = fitt;  statpar = 253
  # -- At sub-brick #19 'happy_1_1#0_Coef' datum type is float:      -1.2433 to       1.11493
  # -- At sub-brick #20 'happy_1_1#0_Tstat' datum type is float:     -3.79723 to       4.66918
  #    statcode = fitt;  statpar = 253
  # -- At sub-brick #21 'happy_2_0#0_Coef' datum type is float:     -1.06906 to       1.27176
  # -- At sub-brick #22 'happy_2_0#0_Tstat' datum type is float:     -3.33812 to       4.75203
  #    statcode = fitt;  statpar = 253
  # -- At sub-brick #23 'happy_2_1#0_Coef' datum type is float:     -1.31209 to       1.45733
  # -- At sub-brick #24 'happy_2_1#0_Tstat' datum type is float:     -4.24193 to       4.21772
  #    statcode = fitt;  statpar = 253
  # -- At sub-brick #25 'neutral_0_0#0_Coef' datum type is float:     -1.08011 to       1.30198
  # -- At sub-brick #26 'neutral_0_0#0_Tstat' datum type is float:     -3.15861 to       4.11072
  #    statcode = fitt;  statpar = 253
  # -- At sub-brick #27 'neutral_0_1#0_Coef' datum type is float:     -1.17224 to       1.20583
  # -- At sub-brick #28 'neutral_0_1#0_Tstat' datum type is float:     -3.92294 to       3.95424
  #    statcode = fitt;  statpar = 253
  # -- At sub-brick #29 'neutral_1_0#0_Coef' datum type is float:     -1.25101 to        1.4216
  # -- At sub-brick #30 'neutral_1_0#0_Tstat' datum type is float:     -4.24336 to       4.83906
  #    statcode = fitt;  statpar = 253
  # -- At sub-brick #31 'neutral_1_1#0_Coef' datum type is float:     -1.41156 to      0.894555
  # -- At sub-brick #32 'neutral_1_1#0_Tstat' datum type is float:     -4.30321 to       3.38636
  #    statcode = fitt;  statpar = 253
  # -- At sub-brick #33 'neutral_2_0#0_Coef' datum type is float:     -1.68936 to       1.43939
  # -- At sub-brick #34 'neutral_2_0#0_Tstat' datum type is float:     -4.74522 to       4.47401
  #    statcode = fitt;  statpar = 253
  # -- At sub-brick #35 'neutral_2_1#0_Coef' datum type is float:     -1.36118 to       1.45831
  # -- At sub-brick #36 'neutral_2_1#0_Tstat' datum type is float:     -4.41911 to       5.60693
  #    statcode = fitt;  statpar = 253



