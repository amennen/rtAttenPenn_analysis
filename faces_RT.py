# purpose: go through given subject ID and get behavior to calculate bias for each day
# negative bias for that day RT_neutral - RT_fearful [so that more positive means they're faster at negative-->more negatively biased]--more positive = more sad
# anti-positive bias: log(RT_positive - RT_neutral) --> more positive-->more slow at positive-->more positive = less  happy
import logging
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s:%(asctime)s - %(message)s')

import numpy as np
import nibabel
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
import seaborn as sns
import sys
from sklearn.utils import shuffle
import random
import glob

project_dir = '/data/jag/cnds/amennen/rtAttenPenn/fmridata/behavdata/faces/'
RUN=0
TRIAL = 4
CONDITION=5
RT=17
ndays=2
#######
ID_LIST  = ['RT002', 'RT003', 'RT008', 'RT009', 'RT013', 'RT014', 'RT015', 'RT018', 'RT020']
subjects = np.array([1,2,101,102,103,104,105,106,3])
HC_ind = np.argwhere(subjects<100)[:,0]
MDD_ind = np.argwhere(subjects>100)[:,0]
nsubjects = len(ID_LIST)
########
all_sadbias = np.zeros((nsubjects,ndays))
all_happybias = np.zeros((nsubjects,ndays))
for s in np.arange(nsubjects):
	ID = ID_LIST[s]
	NUMBER = SUBJECT_LIST[s]
	for d in np.arange(ndays):
		day = d + 1

		happy_RT = []
		neutral_RT = []
		fear_RT = []

		file_name = glob.glob(project_dir + ID + '/' + ID + '_Day' + str(day) + '_Scanner' + '*.csv')
		print(file_name[0])
		with open(file_name[0]) as csv_file:
			csv_reader = csv.reader(csv_file, delimiter=',')
			line_count = 0
			for row in csv_reader:
				#print(row)
				#print(row[CONDITION])
				#print(row[RT])
				#this_run = row[RUN]
				if row[0] == 'A' or row[0] == 'B': # loop only through trial rows
					this_condition = row[CONDITION]
					this_RT = row[RT]
					if this_condition == 'Happy':
					#	print(this_RT)
						if this_RT:
							happy_RT.append(np.float64(this_RT))
					elif this_condition == 'Fearful':
					#	print(this_RT)
						if this_RT:
							fear_RT.append(np.float64(this_RT))
					elif this_condition == 'Neutral':
					#	print(this_RT)
						if this_RT:
							neutral_RT.append(np.float64(this_RT))


		all_sadbias[s,d] = np.mean(neutral_RT) - np.mean(fear_RT)
		all_happybias[s,d] = np.mean(happy_RT) - np.mean(neutral_RT)


# now plot how it changes over time for each group
colors=['k', 'r']
lw = 1
alpha=1
ind = np.arange(2) + 1
fig, ax = plt.subplots(figsize=(12,7))
for s in np.arange(nsubjects):
	if subjects[s] < 100:
		c = 0
	else:
		c = 1
	plt.plot(ind,all_sadbias[s,:], '--',color=colors[c],linewidth=lw)
plt.plot(ind,np.mean(all_sadbias[HC_ind,:],axis=0),lw=5,alpha=alpha,label='HC', color='k')
plt.plot(ind,np.mean(all_sadbias[MDD_ind,:],axis=0),lw=5,alpha=alpha,label='MDD', color='r')
plt.title('Sad bias RT')
plt.ylabel('RT neutral - RT sad')
ax.set_xticks(ind)
ax.set_xticklabels(['Day 1','Day 2'])
plt.legend()
plt.show()

fig, ax = plt.subplots(figsize=(12,7))
for s in np.arange(nsubjects):
	if subjects[s] < 100:
		c = 0
	else:
		c = 1
	plt.plot(ind,all_happybias[s,:], '--',color=colors[c],linewidth=lw)
plt.plot(ind,np.mean(all_happybias[HC_ind,:],axis=0),lw=5,alpha=alpha,label='HC', color='k')
plt.plot(ind,np.mean(all_happybias[MDD_ind,:],axis=0),lw=5,alpha=alpha,label='MDD', color='r')
plt.title('Antihappy bias RT')
plt.ylabel('RT happy - RT happy')
ax.set_xticks(ind)
ax.set_xticklabels(['Day 1','Day 2'])
plt.legend()
plt.show()














