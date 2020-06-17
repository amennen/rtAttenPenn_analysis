# purpose: average significant clusters to see drivers of differences

import os
import glob
from shutil import copyfile
import pandas as pd
import json
import numpy as np
from subprocess import call
import sys
import scipy.stats
import nibabel as nib
import nilearn
import matplotlib.pyplot as plt
import seaborn as sns

## Frame wise displacement isn't here
first_level = '/data/jux/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/afni/first_level/stats'
second_level = '/data/jux/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/afni/group_level'
analyses_out = '/data/jux/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/afni/first_level/stats'
diff_group_out = '/data/jux/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/afni/group_level/ses-03_minus_ses-01'
neg_mask = diff_group_out + '/' + 'ses-03_minus_ses-01_stats_fearfulminusneut_ACC_dlPFC_mask.test1.ETACmask.global.1neg.5perc.nii.gz'
#neg_mask = group_out + '/' + 'ses-01_stats_fearfulminusneut_ACC_dlPFC_mask_fpr1.test1.ETACmask.global.1neg.1perc.nii.gz'
#pos_mask = group_out + '/' + 'ses-01_stats_fearfulminusneut_ACC_dlPFC_mask_fpr1.test1.ETACmask.global.1pos.1perc.nii.gz'

BRIK_KEY = {}
BRIK_KEY[0] = 'neutral'
BRIK_KEY[1] = 'object'
BRIK_KEY[2] = 'happy'
BRIK_KEY[3] = 'fearful'
BRIK_KEY[4] = 'happyminusneut'
BRIK_KEY[5] = 'fearfulminusneut'
BRIK = 5

# instead just load the means from each separate day and see
sessions = [1,3]
for ses in np.arange(len(sessions)):
    ses_id = 'ses-{0:02d}'.format(sessions[ses])
    mean_MDD = "{0}/{1}/{1}_stats_fearfulminusneut_ACC_dlPFC_mask.ttest.nii.gz'[5]'".format(second_level,ses_id)
    mean_HC = "{0}/{1}/{1}_stats_fearfulminusneut_ACC_dlPFC_mask.ttest.nii.gz'[9]'".format(second_level,ses_id)
    # now average each according to the mask
    cmd = "3dmaskave -mask {0} -quiet {1} > {2}/{3}/{3}_mean_MDD_ttest.nii.gz".format(neg_mask,mean_MDD,second_level,ses_id)
    call(cmd,shell=True)
    cmd = "3dmaskave -mask {0} -quiet {1} > {2}/{3}/{3}_mean_HC_ttest.nii.gz".format(neg_mask,mean_HC,second_level,ses_id)
    call(cmd,shell=True)


# now plot
all_data = np.zeros((4,))
for ses in np.arange(len(sessions)):
    ses_id = 'ses-{0:02d}'.format(sessions[ses])
    MDD_results = "{0}/{1}/{1}_mean_MDD_ttest.nii.gz".format(second_level,ses_id)
    HC_results = "{0}/{1}/{1}_mean_HC_ttest.nii.gz".format(second_level,ses_id)
    f = open(MDD_results,"r") #opens file with name of "test.txt"
    z = f.readline()
    f.close()
    all_data[ses*2] = float(z[:-1])

    f = open(HC_results,"r") #opens file with name of "test.txt"
    z = f.readline()
    f.close()
    all_data[ses*2 + 1] = float(z[:-1])
group = np.array(['MDD','HC','MDD','HC'])
ses = np.array(['Pre','Pre','Post','Post'])
data = {}
data['group'] = group
data['ses'] = ses
data['avg'] = all_data
df = pd.DataFrame.from_dict(data=data)

plt.figure()
sns.barplot(x='ses', y='avg', hue='group',data=df)
plt.show()

allsubjects = np.array([1,2,3,4,5,6,7,8,9,10,11,101,102,103,104,105,106,107,108,109,110,111,112])
for s in np.arange(len(allsubjects)):
    subjectNum = allsubjects[s]
    bids_id = 'sub-{0:03d}'.format(subjectNum)

    # concatenate confound EVS
    print(bids_id)
    sessions = [1,3]
    for ses in sessions:
        subjectDay = ses
        ses_id = 'ses-{0:02d}'.format(subjectDay)
        print(ses_id)
        glm_results = "{0}/{1}/{2}/{1}_{2}_task-faces_glm_coefs_REML.nii.gz'[{3}]'".format(first_level,bids_id,ses_id,BRIK)
        output_text_neg = "{0}/{1}/{2}/{1}_{2}_task-faces_negminusneut_dlPFC_neg_avg.txt".format(first_level,bids_id,ses_id)
        output_text_pos = "{0}/{1}/{2}/{1}_{2}_task-faces_negminusneut_dlPFC_pos_avg.txt".format(first_level,bids_id,ses_id)

        cmd = "3dmaskave -mask {0} -quiet {1} > {2}".format(neg_mask,glm_results,output_text_neg)
        call(cmd,shell=True)

        cmd = "3dmaskave -mask {0} -quiet {1} > {2}".format(pos_mask,glm_results,output_text_pos)
        call(cmd,shell=True)

