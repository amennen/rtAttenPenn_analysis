
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


    neutral_first = ("-stim_times 1 {0} 'BLOCK(3,1)' -stim_label 1 neutral_F".format(
                    os.path.join(timing_path, bids_id,ses_id,'neutral_first.txt'.format(bids_id,ses_id))))
    neutral_last = ("-stim_times 2 {0} 'BLOCK(3,1)' -stim_label 2 neutral_L".format(
                    os.path.join(timing_path, bids_id,ses_id,'neutral_last.txt'.format(bids_id,ses_id))))
    # neutral_carry = ("-stim_times 3 {0} 'BLOCK(3,1)' -stim_label 3 neutral_C".format(
    #                 os.path.join(timing_path, bids_id,ses_id,'neutral_carry.txt'.format(bids_id,ses_id))))
    happy_first = ("-stim_times 3 {0} 'BLOCK(3,1)' -stim_label 3 happy_F".format(
                    os.path.join(timing_path, bids_id,ses_id,'happy_first.txt'.format(bids_id,ses_id))))
    happy_last = ("-stim_times 4 {0} 'BLOCK(3,1)' -stim_label 4 happy_L".format(
                    os.path.join(timing_path, bids_id,ses_id,'happy_last.txt'.format(bids_id,ses_id))))
    # happy_carry = ("-stim_times 6 {0} 'BLOCK(3,1)' -stim_label 6 happy_C".format(
    #                 os.path.join(timing_path, bids_id,ses_id,'happy_carry.txt'.format(bids_id,ses_id))))
    fearful_first = ("-stim_times 5 {0} 'BLOCK(3,1)' -stim_label 5 fearful_F".format(
                    os.path.join(timing_path, bids_id,ses_id,'fearful_first.txt'.format(bids_id,ses_id))))
    fearful_last = ("-stim_times 6 {0} 'BLOCK(3,1)' -stim_label 6 fearful_L".format(
                    os.path.join(timing_path, bids_id,ses_id,'fearful_last.txt'.format(bids_id,ses_id))))
    # fearful_carry = ("-stim_times 9 {0} 'BLOCK(3,1)' -stim_label 9 fearful_C".format(
    #                 os.path.join(timing_path, bids_id,ses_id,'fearful_carry.txt'.format(bids_id,ses_id))))
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
                "-mask {10} "
                "-num_glt 7 "
                "-local_times -num_stimts 6 "
                " {3} {4} {5} {6} {7} {8} "
                "-gltsym 'SYM: +happy_L -happy_F' -glt_label 1 'happyLvF' "
                "-gltsym 'SYM: +fearful_L -fearful_F' -glt_label 2 'fearfulLvF' "
                "-gltsym 'SYM: +fearful_L -neutral_L' -glt_label 3 'fearfulvneutralL' "
                "-gltsym 'SYM: +fearful_L -neutral_L' -glt_label 4 'fearfulvneutralL' "
                "-gltsym 'SYM: +fearful_F -neutral_F' -glt_label 5 'fearfulvneutralF' "
                "-gltsym 'SYM: +happy_F -neutral_F' -glt_label 6 'happyvneutralF' "
                "-gltsym 'SYM: +happy_L -neutral_L' -glt_label 7 'happyvneutralL' "
                "-ortvec {9} -fout -tout "
                "-x1D {11}/{1}/{2}/{1}_{2}_task-faces_glm_separate_xmat.1D "
                "-bucket {11}/{1}/{2}/{1}_{2}_task-faces_glm_separate.stats ".format(run_path, 
                    bids_id, ses_id,neutral_first, neutral_last,happy_first,happy_last,fearful_first,fearful_last,full_save_path,whole_brain_mask,analyses_out))

    call(cmd,shell=True)
    # prints and write to file 3dreml fit command
    # runs glm like this too

    # can use -x1D_stop to say don't bother fitting first, use reml fit only
    with open(os.path.join(output_path, '{0}_{1}_task-faces_glm_separate.REML_cmd'.format(bids_id, ses_id))) as f: 
        reml_cmd = '3dREMLfit' + f.read().split('3dREMLfit')[-1]
    call(reml_cmd, shell=True)

    cmd = ("3dbucket -prefix {0}/{1}_{2}_task-faces_glm_coefs_separate_REML.nii.gz "
                "{0}/{1}_{2}_task-faces_glm_separate.stats_REML+tlrc.BRIK'[1..25(2)]'".format(output_path, bids_id, ses_id))
    call(cmd,shell=True)

    # this makes a nifti file with the following 13 sub-briks:
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

# fearful L - neutral L happens twice but oh well

