# purpose: calculate resting state connectivity matrix

# start with loading in resting state data, power mask


import glob
import pandas as pd
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
random.seed(datetime.now())
from nilearn.image import new_img_like
import scipy.stats as sstats  # type: ignore
from nilearn.input_data import NiftiLabelsMasker
from nilearn.connectome import ConnectivityMeasure
from statsmodels.formula.api import ols
import statsmodels.api as sm
import statsmodels
from statsmodels.stats.anova import AnovaRM


powerAtlas = '/data/jag/cnds/amennen/Power/power264MNI_resampled.nii.gz'
noise_save_dir = '/data/jux/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/resting/clean'
def calculateWithinConnectivity(networkName,correlation_matrix,fullDF,systemDF,all_good_ROI):
	# find DMN labels
	this_ROI = fullDF.ROI[systemDF==networkName].values.astype(int) 
	# now convert this to the indices
	this_ROI_indices_in_matrix = np.where(np.in1d(all_good_ROI,this_ROI))[0]
	if networkName == 'Sensory/somatomotor Hand':
		# concatenate other one
		other_SMN = fullDF.ROI[systemDF=='Sensory/somatomotor Mouth'].values.astype(int) 
		other_SMN_indices_in_matrix = np.where(np.in1d(all_good_ROI,other_SMN))[0]
		this_ROI_indices_in_matrix = np.concatenate((this_ROI_indices_in_matrix,other_SMN_indices_in_matrix))
	x,y = np.meshgrid(this_ROI_indices_in_matrix,this_ROI_indices_in_matrix)
	# need to figure this out!!!
	this_ROI_correlations = correlation_matrix[x,y]
	n_nodes = len(this_ROI)
	#### CHECK WITH MEICHEN WITH IF THIS IS THE MEAN FIRST OR JUST SUMMING ###
	within_ROI_sum = np.nansum(this_ROI_correlations)/2 # dividing by 2 because will be double the off-diagonal values
	within_ROI_mean = within_ROI_sum/np.square(n_nodes)
	#within_ROI_mean = np.nanmean(this_ROI_correlations)/np.square(n_nodes)
	return within_ROI_mean

# for one versus all
def calculateOneVsAllConnectivity(networkName,correlation_matrix,fullDF,systemDF,all_good_ROI):
	this_ROI = fullDF.ROI[systemDF==networkName].values.astype(int) 
	this_ROI_indices_in_matrix = np.where(np.in1d(all_good_ROI,this_ROI))[0]
	if networkName == 'Sensory/somatomotor Hand':
		# concatenate other one
		other_SMN = fullDF.ROI[systemDF=='Sensory/somatomotor Mouth'].values.astype(int) 
		other_SMN_indices_in_matrix = np.where(np.in1d(all_good_ROI,other_SMN))[0]
		this_ROI_indices_in_matrix = np.concatenate((this_ROI_indices_in_matrix,other_SMN_indices_in_matrix))
	all_other_indices_in_matrix = [x for x in np.arange(len(all_good_ROI)) if x not in this_ROI_indices_in_matrix]
	x,y = np.meshgrid(this_ROI_indices_in_matrix,all_other_indices_in_matrix)
	# this time we're not dividing by 2 because all x values are ROI 1 and all y values are ROI 2
	across_ROI_correlations = correlation_matrix[x,y]
	n_nodes_this_network = len(this_ROI)
	n_nodes_all_others = len(all_other_indices_in_matrix)
	across_ROI_sum = np.nansum(across_ROI_correlations)
	across_ROI_mean = across_ROI_sum/(n_nodes_this_network*n_nodes_all_others)
	return across_ROI_mean