# now read in all text files and plot
HC_ind = np.argwhere(allsubjects<100)[:,0]
MDD_ind = np.argwhere(allsubjects>100)[:,0]
nsubs = len(allsubjects)
all_subject_averages_neg = np.zeros((nsubs,2))
all_subject_averages_pos = np.zeros((nsubs,2))

for s in np.arange(len(allsubjects)):
    subjectNum = allsubjects[s]
    bids_id = 'sub-{0:03d}'.format(subjectNum)

    # concatenate confound EVS
    print(bids_id)
    sessions = [1,3]
    for ses in np.arange(len(sessions)):
        subjectDay = sessions[ses]
        ses_id = 'ses-{0:02d}'.format(subjectDay)
        print(ses_id)
        output_path = "{0}/{1}/{2}".format(first_level,bids_id,ses_id)
        output_text = "{0}/{1}_{2}_task-faces_negminusneut_dlPFC_neg_avg.txt".format(output_path,bids_id,ses_id)
        f = open(output_text,"r") #opens file with name of "test.txt"
        z = f.readline()
        f.close()

        all_subject_averages_neg[s,ses] = float(z[:-1])
        output_text = "{0}/{1}_{2}_task-faces_negminusneut_dlPFC_pos_avg.txt".format(output_path,bids_id,ses_id)
        f = open(output_text,"r") #opens file with name of "test.txt"
        z = f.readline()
        f.close()
        all_subject_averages_pos[s,ses] = float(z[:-1])


# for negative, MDD < HC so HC mean should be > MDD mean
np.mean(all_subject_averages_neg[HC_ind,0])
np.mean(all_subject_averages_neg[MDD_ind,0])

# for positive, MDD > HC
np.mean(all_subject_averages_pos[HC_ind,0])
np.mean(all_subject_averages_pos[MDD_ind,0])

colors = ['k', 'r'] # HC, MDD

fig = plt.figure(figsize=(10,7))
# plot for each subject
DAY = 0
for s in np.arange(nsubs):
    if allsubjects[s] < 100:
        style = 0
        index=1
        plt.plot(index,all_subject_averages_neg[s,DAY],marker='.', ms=20,color=colors[style],alpha=0.5)
    else:
        style = 1
        index=0
        plt.plot(index,all_subject_averages_neg[s,DAY], marker='.',ms=20,color=colors[style],alpha=0.5)
plt.errorbar(np.array([1]),np.mean(all_subject_averages_neg[HC_ind,DAY],axis=0),lw = 2,marker="+",ms=20,color=colors[0],yerr=scipy.stats.sem(all_subject_averages_neg[HC_ind,DAY],axis=0), label='HC')
plt.errorbar(np.array([0]),np.mean(all_subject_averages_neg[MDD_ind,DAY],axis=0),lw = 2,marker="+",ms=20,color=colors[1],yerr=scipy.stats.sem(all_subject_averages_neg[MDD_ind,DAY],axis=0), label='MDD')
plt.xticks(np.arange(2),('MDD', 'HC'))
plt.ylim([-.3,.3])
plt.xlabel('Group')
plt.ylabel('MDD < HC Session 1 Avg Activity')
plt.title('MDD < HC Session 1')
plt.legend()
fig=plt.figure(figsize=(10,7))
DAY = 1
for s in np.arange(nsubs):
    if allsubjects[s] < 100:
        style = 0
        index=1
        plt.plot(index,all_subject_averages_neg[s,DAY],marker='.', ms=20,color=colors[style],alpha=0.5)
    else:
        style = 1
        index=0
        plt.plot(index,all_subject_averages_neg[s,DAY], marker='.',ms=20,color=colors[style],alpha=0.5)
plt.errorbar(np.array([1]),np.mean(all_subject_averages_neg[HC_ind,DAY],axis=0),lw = 2,marker="+",ms=20,color=colors[0],yerr=scipy.stats.sem(all_subject_averages_neg[HC_ind,DAY],axis=0), label='HC')
plt.errorbar(np.array([0]),np.mean(all_subject_averages_neg[MDD_ind,DAY],axis=0),lw = 2,marker="+",ms=20,color=colors[1],yerr=scipy.stats.sem(all_subject_averages_neg[MDD_ind,DAY],axis=0), label='MDD')
plt.xticks(np.arange(2),('MDD', 'HC'))
plt.ylim([-.3,.3])
plt.xlabel('Group')
plt.ylabel('MDD < HC Session 1 Avg Activity')
plt.title('MDD < HC Session 3')
plt.legend()
plt.show()
