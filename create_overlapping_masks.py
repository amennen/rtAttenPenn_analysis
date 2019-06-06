# purpose: create overlapping masks

# function with the following inputs
# 1 - array of all subjects to create a merged mask with
# 2 - name of the file (will default to session 1/3 of bids directory) 
# -- take them in and arguments to parse--sys.argv
import os
import glob
import argparse
import numpy as np  # type: ignore
import sys
# Add current working dir so main can be run from the top level rtAttenPenn directory
sys.path.append(os.getcwd())
from sklearn.model_selection import KFold
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
import matplotlib
import matplotlib.pyplot as plt
import scipy
import nilearn.masking

mask = sys.argv[1]
PROJECT_DIR='/data/jag/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives'
COMMON_DIR='/data/jag/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/mni_anat' # where to save
#mask='LAMYG_in_MNI.nii.gz'
#mask_wb = 'sub-108_ses-03_task-faces_rec-uncorrected_run-01_bold_space-MNI152NLin2009cAsym_brainmask.nii.gz' # for each subject/session


subjects = np.array([1,2,3,4,5,101,102,103,104,105,106, 107,108])
nsubs = len(subjects)

all_masks_list = []
# first make a list of all nifti masks to create overlapping mask
for s in np.arange(nsubs):
    bids_id = 'sub-{0:03d}'.format(subjects[s])
    for ses in np.array([1,3]):
        ses_id = 'ses-{0:02d}'.format(ses)
        subject_mask = PROJECT_DIR + '/' + 'fmriprep' + '/' + bids_id + '/' + ses_id + '/' + 'func' + '/' + mask
        all_masks_list.append(subject_mask)


common = nilearn.masking.intersect_masks(all_masks_list, threshold=1, connected=True)

# 26 voxels total
# now save
common_base = mask.split('.')[0]
full_common_path = COMMON_DIR + '/' + common_base + '_overlapping' + '.nii.gz'
common.to_filename(full_common_path)
