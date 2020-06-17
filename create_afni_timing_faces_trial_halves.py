# Purpose: take teh first and last trials of the runs
# there's 3 blocks/run - get only first 2 trials, last 2 trials
# each trial is 3 seconds, there are 6 trials = 18 seconds for the block total
import os
import glob
from shutil import copyfile
import pandas as pd
import json
import numpy as np

save_path = '/data/jux/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/afni/first_level/timing_files';
#all_categories = ['fearful','happy', 'neutral']
all_categories = ['object']
# on 1/14/20  - redoing with object so that I can do this including object as a regressor
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
            nhalves = 2
            # first half: colums 0 & 1
            # last half: columns 4 & 5
            #timing[0,trial] timing[0,trial+ntrials] timing[0,trial+(ntrials*2)]
            for h in np.arange(nhalves):
                trial_1 = (h*4)
                trial_2 = (h*4) + 1
                category_str_out = category + '_' + 'half' + '_' + str(h) + '.txt'
                output_file = os.path.join(save_path,bids_id,ses_id,category_str_out)
                outF = open(output_file,"w")
                outF.write('%8.4f %8.4f %8.4f %8.4f %8.4f %8.4f\n' % (timing[0,trial_1],timing[0,trial_2],timing[0,trial_1+ntrials],timing[0,trial_2+ntrials],timing[0,trial_1+(ntrials*2)],timing[0,trial_2+(ntrials*2)]))
                outF.write('%8.4f %8.4f %8.4f %8.4f %8.4f %8.4f' % (timing[1,trial_1],timing[1,trial_2],timing[1,trial_1+ntrials],timing[1,trial_2+ntrials],timing[1,trial_1+(ntrials*2)],timing[1,trial_2+(ntrials*2)]))
                outF.close()