def calculatePairwiseConnectivity(networkA,networkB,correlation_matrix,fullDF,systemDF,all_good_ROI):
	A_ROI = fullDF.ROI[systemDF==networkA].values.astype(int) 
	A_ROI_indices_in_matrix = np.where(np.in1d(all_good_ROI,A_ROI))[0]
	if networkA == 'Sensory/somatomotor Hand':
		# concatenate other one
		other_SMN = fullDF.ROI[systemDF=='Sensory/somatomotor Mouth'].values.astype(int) 
		other_SMN_indices_in_matrix = np.where(np.in1d(all_good_ROI,other_SMN))[0]
		A_ROI_indices_in_matrix = np.concatenate((A_ROI_indices_in_matrix,other_SMN_indices_in_matrix))
	B_ROI = fullDF.ROI[systemDF==networkB].values.astype(int) 
	B_ROI_indices_in_matrix = np.where(np.in1d(all_good_ROI,B_ROI))[0]
	if networkB == 'Sensory/somatomotor Hand':
		# concatenate other one
		other_SMN = fullDF.ROI[systemDF=='Sensory/somatomotor Mouth'].values.astype(int) 
		other_SMN_indices_in_matrix = np.where(np.in1d(all_good_ROI,other_SMN))[0]
		B_ROI_indices_in_matrix = np.concatenate((B_ROI_indices_in_matrix,other_SMN_indices_in_matrix))
	x,y = np.meshgrid(A_ROI_indices_in_matrix,B_ROI_indices_in_matrix)
	# not dividing by 2 again because again ROI 1 is x and ROI 2 is y so we're not double counting anything
	across_ROI_correlations = correlation_matrix[x,y]
	n_nodes_A = len(A_ROI)
	n_nodes_B = len(B_ROI)
	across_ROI_sum = np.nansum(across_ROI_correlations)
	across_ROI_mean = across_ROI_sum/(n_nodes_A*n_nodes_B)
	return across_ROI_mean

# put in check wher eif the std of any voxels in ROI = 0, then skip that vox
nROI = 264
labelsFile = '/data/jag/cnds/amennen/Power/Neuron_consensus_264.csv'
z = pd.read_csv(labelsFile)
complete_labels=z[1:]
ROI = complete_labels['ROI']
system = complete_labels['Suggested System']
all_systems = np.unique(system)
systems_to_keep = ['Default mode','Fronto-parietal Task Control', 
				 'Visual','Subcortical', 'Cingulo-opercular Task Control',  'Salience', 'Ventral attention','Dorsal attention',
				 'Auditory','Sensory/somatomotor Hand', 'Sensory/somatomotor Mouth']
# combine the two sennsory/somatomotor 
n_systems = len(systems_to_keep) - 1
# here we get the ROIs that have each of the labels we don't want
# then we subtract 1 to go to python indices
systems_to_remove = ['Uncertain', 'Cerebellar', 'Memory retrieval?']
systems_to_keep_abbrv = ['DMN', 'FPN', 'VIS', 'SUB', 'CON', 'SAN', 'VAN', 'DAN', 'AUD','SMN']

all_cer_labels = complete_labels.ROI[system=='Cerebellar'].values.astype(int) - 1
all_mem_labels = complete_labels.ROI[system=='Memory retrieval?'].values.astype(int) - 1
all_uncertain_labels = complete_labels.ROI[system=='Uncertain'].values.astype(int) - 1 # go from label to python index
all_bad_labels = np.concatenate((all_cer_labels,all_mem_labels,all_uncertain_labels),axis=0)
# left with 227 regions like beginning of Meichen's (removed the rest for bad signals)
all_network_ind = np.arange(nROI)
all_good_labels = [x for x in all_network_ind if x not in all_bad_labels]
all_good_ROI = np.array(all_good_labels) + 1 # puts as ROI labels so we can find the specific regions we want
nROI_good = len(all_good_labels)

