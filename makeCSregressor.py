# plot results/look at group differences

import os
import glob
import argparse
import numpy as np  # type: ignore
import sys
import pandas as pd
# Add current working dir so main can be run from the top level rtAttenPenn directory
sys.path.append(os.getcwd())
import rtfMRI.utils as utils
import rtfMRI.ValidationUtils as vutils
from rtfMRI.RtfMRIClient import loadConfigFile
from rtfMRI.Errors import ValidationError
from rtAtten.RtAttenModel import getSubjectDayDir
from sklearn.model_selection import KFold
from sklearn.linear_model import LogisticRegression
from rtfMRI.StructDict import StructDict, MatlabStructDict
from sklearn.metrics import roc_auc_score
import matplotlib
import matplotlib.pyplot as plt
import scipy
font = {'weight' : 'normal',
        'size'   : 22}
import csv
from anne_additions.plotting_pretty.commonPlotting import *
matplotlib.rc('font', **font)
# for each subject, you need to run getcs.py in anne_additions first to get cs evidence for that subject
# have python and matlab versions--let's start with matlab 



subjects = np.array([1,2,3,4,5,6,7,8,9,10,11,101, 102,103,104,105,106, 107,108,109,110,111,112,113,114])
HC_ind = np.argwhere(subjects<100)[:,0]
MDD_ind = np.argwhere(subjects>100)[:,0]
nsubs = len(subjects)
d1_runs = 6
d2_runs = 8
d3_runs = 7
totalRuns = d1_runs + d2_runs + d3_runs

# now do the same thing for cs
TRshift = 2
run_regressor = np.zeros((232,))
indices_dict = {}
# indices are from TR map in evernote - these are NOT shifted so now i'm going to shift (and subtracting index of 1)
indices_dict[5] = np.arange(116,141) + TRshift
indices_dict[6] = np.arange(144,169) + TRshift
indices_dict[7] = np.arange(172,197) + TRshift
indices_dict[8] = np.arange(200,225) + TRshift
NF_blocks=[5,6,7,8]
rtAttenPath = '/data/jux/cnds/amennen/rtAttenPenn/fmridata/behavdata/gonogo'
save_dir = '/data/jux/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/afni/first_level/neurofeedback/CS_regressors'
# get HC averages for each RUN OF SCANNER/DAY
nDays = 3
for s in np.arange(nsubs):
#for s in np.arange(1):
#   s=0
    subject_key = 'subject' + str(subjects[s])
    subjectDir = rtAttenPath + '/' + 'subject' + str(subjects[s])
    outfile = subjectDir + '/' 'offlineAUC_RTCS.npz'    
    z=np.load(outfile)
    if subjects[s] == 106:
        d1_runs = 5
    else:
        d1_runs = 6
    CS = z['csOverTime'] # n NF runs x 100 TRs x 3 days
    nTR = np.shape(CS)[1]
    for d in np.arange(nDays):
        if d == 0:
            categSep = CS[0:d1_runs,:,0]
            nRuns = d1_runs
        elif d == 1:
            categSep = CS[0:d2_runs,:,1]
            nRuns = d2_runs
        elif d == 2:
            categSep = CS[0:d3_runs,:,2]
            nRuns = d3_runs

        # now iterate for each run and save regressor
        for r in np.arange(nRuns):
            # if neurofeedback run = 0, actually run is 1 more, then add another 1 because of non 0-based indexing
            run_id = 'run-{0:02d}'.format(r+2)
            run_regressor = np.zeros((232,))*np.nan
            this_run_data = categSep[r,:]
            this_run_reshaped = np.reshape(this_run_data,(4,25))
            for b in np.arange(4):
                run_regressor[indices_dict[b+5]] = this_run_reshaped[b,:]

            z = pd.DataFrame(data=run_regressor)








