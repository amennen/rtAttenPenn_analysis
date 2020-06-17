# get subject info

# values: 
# subjectnumber
# sex
# age
# group


import os
from os.path import exists, join
from os import makedirs
from glob import glob
from shutil import copyfile
import pandas as pd
import nibabel as nib
import json
import pydicom
import pandas as pd
import numpy as np
import glob

bids_dir = '/data/jux/cnds/amennen/rtAttenPenn/fmridata/Nifti'
file_name='participants.tsv'
columns=['participant_id', 'age', 'sex', 'group']
data=[]
# script should just loop over all subjects possible
allsubjects = np.array([1,2,3,4,5,6,7,8,9,10,11,12,101,102, 103, 104,105, 106,107,108,109,110,111,112,113,114,115])
nsub = len(allsubjects)


s  = pd.read_csv(join(bids_dir, 'participants.tsv'), sep='\t')
# get total females
females = np.argwhere(s['sex']=='F')[:,0]
avg_age = np.mean(s['age'])
print('***')
print('n females %i' % len(females))
print('average age %2.2f' % avg_age)
# get number of genders for each group
males_MDD = np.argwhere((s['group']=='MDD') & (s['sex']=='M'))[:,0]
n_males_MDD = len(males_MDD)
avg_age_males_MDD = np.mean(s['age'][males_MDD])
print('****')
print('n males MDD = %i' % n_males_MDD)
print('avg age = %2.2f' % avg_age_males_MDD)
females_MDD = np.argwhere((s['group']=='MDD') & (s['sex']=='F'))[:,0]
n_females_MDD = len(females_MDD)
avg_age_females_MDD = np.mean(s['age'][females_MDD])
print('****')
print('n females MDD = %i' % n_females_MDD)
print('avg age = %2.2f' % avg_age_females_MDD)
# get the average age for all MDD
all_MDD = np.argwhere(s['group']=='MDD')[:,0] 
MDD_age = np.mean(s['age'][all_MDD])
n_MDD = len(all_MDD)
print('****')
print('n MDD = %i' % n_MDD)
print('avg age = %2.2f' % MDD_age)
# get the average age for all HC
all_HC = np.argwhere(s['group']=='HC')[:,0]
HC_age = np.mean(s['age'][all_HC])
n_HC = len(all_HC)
print('****')
print('n HC = %i' % n_HC)
print('avg age = %2.2f' % HC_age)
males_HC = np.argwhere((s['group']=='HC') & (s['sex']=='M'))[:,0]
n_males_HC = len(males_HC)
avg_age_males_HC = np.mean(s['age'][males_HC])
print('****')
print('n males HC = %i' % n_males_HC)
print('avg age = %2.2f' % avg_age_males_HC)
females_HC = np.argwhere((s['group']=='HC') & (s['sex']=='F'))[:,0]
n_females_HC = len(females_HC)
avg_age_females_HC = np.mean(s['age'][females_HC])
print('****')
print('n females HC = %i' % n_females_HC)
print('avg age = %2.2f' % avg_age_females_HC)

