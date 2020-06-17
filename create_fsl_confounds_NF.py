# purpose: delete TRs that you don't want for fsl first level and take only the noise EVs that you care about

import os
import glob
from shutil import copyfile
import pandas as pd
import json
import numpy as np

bids_dir = '/data/jux/cnds/amennen/rtAttenPenn/fmridata/Nifti'
save_dir = '/data/jux/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/fsl/first_level/confound_EVs'
fmriprep_out="/data/jux/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/fmriprep"

# then create empty tsv files
#all_subjects = np.array([2,101,102,103,104,105])
#all_subjects = np.array([4,107])
#all_subjects = np.array([1,2,3,4,5,6,7,8,9,10,11,101, 102,103,104,105,106, 107,108,109,110,111,112,113,114])
all_subjects = np.array([110])
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
                if subjectNum==110 and subjectDay==1:
                        # change the day path manually
                        day_path = os.path.join(fmriprep_out,bids_id,'ses-10')
                func_path = os.path.join(day_path,'func')
                all_func_tsv = glob.glob(os.path.join(func_path, '*_confounds.tsv'))
                n_func = len(all_func_tsv)

                for t in np.arange(n_func):
                        # updated change 1/28: if resting/go no go don't do this because we're going to handle everything differently
                        if 'task-gonogo_rec-uncorrected' in all_func_tsv[t]:
                                print(all_func_tsv[t])
                                # if not the faces task, then don't save the confounds
                                if subjectNum == 1 and subjectDay == 1:
                                        nToDelete=0
                                else:
                                        nToDelete = 10 # want to go from 242 --> 232 TRs
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
                                print(full_save_path)
                                newDF.to_csv(full_save_path,sep='\t',index=False)
                                # check that you didn't erase tsv files like an idiot
                                NAMETOSAVE_1D = NAMETOSAVE.split('.')[0] + '.1D'
                                full_save_path_1D = os.path.join(dest_path,NAMETOSAVE_1D)
                                newDF.to_csv(full_save_path_1D,sep='\t',index=False,header=False)

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
