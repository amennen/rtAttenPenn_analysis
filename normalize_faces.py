# PURPOSE: normalize all facs runs --> afni

import os
import glob
from shutil import copyfile
import json
import numpy as np
from subprocess import call
import sys
import scipy.stats
import nibabel as nib
import nilearn
from nilearn import image

fmriprep_out="/data/jux/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/fmriprep"
task_path = '/data/jux/cnds/amennen/rtAttenPenn/fmridata/behavdata/faces'
save_path = '/data/jux/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/afni/first_level/normalized_runs'

# BEFORE YOU DO ANYTHING SMOOTH THE DATA!
fwhm = 6
subjectNum = np.int(sys.argv[1])
bids_id = 'sub-{0:03d}'.format(subjectNum)
print(bids_id)
sessions = [1,3]
nRuns = 2
n_TR_to_delete = 5
for s in sessions:
        subjectDay = s
        ses_id = 'ses-{0:02d}'.format(subjectDay)
        print(ses_id)
        day_path=os.path.join(fmriprep_out,bids_id,ses_id, 'func')
        for r in np.arange(nRuns):
            faces_nifti_fn = glob.glob(os.path.join(day_path,'*task-faces_rec-uncorrected_run-0{0}_bold_space-MNI*preproc*'.format(r+1)))
            faces_nifti = faces_nifti_fn[0]
            smoothed_nifti = nilearn.image.smooth_img(faces_nifti, fwhm)
            #file_object = nib.load(faces_nifti)
            faces_data = smoothed_nifti.get_fdata()
            # so this outputs to 65 x 77 x 65 x 147

            # remove first 5 TRs, then score and save 
            faces_nifti_removed = faces_data[:,:,:,n_TR_to_delete:]
            zscored_data = scipy.stats.zscore(faces_nifti_removed,axis=3)
            zscored_data = np.nan_to_num(zscored_data)
            # now save nifti

            NAMETOSAVE = os.path.split(faces_nifti)[-1]
            dest_path = save_path + '/' + bids_id + '/' + ses_id
            if not os.path.exists(dest_path):
                os.makedirs(dest_path)
            full_save_path = os.path.join(dest_path, NAMETOSAVE)

            # get old header
            new_header = header=smoothed_nifti.header.copy()
            new_header['dim'][4] = header['dim'][4] - n_TR_to_delete
            new_img = nib.Nifti1Image(zscored_data, smoothed_nifti.affine, new_header)

            # create nifti object
            new_img.to_filename(full_save_path)





