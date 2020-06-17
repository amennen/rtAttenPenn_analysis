# PURPOSE: create new derivative csv file by:

# 1. reading given subject's/day/task confound csv
# 2. specify which confounds you're keeping
# 3. for each of the confounds:
        # - take derivative
        # - take quadratic
        # - take derivative of quadtratic
# 4. add this to a new CSV file 
# 5. save CSV file (1D format for AFNI)
# 6. truncate and save nifti file

import os
import glob
import pandas as pd
import json
import numpy as np
from subprocess import call
import sys

fmriprep_out="/data/jux/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/fmriprep"
save_dir='/data/jux/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/resting/confound_EVs'
trunc_save_dir = '/data/jux/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/resting/trunc'
# subjects 106,3,107,4,108 got resting state
#subjectNum = 106
# make subject number argument
subjectNum=np.int(sys.argv[1])

bids_id = 'sub-{0:03d}'.format(subjectNum)
print(bids_id)
ndays=3

for d in np.arange(ndays):
        subjectDay = d + 1
        ses_id = 'ses-{0:02d}'.format(subjectDay)
        print(ses_id)
        day_path=os.path.join(fmriprep_out,bids_id,ses_id, 'func')
        all_func_tsv = glob.glob(os.path.join(day_path, '*_confounds.tsv'))
        n_func = len(all_func_tsv)
        for t in np.arange(n_func):
                if 'rest' in all_func_tsv[t]:
                        #fn = glob.glob(os.path.join(day_path, '*task-rest*confounds.tsv'))
                        resting_confounds = all_func_tsv[t]
                        nToDelete = 4
                        z = pd.read_csv(resting_confounds, sep='\t')
                        print('ORIGINAL CONFOUND EV SHAPE')
                        print(np.shape(z))
                        NAMETOSAVE = os.path.split(resting_confounds)[-1]
                        NAMETOSAVE_ROOT = NAMETOSAVE.split('.')[0]
                        columns=['CSF','WhiteMatter', 'GlobalSignal', 'X', 'Y', 'Z','RotX', 'RotY', 'RotZ']
                        nConfounds = len(columns)
                        NEWDF = pd.DataFrame(data=z[nToDelete:],columns=columns)
                        MASTERDF = pd.DataFrame(data=z[nToDelete:],columns=columns)
                        #motion_confounds = ['X', 'Y', 'Z','RotX', 'RotY', 'RotZ']
                        #n_moco = len(motion_confounds)
                        for c in np.arange(nConfounds): # doing derivative etc. to ALL confounds not just motion ones
                                this_confound_name = columns[c]
                                this_confound = NEWDF[columns[c]]
                                c_diff = np.nan_to_num(pd.Series.diff(this_confound))
                                c_diff_name = this_confound_name + '_diff'
                                c_squared = this_confound.apply(np.square)
                                c_squared_name = this_confound_name + '_sq'
                                c_squared_diff = np.nan_to_num(pd.Series.diff(c_squared))
                                c_squared_diff_name = this_confound_name + '_sq_diff'

                                # now add to master dataframe
                                MASTERDF[c_diff_name] = c_diff
                                MASTERDF[c_squared_name] = c_squared
                                MASTERDF[c_squared_diff_name] = c_squared_diff

                        #final_array = MASTERDF.values
                        # now save this as 1D file

                        dest_path = save_dir + '/' + bids_id + '/' + ses_id
                        if not os.path.exists(dest_path):
                                os.makedirs(dest_path)
                        print('NEW CONFOUND SHAPE')
                        print(np.shape(MASTERDF))
                        NAMETOSAVE = NAMETOSAVE_ROOT + '.1D'
                        full_save_path = os.path.join(dest_path,NAMETOSAVE)
                        print('saving to' + full_save_path)
                        MASTERDF.to_csv(full_save_path,sep='\t',index=False,header=False)

                        # now delete first 4 TRs and resave nifti file
                        rest_nifti_fn = glob.glob(os.path.join(day_path,'*task-rest_rec-uncorrected_run-01_bold_space-MNI*preproc*'))
                        rest_nifti = rest_nifti_fn[0]
                        NAMETOSAVE = os.path.split(rest_nifti)[-1]
                        dest_path = trunc_save_dir + '/' + bids_id + '/' + ses_id
                        if not os.path.exists(dest_path):
                                os.makedirs(dest_path)
                        full_save_path = os.path.join(dest_path, NAMETOSAVE)
                        # now run fslroi command to remove first 4 TRs
                        #print('fslroi %s %s %i' % (rest_nifti,full_save_path,nToDelete))
                        command = 'fslroi %s %s %i %i' % (rest_nifti,full_save_path,nToDelete,np.shape(MASTERDF)[0])
                        call(command,shell=True)

