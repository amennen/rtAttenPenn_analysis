# make amygdala average for resting state 

import os
import glob
from shutil import copyfile
import json
import numpy as np
from subprocess import call
import sys
fmriprep_out="/data/jux/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/fmriprep"
reg_save_dir='/data/jux/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/resting/confound_EVs'
trunc_save_dir = '/data/jux/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/resting/trunc'
noise_save_dir = '/data/jux/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/resting/clean'
COMMON_AMYG='/data/jux/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/mni_anat/LAMYG_in_MNI_overlapping.nii.gz' 
# subjects 106,3,107,4,108 got resting state
#subjectNum = 106
subjectNum = np.int(sys.argv[1])
bids_id = 'sub-{0:03d}'.format(subjectNum)
print(bids_id)
sessions = [1,3]
for s in sessions:
        subjectDay = s
        ses_id = 'ses-{0:02d}'.format(subjectDay)
        print(ses_id)
        # get regression file 
        confounds_path = reg_save_dir + '/' + bids_id + '/' + ses_id
        confound_fn = glob.glob(os.path.join(confounds_path, '*.1D'))
        confound_fn = confound_fn[0]

        # get nifti file
        nifti_path = trunc_save_dir + '/' + bids_id + '/' + ses_id
        nifti_fn = glob.glob(os.path.join(nifti_path, '*.nii.gz'))
        nifti_fn = nifti_fn[0]

        # specify where to save cleaned version
        clean_path = noise_save_dir + '/' + bids_id + '/' + ses_id
        preproc_output = "{0}/{1}_{2}_task_rest_glm.nii.gz".format(clean_path,bids_id,ses_id)
        saved_average = "{0}/{1}_{2}_task_rest_LAMYG_avg".format(clean_path,bids_id,ses_id)
        command = ("3dmaskave -quiet -mask {0} {1} > {2}.1D".format(COMMON_AMYG,preproc_output,saved_average))
        call(command,shell=True)

        # now create correlation matrix
        saved_correlation = "{0}/{1}_{2}_task_rest_corr_LAMYG.nii.gz".format(clean_path,bids_id,ses_id)
        command = ("3dfim+ -bucket {0} -fim_thr 0 -out Correlation -ideal_file {1}.1D -input {2}".format(saved_correlation,saved_average,preproc_output))
        call(command,shell=True)

        # transform to z transform
        saved_z = "{0}/{1}_{2}_task_rest_corr_r2z_LAMYG.nii.gz".format(clean_path,bids_id,ses_id)
        command = ("3dcalc -a {0} -expr 'log((1+a)/(1-a))/2' -prefix {1}".format(saved_correlation,saved_z))
        call(command,shell=True)


