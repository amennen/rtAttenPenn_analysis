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

PROJECT_DIR='/data/jux/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives'
COMMON_DIR='/data/jux/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/mni_anat' # where to save
MNI_DIR = '/data/jux/cnds/amennen/rtAttenPenn/MNI_things'
#mask='LAMYG_in_MNI.nii.gz'
#mask_wb = 'sub-108_ses-03_task-faces_rec-uncorrected_run-01_bold_space-MNI152NLin2009cAsym_brainmask.nii.gz' # for each subject/session

def intersectMasks(mask1,mask2,threshold=1):
    all_masks_list = []
    all_masks_list.append(mask1)
    all_masks_list.append(mask2)
    # threshold = 0 means only the interesection
    common = nilearn.masking.intersect_masks(all_masks_list,threshold,connected=False)
    return common


# now save
mask1 = MNI_DIR + '/' + 'ACC_MFG_IFG_FSL_2mm_bin0p5_resampled.nii.gz'
mask2 = MNI_DIR + '/' + 'mni_GM_thr0p25_bin_resampled.nii.gz'
common = intersectMasks(mask1,mask2)
full_common_path = MNI_DIR + '/' + 'mni_GM_ACC_MFG_IFG_intersect' + '.nii.gz'
common.to_filename(full_common_path)