subjects = np.array([3,4,5,6,7,8,9,10,11,106,107,108,109,110,111,112,113])
nSub = len(subjects)
HC_ind = np.argwhere(subjects<100)[:,0]
MDD_ind = np.argwhere(subjects>100)[:,0]
sessions = [1,3]
nDays = len(sessions)
average_within_mat = np.zeros((n_systems,n_systems,nSub,nDays))
average_one_vs_all = np.zeros((n_systems,nSub,nDays))
# NOW CALCULATE DATA FOR SUBJECTS
for s in np.arange(nSub):
	subjectNum=subjects[s]
	bids_id = 'sub-{0:03d}'.format(subjectNum)
	for ses in np.arange(nDays):
		subjectDay=sessions[ses]
		ses_id = 'ses-{0:02d}'.format(subjectDay)
		clean_path = noise_save_dir + '/' + bids_id + '/' + ses_id
		cleaned_image = '{0}/{1}_{2}_task_rest_glm.nii.gz'.format(clean_path,bids_id,ses_id)

		cleaned_image_data = nib.load(cleaned_image).get_fdata()
		# doing standardize = True here at least makes it so voxels outside of brain would have 0 std and not be included
		masker = NiftiLabelsMasker(labels_img=powerAtlas, standardize=True,
		                           memory='nilearn_cache', verbose=5)
		time_series = masker.fit_transform(cleaned_image) # now data is n time points x 264 nodes
		time_series_good_labels = time_series[:,all_good_labels] # now data is in n time points x 227 nodes
		correlation_measure = ConnectivityMeasure(kind='correlation')
		correlation_matrix = correlation_measure.fit_transform([time_series_good_labels])[0] # takes correlation for all 227 nodes
		np.fill_diagonal(correlation_matrix,np.nan) # to make sure you don't get the same node in the within connectivity difference
		for row in np.arange(n_systems):
			for col in np.arange(n_systems):
				if row == col: # diagonal
					average_within_mat[row,col,s,ses] = calculateWithinConnectivity(systems_to_keep[row],correlation_matrix,complete_labels,system,all_good_ROI)
				else:
					average_within_mat[row,col,s,ses] = calculatePairwiseConnectivity(systems_to_keep[row],systems_to_keep[col],correlation_matrix,complete_labels,system,all_good_ROI)
			# now calculate oneVsAll
			average_one_vs_all[row,s,ses] = calculateOneVsAllConnectivity(systems_to_keep[row],correlation_matrix,complete_labels,system,all_good_ROI)


# NEXT STEPS: average by HC or MDD - do separately for 1 vs. 3 before subtracting
avg_HC_1 = np.mean(average_within_mat[:,:,HC_ind,0],axis=2)
avg_HC_2 = np.mean(average_within_mat[:,:,HC_ind,1],axis=2)
avg_MDD_1 = np.mean(average_within_mat[:,:,MDD_ind,0],axis=2)
avg_MDD_2 = np.mean(average_within_mat[:,:,MDD_ind,1],axis=2)
diff_1 = avg_MDD_1 - avg_HC_1
diff_2 = avg_MDD_2 - avg_HC_2
avg_oneVsAll_HC_1 = np.mean(average_one_vs_all[:,HC_ind,0],axis=1)
avg_oneVsAll_HC_2 = np.mean(average_one_vs_all[:,HC_ind,1],axis=1)
avg_oneVsAll_MDD_1 = np.mean(average_one_vs_all[:,MDD_ind,0],axis=1)
avg_oneVsAll_MDD_2 = np.mean(average_one_vs_all[:,MDD_ind,1],axis=1)

# plot within by 1 vs all


alignment = {'horizontalalignment': 'center', 'verticalalignment': 'baseline'}
plt.figure(figsize=(20,20))
plt.subplot(221)
plt.plot(np.diagonal(avg_HC_1),avg_oneVsAll_HC_1, '.',ms=10)
for systemInd in np.arange(n_systems):
	plt.text(np.diagonal(avg_HC_1)[systemInd],avg_oneVsAll_HC_1[systemInd], systems_to_keep_abbrv[systemInd], size='xx-small',weight='light', **alignment)
plt.ylim([-.1, .1])
plt.xlim([0,0.2])
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
plt.xlabel('Within network connectivity',fontsize=10)
plt.ylabel('One-vs-all connectivity',fontsize=10)
plt.title('HC 1',fontsize=10)
plt.subplot(222)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
plt.plot(np.diagonal(avg_HC_2),avg_oneVsAll_HC_2, '.',ms=10)
for systemInd in np.arange(n_systems):
	plt.text(np.diagonal(avg_HC_2)[systemInd],avg_oneVsAll_HC_2[systemInd], systems_to_keep_abbrv[systemInd], size='xx-small',weight='light', **alignment)
plt.ylim([-.1, .1])
plt.xlim([0,0.2])
plt.xlabel('Within network connectivity',fontsize=10)
plt.ylabel('One-vs-all connectivity',fontsize=10)
plt.title('HC 2',fontsize=10)
plt.subplot(223)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
plt.plot(np.diagonal(avg_MDD_1),avg_oneVsAll_MDD_1, '.',ms=10)
for systemInd in np.arange(n_systems):
	plt.text(np.diagonal(avg_MDD_1)[systemInd],avg_oneVsAll_MDD_1[systemInd], systems_to_keep_abbrv[systemInd], size='xx-small',weight='light', **alignment)
