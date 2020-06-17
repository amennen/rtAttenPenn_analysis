# purpose: use afni 3dttest to threshold differences

import os
import glob
from shutil import copyfile
import pandas as pd
import json
import numpy as np
from subprocess import call
import sys

first_level = '/data/jux/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/afni/first_level/stats'
second_level = '/data/jux/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/afni/group_level/'

FP_mask = '/data/jux/cnds/amennen/rtAttenPenn/MNI_things/Yeo2011_6Network_mask_reoriented_resampled.nii.gz'
COMMON_DIR='/data/jux/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/mni_anat'
dlPFC_mask = '/data/jux/cnds/amennen/rtAttenPenn/MNI_things/mni_GM_ACC_MFG_IFG_intersect.nii.gz'
whole_brain_mask = '/data/jux/cnds/amennen/rtAttenPenn/MNI_things/mni_icbm152_t1_tal_nlin_asym_09c_BOLD_mask_Penn.nii'

BRIK_KEY = {}
BRIK_KEY[0] = 'neutral'
BRIK_KEY[1] = 'object'
BRIK_KEY[2] = 'happy'
BRIK_KEY[3] = 'fearful'
BRIK_KEY[4] = 'happyminusneut'
BRIK_KEY[5] = 'fearfulminusneut'
BRIK = 5

# output of 3dttest
move_to_dir = "{0}/ses-03_minus_ses-01/".format(second_level)
os.chdir(move_to_dir)

# command = ("3dClusterize -inset ses-03_minus_ses-01_stats_{0}_ACC_dlPFC_mask_clustsim_noBLUR.nii.gz ".format(BRIK_KEY[BRIK]) +
#    " -ithr 1 -idat 0 -mask {0} ".format(dlPFC_mask) +
#    "-NN 3 -bisided p=0.001 " +
# #   "-clust_nvox 13 " +
#    "-1Dformat ClusterThr.1D " +
#    "-pref_map ClusterMap.nii.gz")
# call(command,shell=True)

# read in the acf parameters
## WHICH MASK TO INPUT?? choices: whole brain mask/smaller dlpfc maskS
acf_params = "{0}/ses-{1:02d}_minus_ses-{2:02d}_ACF_params.npy".format(move_to_dir,3,1)
params = np.load(acf_params)
a = params[0]
b = params[1]
c = params[2]
command = ("3dClustSim -LOTS -nodec -mask {0} -acf {1} {2} {3} ".format(dlPFC_mask,a,b,c) + 
    " -prefix {0}/3dClustSim_clusterTable_dlPFC ".format(move_to_dir) )
call(command,shell=True)
# command = ("3dClustSim -LOTS -nodec -mask {0} -acf {1} {2} {3} ".format(whole_brain_mask,a,b,c) + 
#     " -prefix 3dClustSim_clusterTable_wb" +
#     )
# call(command,shell=True)