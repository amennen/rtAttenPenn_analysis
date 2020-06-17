
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
run_path = '/data/jux/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/afni/first_level/highpass_normalized_runs_baseline'
cf_dir = '/data/jux/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/fsl/first_level/confound_EVs'
timing_path = '/data/jux/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/afni/first_level/timing_files'
analyses_out = '/data/jux/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/afni/first_level/stats'
whole_brain_mask = '/data/jux/cnds/amennen/rtAttenPenn/MNI_things/mni_icbm152_t1_tal_nlin_asym_09c_BOLD_mask_Penn.nii'
subjectNum = np.int(sys.argv[1])
bids_id = 'sub-{0:03d}'.format(subjectNum)
all_categories = ['fearful','happy', 'neutral', 'object']
ntrials=1 # here we only want this first trials

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
            #this_reg = "-stim_times {0} {1}/{2}_trial_{3}.txt 'TENT(0,18,10)' -stim_label {0} {2}_{3} ".format(reg_counter,os.path.join(timing_path, bids_id,ses_id),category,trial)
            this_reg = "-stim_times {0} {1}/{2}_trial_{3}.txt 'TENT(0,24,9)' -stim_label {0} {2}_{3} ".format(reg_counter,os.path.join(timing_path, bids_id,ses_id),category,trial)

            all_reg = all_reg + this_reg
            reg_counter += 1
    output_path = "{0}/{1}/{2}".format(analyses_out,bids_id,ses_id)
    if not os.path.exists(output_path):
        cmd = 'mkdir -pv {0}'.format(output_path)
        call(cmd,shell=True)
    # look at how many jobs it's using bc it might be trying to use all CPUs/jobs that are available
    # put a mask *****-- some brain mask for the template space to be used for every subject
    # automask will only run for each person with what it sense is the brain
    # removing polort A
    cmd = ("3dDeconvolve  "
                "-input "
                "{0}/{1}/{2}/{1}_{2}_task-faces_rec-uncorrected_run-01_bold_space-MNI152NLin2009cAsym_preproc.nii.gz "
                "{0}/{1}/{2}/{1}_{2}_task-faces_rec-uncorrected_run-02_bold_space-MNI152NLin2009cAsym_preproc.nii.gz "
                "-mask {5} "
                # "-num_glt 1 "
                # "-gltsym 'SYM: +fearful_5 +fearful_4 + fearful_3 -fearful_2 -fearful_1 -fearful_0' -glt_label 1 'fearful_diff' "
                "-local_times -num_stimts 4 {3} "
                "-ortvec {4} -fout -tout "
                "-x1D {6}/{1}/{2}/{1}_{2}_task-faces_glm_trials_TENT_xmat.1D "
                "-bucket {6}/{1}/{2}/{1}_{2}_task-faces_glm_trials_TENT.stats ".format(run_path, 
                    bids_id, ses_id,all_reg,full_save_path,whole_brain_mask,analyses_out))

    call(cmd,shell=True)
    # prints and write to file 3dreml fit command
    # runs glm like this too

    # can use -x1D_stop to say don't bother fitting first, use reml fit only
    with open(os.path.join(output_path, '{0}_{1}_task-faces_glm_trials_TENT.REML_cmd'.format(bids_id, ses_id))) as f: 
        reml_cmd = '3dREMLfit' + f.read().split('3dREMLfit')[-1]
    call(reml_cmd, shell=True)

    # cmd = ("3dbucket -prefix {0}/{1}_{2}_task-faces_glm_coefs_trials_REML_TENT.nii.gz "
    #             "{0}/{1}_{2}_task-faces_glm_trials_TENT.stats_REML+tlrc.BRIK'[1..79(2)]'".format(output_path, bids_id, ses_id))
    cmd = ("3dbucket -prefix {0}/{1}_{2}_task-faces_glm_coefs_trials_REML_TENT.nii.gz "
            "{0}/{1}_{2}_task-faces_glm_trials_TENT.stats_REML+tlrc.BRIK'[1..71(2)]'".format(output_path, bids_id, ses_id))
    call(cmd,shell=True)

 # Number of values stored at each pixel = 81
 #  -- At sub-brick #0 'Full_Fstat' datum type is float:            0 to       366.918
 #     statcode = fift;  statpar = 40 231
 #  -- At sub-brick #1 'fearful_0#0_Coef' datum type is float:     -194.333 to       1237.76
 #  -- At sub-brick #2 'fearful_0#0_Tstat' datum type is float:     -15.1402 to       13.6072
 #     statcode = fitt;  statpar = 231
 #  -- At sub-brick #3 'fearful_0#1_Coef' datum type is float:     -67.8929 to        9.5736
 #  -- At sub-brick #4 'fearful_0#1_Tstat' datum type is float:     -6.97956 to       18.1474
 #     statcode = fitt;  statpar = 231
 #  -- At sub-brick #5 'fearful_0#2_Coef' datum type is float:     -10.9114 to       2.54532
 #  -- At sub-brick #6 'fearful_0#2_Tstat' datum type is float:     -3.62406 to       11.5028
 #     statcode = fitt;  statpar = 231
 #  -- At sub-brick #7 'fearful_0#3_Coef' datum type is float:      -1.7235 to       8.17957
 #  -- At sub-brick #8 'fearful_0#3_Tstat' datum type is float:     -7.20175 to       7.20175
 #     statcode = fitt;  statpar = 231
 #  -- At sub-brick #9 'fearful_0#4_Coef' datum type is float:     -27.5492 to       1.33623
 #  -- At sub-brick #10 'fearful_0#4_Tstat' datum type is float:     -4.43207 to       8.35034
 #     statcode = fitt;  statpar = 231
 #  -- At sub-brick #11 'fearful_0#5_Coef' datum type is float:     -54.3221 to       1.76355
 #  -- At sub-brick #12 'fearful_0#5_Tstat' datum type is float:     -5.23538 to       9.08644
 #     statcode = fitt;  statpar = 231
 #  -- At sub-brick #13 'fearful_0#6_Coef' datum type is float:      -2.1577 to         25.37
 #  -- At sub-brick #14 'fearful_0#6_Tstat' datum type is float:     -5.78857 to       7.19885
 #     statcode = fitt;  statpar = 231
 #  -- At sub-brick #15 'fearful_0#7_Coef' datum type is float:     -26.1111 to       5.17305
 #  -- At sub-brick #16 'fearful_0#7_Tstat' datum type is float:     -6.11743 to       7.46992
 #     statcode = fitt;  statpar = 231
 #  -- At sub-brick #17 'fearful_0#8_Coef' datum type is float:     -8.92728 to       1.54324
 #  -- At sub-brick #18 'fearful_0#8_Tstat' datum type is float:     -5.74866 to        8.7515
 #     statcode = fitt;  statpar = 231
 #  -- At sub-brick #19 'fearful_0#9_Coef' datum type is float:     -20.3737 to       4.13871
 #  -- At sub-brick #20 'fearful_0#9_Tstat' datum type is float:     -7.03108 to        8.1524
 #     statcode = fitt;  statpar = 231
 #  -- At sub-brick #21 'happy_0#0_Coef' datum type is float:     -336.957 to       88.0722
 #  -- At sub-brick #22 'happy_0#0_Tstat' datum type is float:     -7.81449 to       23.1014
 #     statcode = fitt;  statpar = 231
 #  -- At sub-brick #23 'happy_0#1_Coef' datum type is float:      -15.033 to       8.39928
 #  -- At sub-brick #24 'happy_0#1_Tstat' datum type is float:     -14.9242 to       11.0184
 #     statcode = fitt;  statpar = 231
 #  -- At sub-brick #25 'happy_0#2_Coef' datum type is float:     -11.7981 to       5.50927
 #  -- At sub-brick #26 'happy_0#2_Tstat' datum type is float:     -7.17904 to        7.8211
 #     statcode = fitt;  statpar = 231
 #  -- At sub-brick #27 'happy_0#3_Coef' datum type is float:     -35.0001 to       1.88262
 #  -- At sub-brick #28 'happy_0#3_Tstat' datum type is float:     -6.83708 to       10.9671
 #     statcode = fitt;  statpar = 231
 #  -- At sub-brick #29 'happy_0#4_Coef' datum type is float:     -5.76419 to       1.45661
 #  -- At sub-brick #30 'happy_0#4_Tstat' datum type is float:     -6.86098 to       10.7067
 #     statcode = fitt;  statpar = 231
 #  -- At sub-brick #31 'happy_0#5_Coef' datum type is float:     -9.85519 to       1.69674
 #  -- At sub-brick #32 'happy_0#5_Tstat' datum type is float:     -6.67354 to       10.5361
 #     statcode = fitt;  statpar = 231
 #  -- At sub-brick #33 'happy_0#6_Coef' datum type is float:     -18.8469 to       23.7196
 #  -- At sub-brick #34 'happy_0#6_Tstat' datum type is float:     -6.49894 to       7.14007
 #     statcode = fitt;  statpar = 231
 #  -- At sub-brick #35 'happy_0#7_Coef' datum type is float:     -3.47613 to       6.93988
 #  -- At sub-brick #36 'happy_0#7_Tstat' datum type is float:     -7.11908 to       7.11908
 #     statcode = fitt;  statpar = 231
 #  -- At sub-brick #37 'happy_0#8_Coef' datum type is float:     -3.04848 to       21.8188
 #  -- At sub-brick #38 'happy_0#8_Tstat' datum type is float:     -6.86165 to       7.83016
 #     statcode = fitt;  statpar = 231
 #  -- At sub-brick #39 'happy_0#9_Coef' datum type is float:     -3.67314 to         7.717
 #  -- At sub-brick #40 'happy_0#9_Tstat' datum type is float:     -6.78999 to       10.0952
 #     statcode = fitt;  statpar = 231
 #  -- At sub-brick #41 'neutral_0#0_Coef' datum type is float:     -226.253 to       511.279
 #  -- At sub-brick #42 'neutral_0#0_Tstat' datum type is float:     -96.9901 to       13.8589
 #     statcode = fitt;  statpar = 231
 #  -- At sub-brick #43 'neutral_0#1_Coef' datum type is float:     -55.1996 to       29.6612
 #  -- At sub-brick #44 'neutral_0#1_Tstat' datum type is float:     -13.8071 to       113.224
 #     statcode = fitt;  statpar = 231
 #  -- At sub-brick #45 'neutral_0#2_Coef' datum type is float:     -70.5749 to        3.1537
 #  -- At sub-brick #46 'neutral_0#2_Tstat' datum type is float:     -36.2501 to       7.06358
 #     statcode = fitt;  statpar = 231
 #  -- At sub-brick #47 'neutral_0#3_Coef' datum type is float:     -40.3126 to       2.18262
 #  -- At sub-brick #48 'neutral_0#3_Tstat' datum type is float:     -6.17033 to       6.83104
 #     statcode = fitt;  statpar = 231
 #  -- At sub-brick #49 'neutral_0#4_Coef' datum type is float:     -19.8148 to       4.62954
 #  -- At sub-brick #50 'neutral_0#4_Tstat' datum type is float:     -6.62663 to       6.99749
 #     statcode = fitt;  statpar = 231
 #  -- At sub-brick #51 'neutral_0#5_Coef' datum type is float:     -79.9549 to       2.30006
 #  -- At sub-brick #52 'neutral_0#5_Tstat' datum type is float:     -6.32169 to       7.00834
 #     statcode = fitt;  statpar = 231
 #  -- At sub-brick #53 'neutral_0#6_Coef' datum type is float:     -23.6773 to       4.99605
 #  -- At sub-brick #54 'neutral_0#6_Tstat' datum type is float:     -6.28628 to       6.79499
 #     statcode = fitt;  statpar = 231
 #  -- At sub-brick #55 'neutral_0#7_Coef' datum type is float:      -18.635 to       5.65907
 #  -- At sub-brick #56 'neutral_0#7_Tstat' datum type is float:     -6.84543 to       6.85709
 #     statcode = fitt;  statpar = 231
 #  -- At sub-brick #57 'neutral_0#8_Coef' datum type is float:     -4.41194 to        43.156
 #  -- At sub-brick #58 'neutral_0#8_Tstat' datum type is float:     -6.19889 to       6.84051
 #     statcode = fitt;  statpar = 231
 #  -- At sub-brick #59 'neutral_0#9_Coef' datum type is float:     -6.15064 to       22.9785
 #  -- At sub-brick #60 'neutral_0#9_Tstat' datum type is float:     -6.51011 to        7.2583
 #     statcode = fitt;  statpar = 231
 #  -- At sub-brick #61 'object_0#0_Coef' datum type is float:     -154.312 to        341.01
 #  -- At sub-brick #62 'object_0#0_Tstat' datum type is float:     -9.99783 to       9.99783
 #     statcode = fitt;  statpar = 231
 #  -- At sub-brick #63 'object_0#1_Coef' datum type is float:     -45.4806 to       26.4861
 #  -- At sub-brick #64 'object_0#1_Tstat' datum type is float:     -6.89708 to       7.89998
 #     statcode = fitt;  statpar = 231
 #  -- At sub-brick #65 'object_0#2_Coef' datum type is float:     -6.74618 to       11.9222
 #  -- At sub-brick #66 'object_0#2_Tstat' datum type is float:     -5.62015 to       7.21169
 #     statcode = fitt;  statpar = 231
 #  -- At sub-brick #67 'object_0#3_Coef' datum type is float:     -10.4689 to       5.60537
 #  -- At sub-brick #68 'object_0#3_Tstat' datum type is float:     -6.65818 to       6.65818
 #     statcode = fitt;  statpar = 231
 #  -- At sub-brick #69 'object_0#4_Coef' datum type is float:     -10.0915 to       15.4241
 #  -- At sub-brick #70 'object_0#4_Tstat' datum type is float:     -6.10691 to        7.5209
 #     statcode = fitt;  statpar = 231
 #  -- At sub-brick #71 'object_0#5_Coef' datum type is float:     -5.77171 to       6.94347
 #  -- At sub-brick #72 'object_0#5_Tstat' datum type is float:     -6.27678 to       6.71925
 #     statcode = fitt;  statpar = 231
 #  -- At sub-brick #73 'object_0#6_Coef' datum type is float:      -3.5829 to       4.90032
 #  -- At sub-brick #74 'object_0#6_Tstat' datum type is float:     -4.74328 to       6.62142
 #     statcode = fitt;  statpar = 231
 #  -- At sub-brick #75 'object_0#7_Coef' datum type is float:      -2.1945 to       4.85011
 #  -- At sub-brick #76 'object_0#7_Tstat' datum type is float:      -6.3925 to       6.74525
 #     statcode = fitt;  statpar = 231
 #  -- At sub-brick #77 'object_0#8_Coef' datum type is float:     -2.43138 to       20.6229
 #  -- At sub-brick #78 'object_0#8_Tstat' datum type is float:     -5.44289 to        7.0006
 #     statcode = fitt;  statpar = 231
 #  -- At sub-brick #79 'object_0#9_Coef' datum type is float:     -7.65267 to       18.2014
 #  -- At sub-brick #80 'object_0#9_Tstat' datum type is float:     -6.50271 to        6.7476
 #     statcode = fitt;  statpar = 231