plt.ylim([-.1, .1])
plt.xlim([0,0.2])
plt.xlabel('Within network connectivity',fontsize=10)
plt.ylabel('One-vs-all connectivity',fontsize=10)
plt.title('MDD 1',fontsize=10)
plt.subplot(224)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
plt.plot(np.diagonal(avg_MDD_2),avg_oneVsAll_MDD_2, '.',ms=10)
for systemInd in np.arange(n_systems):
	plt.text(np.diagonal(avg_MDD_2)[systemInd],avg_oneVsAll_MDD_2[systemInd], systems_to_keep_abbrv[systemInd], size='xx-small',weight='light', **alignment)
plt.ylim([-.1, .1])
plt.xlim([0,0.2])
plt.xlabel('Within network connectivity',fontsize=10)
plt.ylabel('One-vs-all connectivity',fontsize=10)
plt.title('MDD 2',fontsize=10)

plt.show()





vmin=-0.5
vmax=0.5

plt.subplot(121)
plt.imshow(diff_1,vmin=vmin,vmax=vmax,cmap='coolwarm')
plt.title('MDD - HC 1')
plt.colorbar()
plt.xticks(np.arange(n_systems),systems_to_keep_abbrv,fontsize=5)
plt.yticks(np.arange(n_systems),systems_to_keep_abbrv,fontsize=5)
plt.subplot(122)
plt.imshow(diff_2,vmin=vmin,vmax=vmax,cmap='coolwarm')
plt.title('MDD - HC 2')
plt.colorbar()
plt.xticks(np.arange(n_systems),systems_to_keep_abbrv,fontsize=5)
plt.yticks(np.arange(n_systems),systems_to_keep_abbrv,fontsize=5)

plt.show()

plt.subplot(221)
plt.imshow(avg_HC_1,vmin=vmin,vmax=vmax,cmap='coolwarm')
plt.title('HC 1')
plt.colorbar()
plt.xticks(np.arange(n_systems),systems_to_keep_abbrv,fontsize=5)
plt.yticks(np.arange(n_systems),systems_to_keep_abbrv,fontsize=5)
plt.subplot(222)
plt.imshow(avg_HC_2,vmin=vmin,vmax=vmax,cmap='coolwarm')
plt.title('HC 2')
plt.colorbar()
plt.xticks(np.arange(n_systems),systems_to_keep_abbrv,fontsize=5)
plt.yticks(np.arange(n_systems),systems_to_keep_abbrv,fontsize=5)
plt.subplot(223)
plt.imshow(avg_MDD_1,vmin=vmin,vmax=vmax,cmap='coolwarm')
plt.xticks(np.arange(n_systems),systems_to_keep_abbrv,fontsize=5)
plt.yticks(np.arange(n_systems),systems_to_keep_abbrv,fontsize=5)
plt.title('MDD 1')
plt.colorbar()
plt.subplot(224)
plt.imshow(avg_MDD_2,vmin=vmin,vmax=vmax,cmap='coolwarm')
plt.title('MDD 2')
plt.colorbar()
plt.xticks(np.arange(n_systems),systems_to_keep_abbrv,fontsize=5)
plt.yticks(np.arange(n_systems),systems_to_keep_abbrv,fontsize=5)
plt.show()


# last thing: for given row,col in matrix, plot bargraph of differences by day

system = 0
row=system
col=row
linestyles = ['-', ':']
colors=['k', 'r']
nVisits = 2

fig = plt.figure(figsize=(10,7))
# plot for each subject
for s in np.arange(nSub):
	if subjects[s] < 100:
		style = 0
		plt.plot(np.arange(nVisits),average_within_mat[row,col,s,:],marker='.', ms=20,color=colors[style],alpha=0.5)
	else:
		style = 1
		plt.plot(np.arange(nVisits),average_within_mat[row,col,s,:], marker='.',ms=20,color=colors[style],alpha=0.5)
