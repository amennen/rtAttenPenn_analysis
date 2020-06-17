
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


    neutral_reg = ("-stim_times 1 {0} 'BLOCK(3,1)' -stim_label 1 neutral".format(
                    os.path.join(timing_path, bids_id,ses_id,'neutral.txt'.format(bids_id,ses_id))))

    object_reg = ("-stim_times 2 {0} 'BLOCK(3,1)' -stim_label 2 object".format(
                    os.path.join(timing_path, bids_id,ses_id,'object.txt'.format(bids_id,ses_id))))

    happy_reg = ("-stim_times 3 {0} 'BLOCK(3,1)' -stim_label 3 happy".format(
                    os.path.join(timing_path, bids_id,ses_id,'happy.txt'.format(bids_id,ses_id))))

    fearful_reg = ("-stim_times 4 {0} 'BLOCK(3,1)' -stim_label 4 fearful".format(
                    os.path.join(timing_path, bids_id,ses_id,'fearful.txt'.format(bids_id,ses_id))))

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
                "-mask {8} "
                "-num_glt 2 "
                "-local_times -num_stimts 4 "
                " {3} {4} {5} {6} "
                "-gltsym 'SYM: +happy -neutral' -glt_label 1 'happyvsneut' "
                "-gltsym 'SYM: +fearful -neutral' -glt_label 2 'fearvsneut' "
                "-ortvec {7} "
                "-fout -tout -x1D {9}/{1}/{2}/{1}_{2}_task-faces_glm.X.xmat.1D " # this is the actual design matrix
                "-xjpeg {9}/{1}/{2}/{1}_{2}_task-faces_glm.X.jpg " # this is the design matrix
                "-fitts {9}/{1}/{2}/{1}_{2}_task-faces_glm.fitts " # model prediction - betas * signal
                "-errts {9}/{1}/{2}/{1}_{2}_task-faces.errts " # residuals
                "-bucket {9}/{1}/{2}/{1}_{2}_task-faces_glm.stats".format(run_path,
                    bids_id, ses_id, neutral_reg, object_reg, happy_reg, fearful_reg,full_save_path,whole_brain_mask,analyses_out ))

    call(cmd,shell=True)
    # prints and write to file 3dreml fit command
    # runs glm like this too

    # can use -x1D_stop to say don't bother fitting first, use reml fit only
    with open(os.path.join(output_path, '{0}_{1}_task-faces_glm.REML_cmd'.format(bids_id, ses_id))) as f: 
        reml_cmd = '3dREMLfit' + f.read().split('3dREMLfit')[-1]
    call(reml_cmd, shell=True)

    cmd = ("3dbucket -prefix {0}/{1}_{2}_task-faces_glm_coefs_REML.nii.gz "
                "{0}/{1}_{2}_task-faces_glm.stats_REML+tlrc.BRIK'[1..11(2)]'".format(output_path, bids_id, ses_id))
    call(cmd,shell=True)

    # this makes a nifti file with the following 6 sub-briks:
    # sub-brick 0: neutral
    # sub-brick 1: object
    # sub-brick 2: happy
    # sub-brick 3: feaful
    # sub-brick 4: happy - neut
    # sub-brick 5: negative - neut


