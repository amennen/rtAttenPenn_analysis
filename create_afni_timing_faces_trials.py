# Purpose: get all 6 trials
# there's 6 trials per run, each 3 second long, repeated 3 times

import os
import glob
from shutil import copyfile
import pandas as pd
import json
import numpy as np

save_path = '/data/jux/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/afni/first_level/timing_files';
all_categories = ['fearful','happy', 'neutral', 'object']
subjects = np.array([1,2,3,4,5,6,7,8,9,10,11,101, 102,103,104,105,106, 107,108,109,110,111,112,113,114])
days=[1,3]
for subjectNum in subjects:
    bids_id = 'sub-{0:03d}'.format(subjectNum)
    for d in days:
        subjectDay=d
        ses_id = 'ses-{0:02d}'.format(subjectDay)
        # then for each category, we want the first, last, and 1 TR after
        for c in np.arange(len(all_categories)):
            category = all_categories[c]
            category_str = category + '.txt'
            file_name = os.path.join(save_path,bids_id,ses_id, category_str)
            t = pd.read_fwf(file_name,header=None)
            timing = t.values # now 2 x 18 array
            # all first values are every 6
            ntrials = 6
            #timing[0,trial] timing[0,trial+ntrials] timing[0,trial+(ntrials*2)]
            for trial in np.arange(ntrials):
                category_str_out = category + '_' + 'trial' + '_' + str(trial) + '.txt'
                output_file = os.path.join(save_path,bids_id,ses_id,category_str_out)
                outF = open(output_file,"w")
                outF.write('%8.4f %8.4f %8.4f\n' % (timing[0,trial],timing[0,trial+ntrials],timing[0,trial+(ntrials*2)]))
                outF.write('%8.4f %8.4f %8.4f' % (timing[1,trial],timing[1,trial+ntrials],timing[1,trial+(ntrials*2)]))
                outF.close()