plt.errorbar(np.arange(nVisits),np.nanmean(average_within_mat[row,col,HC_ind,:],axis=0),lw = 5,color=colors[0],yerr=scipy.stats.sem(average_within_mat[row,col,HC_ind,:],axis=0,nan_policy='omit'), label='HC')
plt.errorbar(np.arange(nVisits),np.nanmean(average_within_mat[row,col,MDD_ind,:],axis=0),lw = 5,color=colors[1],yerr=scipy.stats.sem(average_within_mat[row,col,MDD_ind,:],axis=0,nan_policy='omit'), label='MDD')
plt.xticks(np.arange(nVisits),('Pre NF', 'Post NF'))
plt.xlabel('Visit')
plt.title('Row %i Col %i' % (row,col))
plt.title('%s Within-Network Connectivity'% systems_to_keep_abbrv[system])
plt.legend()
plt.show()
# now test significance
print('FIRST DAY')
print(scipy.stats.ttest_ind(average_within_mat[row,col,HC_ind,0],average_within_mat[row,col,MDD_ind,0]))
print('LAST DAY')
print(scipy.stats.ttest_ind(average_within_mat[row,col,HC_ind,1],average_within_mat[row,col,MDD_ind,1]))

# now get the specific ROI values for each network that you want to compute
# IMPORTANT: MAKE ANY CORRELATION MATRIX HAVE NAN DIAGNOALS BEFORE YOU PASS INTO FUNCTION!!

#### FOR POSTER: look at just DMN first
DMN_connectivity = average_within_mat[0,0,:,:].flatten() # nsubs x ndays --> flattens to s1 day 1 s1 day 2 s2 day 1 s2 day 2
FPN_connectivity =  average_within_mat[1,1,:,:].flatten()
DAN_connectivity =  average_within_mat[7,7,:,:].flatten()
CON_connectivity =  average_within_mat[4,4,:,:].flatten()
SAN_connectivity =  average_within_mat[5,5,:,:].flatten()

ndays=2
day = np.tile(np.arange(ndays),nSub)
subject = np.repeat(subjects,ndays)
groups = ['HC' if i in HC_ind else 'MDD' for i in np.arange(nSub)]
groups = np.repeat(groups,ndays)
DATA = {}
DATA['DMN_connectivity'] = DMN_connectivity
DATA['FPN_connectivity'] = FPN_connectivity
DATA['DAN_connectivity'] = DAN_connectivity
DATA['CON_connectivity'] = CON_connectivity
DATA['SAN_connectivity'] = SAN_connectivity

DATA['day'] = day
DATA['subject'] = subject
DATA['groups'] = groups
df = pd.DataFrame.from_dict(DATA)
plt.figure()
sns.barplot(data=df,x='day',y='DMN_connectivity',hue='groups',ci=68,palette=['k','r'],alpha=0.5)
plt.title('DMN connectivity changes')
plt.ylabel('DMN Within Connectivity')
plt.show()
scipy.stats.ttest_ind(average_within_mat[0,0,HC_ind,0],average_within_mat[0,0,MDD_ind,0]) # for 1-sided t-test the p-values would be 0.17
model = ols('DMN_connectivity ~ groups*day',data=df).fit()
model.summary()

plt.figure()
sns.barplot(data=df,x='day',y='FPN_connectivity',hue='groups',ci=68,palette=['k','r'],alpha=0.5)
plt.title('FPN connectivity changes')
plt.ylabel('FPN Within Connectivity')
plt.show()

plt.figure()
sns.barplot(data=df,x='day',y='SAN_connectivity',hue='groups',ci=68,palette=['k','r'],alpha=0.5)
plt.show()
# Plot the correlation matrix
# Make a large figure
# Mask the main diagonal for visualization:
#np.fill_diagonal(correlation_matrix, 0)
# The labels we have start with the background (0), hence we skip the
# first label
# matrices are ordered for block-like representation
#plotting.plot_matrix(correlation_matrix, figure=(10, 8),
#                     vmax=1, vmin=-1)
#plt.show()

# default mode, salience, dorsal attention within and across
# FROM Yvette - do correlation first, then try wavelet and see if it makes a difference
# left off in the middle-- indexing from ROI is off if you change the matrix then
# TO DO: now do the same thing but calculate across other networks



# figure out simplest way to do this

