# Purpose: take teh first and last trials of the runs
# there's 3 trials/run

import os
import glob
from shutil import copyfile
import pandas as pd
import json
import numpy as np

save_path = '/data/jux/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/afni/first_level/timing_files';
all_categories = ['fearful','happy', 'neutral']
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
            ind_first = np.arange(0,18,6)
            ind_last = np.arange(5,18,6)
            A_first_timing = timing[0,ind_first]
            A_last_timing = timing[0,ind_last]
            A_carry_timing = A_last_timing + 3
            B_first_timing = timing[1,ind_first]
            B_last_timing = timing[1,ind_last]
            B_carry_timing = B_last_timing + 3

            # now print to a data file
            category_str_out_first = category + '_first' + '.txt'
            category_str_out_last = category + '_last' + '.txt'
            category_str_out_carry = category + '_carry' + '.txt'

            output_first = os.path.join(save_path,bids_id,ses_id,category_str_out_first)
            outF = open(output_first,"w")
            outF.write('%8.4f %8.4f %8.4f\n' % (A_first_timing[0],A_first_timing[1],A_first_timing[2]))
            outF.write('%8.4f %8.4f %8.4f' % (B_first_timing[0],B_first_timing[1],B_first_timing[2]))
            outF.close()

            output_last = os.path.join(save_path,bids_id,ses_id,category_str_out_last)
            outF = open(output_last,"w")
            outF.write('%8.4f %8.4f %8.4f\n' % (A_last_timing[0],A_last_timing[1],A_last_timing[2]))
            outF.write('%8.4f %8.4f %8.4f' % (B_last_timing[0],B_last_timing[1],B_last_timing[2]))
            outF.close()

            output_carry = os.path.join(save_path,bids_id,ses_id,category_str_out_carry)
            outF = open(output_carry,"w")
            outF.write('%8.4f %8.4f %8.4f\n' % (A_carry_timing[0],A_carry_timing[1],A_carry_timing[2]))
            outF.write('%8.4f %8.4f %8.4f' % (B_carry_timing[0],B_carry_timing[1],B_carry_timing[2]))
            outF.close()
