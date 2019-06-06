# purpose: delete TRs that you don't want for fsl first level and take only the noise EVs that you care about

import os
import glob
from shutil import copyfile
import pandas as pd
import json
import numpy as np

bids_dir = '/data/jag/cnds/amennen/rtAttenPenn/fmridata/Nifti'
save_dir = '/data/jag/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/fsl/first_level/confound_EVs'
fmriprep_out="/data/jag/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/fmriprep"

# then create empty tsv files
#all_subjects = np.array([2,101,102,103,104,105])
all_subjects = np.array([3])
# don't run on subject 1, day 1** accidentally deleted the TRs for the person so run with ntodelete=0 for days 1 ONLY**
# to read in old file: OLD=pd.read_csv(full_save_path,sep='\t')
nsub=len(all_subjects)
ndays=3
for s in np.arange(nsub):
        subjectNum=all_subjects[s]
        for d in np.arange(ndays):
                subjectDay=d+1
                bids_id = 'sub-{0:03d}'.format(subjectNum)
                print(bids_id)
                ses_id = 'ses-{0:02d}'.format(subjectDay)
                print(ses_id)
                day_path=os.path.join(fmriprep_out,bids_id,ses_id)
                func_path = os.path.join(day_path,'func')
                all_func_tsv = glob.glob(os.path.join(func_path, '*_confounds.tsv'))
                n_func = len(all_func_tsv)

                for t in np.arange(n_func):
                        # updated change 1/28: if resting/go no go don't do this because we're going to handle everything differently
                        if 'faces' in all_func_tsv[t]:
                                # if not the faces task, then don't save the confounds
                                nToDelete = 5 # want to go from 147 --> 142 TRs
                                if subjectNum == 1 and subjectDay == 1:
                                	nToDelete=0
                                z = pd.read_csv(all_func_tsv[t], sep='\t')
                                NAMETOSAVE = os.path.split(all_func_tsv[t])[-1]
                                newDF = pd.DataFrame(data=z[nToDelete:], columns=['FramewiseDisplacement','X', 'Y', 'Z', 'RotX', 'RotY', 'RotZ'])
                                #newDF = pd.DataFrame(data=z[nToDelete:], columns=['aCompCor00','aCompCor01', 'aCompCor02', 'aCompCor03', 'aCompCor04', 'aCompCor05','X', 'Y', 'Z', 'RotX', 'RotY', 'RotZ'])
                                # delete 5 TRS for faces task and delete 10 TRs for gononogo task

                                # make new directory for that subject/day
                                dest_path = save_dir + '/' + bids_id + '/' + ses_id
                                if not os.path.exists(dest_path):
                                        os.makedirs(dest_path)
                                full_save_path = os.path.join(dest_path,NAMETOSAVE)
                                newDF.to_csv(full_save_path,sep='\t',index=False)
                                # check that you didn't erase tsv files like an idiot
                                
                                print('ORIGINAL CONFOUND EV SHAPE')
                                z = pd.read_csv(all_func_tsv[t], sep='\t')
                                print(np.shape(z))
                                # check that you set EV files correctly
                                print('NEW CONFOUND SHAPE')
                                dest_path = save_dir + '/' + bids_id + '/' + ses_id
                                NAMETOSAVE = os.path.split(all_func_tsv[t])[-1]
                                full_save_path = os.path.join(dest_path,NAMETOSAVE)
                                z = pd.read_csv(full_save_path, sep='\t')
                                print(np.shape(z))
