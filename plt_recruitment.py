# plot recruitment numbers for penn
# shown are the number of people who consented to the study (not who qualified/continued the study)

import os
import glob
from shutil import copyfile
import pandas as pd
import json
import numpy as np
from subprocess import call
import time
import logging
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s:%(asctime)s - %(message)s')
import numpy as np
import pickle
import nibabel as nib
import nilearn
from nilearn.image import resample_to_img
import matplotlib.pyplot as plt
from nilearn import plotting
from nilearn.plotting import show
from nilearn.plotting import plot_roi
from nilearn import image
from nilearn.masking import apply_mask
# get_ipython().magic('matplotlib inline')
import scipy
import matplotlib
import matplotlib.pyplot as plt
from nilearn import image
from nilearn.input_data import NiftiMasker
#from nilearn import plotting
import nibabel
from nilearn.masking import apply_mask
from nilearn.image import load_img
from nilearn.image import new_img_like
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
import csv
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
import seaborn as sns
import pandas as pd
import csv
from scipy import stats
import sys
from sklearn.utils import shuffle
import random
from datetime import datetime
import nilearn
random.seed(datetime.now())
from nilearn.image import new_img_like
import scipy.stats as sstats  # type: ignore

months_scanned = ['4/18','5/18', '6/18', '7/18', '8/18', '9/18', '10/18', '11/18', '12/18', '1/19', '2/19', '3/19', '4/19']
n_MDD = [0,0,0,3,4,4,2,1,1,1,1,1,0]
n_HC =  [1,2,0,0,0,0,0,0,0,1,1,1,1]
n_months = len(n_MDD)
plt.figure()
plt.plot(np.arange(n_months),n_MDD, color='r', marker='.', label='MDD')
plt.plot(np.arange(n_months),n_HC, color='k', marker='.', label='HC')
plt.title('# Subjects constented by month')
plt.xticks(np.arange(n_months), months_scanned)
plt.xlabel('Month')
plt.ylabel('# Consented')
plt.legend()
plt.show()