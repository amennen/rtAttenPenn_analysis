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
import os
#import seaborn as sns
import nistats
from nilearn import plotting
from nistats.second_level_model import SecondLevelModel
from nistats.thresholding import map_threshold
from nistats.reporting import get_clusters_table
from nilearn import image


cf_dir = '/data/jux/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/fsl/first_level/confound_EVs'
second_level = '/data/jux/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/afni/group_level/'
def getMeanFD_faces(subjectNum,subjectDay):
    # here we have to do for each run
    ses_id = 'ses-{0:02d}'.format(subjectDay)
    bids_id = 'sub-{0:03d}'.format(subjectNum)
    cf_dir = '/data/jux/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/fsl/first_level/confound_EVs'
    confounds_dir = cf_dir + '/' + bids_id + '/' + ses_id
    confounds_fn = confounds_dir + '/' + bids_id + '_' + ses_id + '_' + 'task-faces_rec-uncorrected_COMBINED_bold_confounds.1D'
    z = pd.read_csv(confounds_fn, sep='\t',header=None)
    meanFD = np.mean(z[0])
    return meanFD

columns = ['subj', 'FD']
allsubjects = np.array([1,2,3,4,5,6,7,8, 9,10,11,101,102,103,104,105,106,107,108,109,110,111,112,113,114])
nsub = len(allsubjects)
sessions = [1,3]
for ses in sessions:
  ses_id = 'ses-{0:02d}'.format(ses)

  data = []
  for s in np.arange(nsub):
      subjectNum=allsubjects[s]
      bids_id = 'sub-{0:03d}'.format(subjectNum)
      meanFD = getMeanFD_faces(subjectNum,ses)
      data.append((bids_id,meanFD))

  df = pd.DataFrame(data=data,columns=columns)
  df.to_csv(os.path.join(second_level, 'FD_covar_{0}.txt'.format(ses_id)), sep=' ', index=False)


# now make average FD too
data = []
for s in np.arange(nsub):
  subjectNum = allsubjects[s]
  bids_id = 'sub-{0:03d}'.format(subjectNum)
  meanFD1 = getMeanFD_faces(subjectNum,1)
  meanFD2 = getMeanFD_faces(subjectNum,3)
  avg_FD = np.mean([meanFD1,meanFD2])
  data.append((bids_id,avg_FD))
df = pd.DataFrame(data=data,columns=columns)
df.to_csv(os.path.join(second_level, 'FD_covar_SES_mean.txt'), sep=' ', index=False)





