# Purpose: make text file of mean FD -- here for rest but adapt later for other runs

import csv
import numpy as np
import scipy
import matplotlib
import matplotlib.pyplot as plt
#from nilearn import image
#from nilearn.input_data import NiftiMasker
#from nilearn import plotting
import nibabel
#from nilearn.masking import apply_mask
#from nilearn.image import load_img
#from nilearn.image import new_img_like
import numpy as np
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn import datasets, svm, metrics
from sklearn.linear_model import Ridge
from sklearn.svm import SVC, LinearSVC
from sklearn.cross_validation import KFold
from sklearn.cross_validation import LeaveOneLabelOut
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors.nearest_centroid import NearestCentroid
from sklearn.multiclass import OneVsRestClassifier
from sklearn.cross_validation import cross_val_score
from sklearn.cross_validation import StratifiedKFold
from sklearn.metrics import roc_curve, auc, roc_auc_score
from sklearn.feature_selection import SelectFwe
from scipy import signal
from scipy.fftpack import fft, fftshift
from scipy import interp
import seaborn as sns
import pandas as pd
import glob
params = {'legend.fontsize': 'large',
          'figure.figsize': (5, 3),
          'axes.labelsize': 'x-large',
          'axes.titlesize': 'x-large',
          'xtick.labelsize': 'x-large',
          'ytick.labelsize': 'x-large'}
font = {'weight': 'bold',
        'size': 22}
plt.rc('font', **font)
from sklearn.feature_selection import VarianceThreshold
from sklearn.feature_selection import SelectPercentile, f_classif, GenericUnivariateSelect, SelectKBest, chi2
from sklearn.feature_selection import RFE
import os
#import seaborn as sns
import nistats
from nilearn import plotting
from nistats.second_level_model import SecondLevelModel
from nistats.thresholding import map_threshold
from nistats.reporting import get_clusters_table
from nilearn import image

reg_save_dir='/data/jux/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/resting/confound_EVs'
trunc_save_dir = '/data/jux/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/resting/trunc'
noise_save_dir = '/data/jux/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/resting/clean'
FP_mask = '/data/jux/cnds/amennen/rtAttenPenn/MNI_things/Yeo2011_6Network_mask_reoriented_resampled.nii.gz'
FP_mask = '/data/jux/cnds/amennen/rtAttenPenn/MNI_things/Yeo2011_6Network_mask_reoriented_resampled.nii.gz'
COMMON_DIR='/data/jux/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/mni_anat'
common_base = 'dlPFC_in_MNI'
dlPFC_mask = COMMON_DIR + '/' + common_base + '_overlapping' + '.nii.gz'

def getMeanFD_rest(subjectNum,subjectDay):
    fmriprep_out="/data/jux/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/fmriprep"
    ses_id = 'ses-{0:02d}'.format(subjectDay)
    bids_id = 'sub-{0:03d}'.format(subjectNum)
    day_path=os.path.join(fmriprep_out,bids_id,ses_id, 'func')
    fn = glob.glob(os.path.join(day_path, '*task-rest*confounds.tsv'))
    nToDelete = 4
    z = pd.read_csv(fn[0], sep='\t')
    FD = z['FramewiseDisplacement']
    meanFD = np.mean(FD[nToDelete:])
    return meanFD

columns = ['subj', 'FD']
allsubjects = np.array([3,4,5,6,7,8,9,10,11, 106,107,108,109,110,111,112])
nsub = len(allsubjects)
ses = 1
ses_id = 'ses-{0:02d}'.format(ses)

data = []
for s in np.arange(nsub):
    subjectNum=allsubjects[s]
    bids_id = 'sub-{0:03d}'.format(subjectNum)
    meanFD = getMeanFD_rest(subjectNum,1)
    data.append((bids_id,meanFD))

df = pd.DataFrame(data=data,columns=columns)
df.to_csv(os.path.join(noise_save_dir, 'FD_covar_{0}.txt'.format(ses_id)), sep=' ', index=False)











