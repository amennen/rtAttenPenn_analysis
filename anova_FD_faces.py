# PURPOSE: run anova on FD displacement

import os
import glob
from shutil import copyfile
import pandas as pd
import json
import numpy as np
from subprocess import call
import sys
from statsmodels.formula.api import ols
import statsmodels.api as sm
import statsmodels
from statsmodels.stats.anova import AnovaRM
first_level = '/data/jux/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/afni/first_level/stats'
second_level = '/data/jux/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/afni/group_level/'

ses_id = 'ses-{0:02d}'.format(1)
covar_file_1 = second_level + '/' + 'FD_covar_{0}.txt'.format(ses_id)
ses_id = 'ses-{0:02d}'.format(3)
covar_file_2 = second_level + '/' + 'FD_covar_{0}.txt'.format(ses_id)

data1 = pd.read_csv(covar_file_1,sep=' ')
nSub = len(data1)
# session labels
ses_1_col = np.ones((nSub,))
# get group labels
allNames = data1['subj']
ses_1_group = [None] * nSub
for s in np.arange(nSub):
    subjectNum = int(allNames[s].split('-')[-1])
    if subjectNum < 100:
        ses_1_group[s] = 'HC'
    elif subjectNum > 100:
        ses_1_group[s] = 'MDD'
ses_1_info = {}
ses_1_info['FD'] = np.array(data1['FD'])
ses_1_info['subj'] = list(data1['subj'])
ses_1_info['ses'] = ses_1_col
ses_1_info['group'] = ses_1_group
ses_1_df = pd.DataFrame(data=ses_1_info)

# now do the same thing for the second session scan
data2 = pd.read_csv(covar_file_2,sep=' ')
nSub = len(data2)
# session labels
ses_2_col = 3*np.ones((nSub,))
# get group labels
allNames = data2['subj']
ses_2_group = [None] * nSub
for s in np.arange(nSub):
    subjectNum = int(allNames[s].split('-')[-1])
    if subjectNum < 100:
        ses_2_group[s] = 'HC'
    elif subjectNum > 100:
        ses_2_group[s] = 'MDD'
ses_2_info = {}
ses_2_info['FD'] = np.array(data2['FD'])
ses_2_info['subj'] = list(data2['subj'])
ses_2_info['ses'] = ses_2_col
ses_2_info['group'] = ses_2_group
ses_2_df = pd.DataFrame(data=ses_2_info)

FULL_DF = pd.concat([ses_1_df,ses_2_df])
aovrm2way = AnovaRM(FULL_DF, 'FD', 'subj', within=[ 'group'])
res2way = aovrm2way.fit()
print(res2way)

model = ols('FD ~ group*ses',data=FULL_DF).fit()
print(f"Overall model F({model.df_model: .0f},{model.df_resid: .0f}) = {model.fvalue: .3f}, p = {model.f_pvalue: .4f}")
model.summary()
aov_table = sm.stats.anova_lm(model, typ=2)
aov_table

# interaction not significant - repeat

model = ols('FD ~ group + ses',data=FULL_DF).fit()
print(f"Overall model F({model.df_model: .0f},{model.df_resid: .0f}) = {model.fvalue: .3f}, p = {model.f_pvalue: .4f}")
model.summary()
aov_table = sm.stats.anova_lm(model, typ=2)
aov_table

# look at each variable
mc = statsmodels.stats.multicomp.MultiComparison(FULL_DF['FD'], FULL_DF['group'])
mc_results = mc.tukeyhsd()
print(mc_results)

mc = statsmodels.stats.multicomp.MultiComparison(FULL_DF['FD'], FULL_DF['ses'])
mc_results = mc.tukeyhsd()
print(mc_results)

# nothing significant --> just take average and put into model or remove from model