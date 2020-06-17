"""
Functions to help process real-time fMRI data after-the-fact. Processes all the block data from a full run
"""


import numpy as np
import glob 
import sys
import os
import os
import glob
import argparse
import sys
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
font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 22}

matplotlib.rc('font', **font)
import csv
import matplotlib.pyplot as plt
import math

# NOTE: will have to un-wrap the sample data from the sampledata directory in order for this to work now
def get_blockData(subjNumb, day, run):
    data_files = glob.glob('/data/jag/cnds/amennen/rtAttenPenn/behavgonogo' + '/subject'+str(subjNumb)+'/day'+str(day)+'/run'+str(run)+'/blockdata_'+str(run)+'*.mat')
    filename = data_files[-1]
    behav = utils.loadMatFile(filename)
    data = behav['blockData']
    return data 

def get_blockType(data):
	blockTypes = np.zeros((8,1))
	for b in np.arange(8):
		blockTypes[b] = data['specificBlock'][:,b][0][0][0]
	return blockTypes[:,0].astype(int)

def aprime(h,fa):
    if h + fa != 2 and h + fa != 0: 
    	if np.greater_equal(h,fa): a = .5 + (((h-fa) * (1+h-fa)) / (4 * h * (1-fa)))
    	else: a = .5 - (((fa-h) * (1+fa-h)) / (4 * fa * (1-h)))
    else:
        a = np.nan
    return a
# Takes in the 'blockdata' from a given run as input, and returns and 1x8 array indicating what the 'attended category'
# was for each of the 8 blocks in the run (1 = scene, 2 = face)
def get_attCategs(data):
    # what category are they attending to during this block? 1 = attending to face, 2 = attending to scene 
    # make a list of 8 values, which tells you the attended category for each block in the run 
    # so attCateg[i] is the category of what they are supposed to attend to for each of the 8 blocks in this 
    # run (i from 0-7)
    temp_attCateg = data.attCateg[0,:]
    attCateg = []
    attCateg[:] = [temp_attCateg[i][0] for i in range(0,len(temp_attCateg))]
    return attCateg


    

# Takes the 'blockdata' from a given run as input, and returns 2 things:
# (1) an 8x50 array of the scene category for each scene image (indoor or outdoor)
# (2) an 8x50 array of the face category for each face image (neutral male, neutral female, sad male, sad female,
#      happy male, happy female)
def get_imCategs(data):
    # create a data structure to store whether the scene is indoor(1)/outdoor(2) for each stimulus
    # sceneImCategs[i][j] gives the category of the scene (indoor or outdoor), with i from 0-7 (each block) and 
    # j from 0-49 (each trial)
    temp_sceneImCategs = data.categs[0,:]
    sceneImCategs = []
    sceneImCategs[:] = [temp_sceneImCategs[i][0][0][0] for i in range(0,len(temp_sceneImCategs))]


    # create a data structure to store whether the face is male/female and happy/neutral/sad for each stimulus
    # neutral M = 3, neutral F = 4, sad M = 5, sad F = 6, happy M = 7, happy F = 8
    # faceImCategs[i][j] gives the category of the face , with i from 0-7 (each block) and 
    # j from 0-49 (each trial)
    temp_faceImCategs = data.categs[0,:]
    faceImCategs = []
    faceImCategs[:] = [temp_faceImCategs[i][0][1][0] for i in range(0,len(temp_faceImCategs))]

    return sceneImCategs, faceImCategs



# Takes the 'blockdata' from a given run as input, and returns an 8x50 array indicating whether each trial was
# a Go Trial (1) or a No-Go Trial (0), as well as an 8x50 array indicating whether the subject pressed (1) or didn't 
# press (0) at each trial
def get_trialTypes_and_responses(data):
    # create a data structure to store the trial type (Go or No-Go) for each trial. 
    # trialType[i][j] gives the trial type for trial j in block i (i from 0-7, j from 0-49)
    temp_trialType = data.corrresps[0,:]
    trialType = []

    trialType[:] = [temp_trialType[i][0] for i in range(0, len(temp_trialType))]
    flatList_trialType = [item for sublist in trialType for item in sublist]

    temp2_trialType = flatList_trialType
    temp2_trialType = [0  if np.isnan(i) else 1.0 for i in flatList_trialType]
    trialType = np.reshape(temp2_trialType, [8,50])
    
    # create a data structure to store their behavioral responses (press vs no-press)
    # 1 = press, 0 = no press. responses[i][j] gives subject's response on trial j (0-49) during block i (0-7)
    temp_responses = data.accs[0,:]
    responses = []

    responses[:] = [temp_responses[i][0] for i in range(0, len(temp_responses))]
    flatList_responses = [item for sublist in responses for item in sublist]
    
    temp2_responses = flatList_responses 
    temp2_responses = [1 if flatList_responses[i] == 0 and temp2_trialType[i] == 0 else flatList_responses[i] for i in
                       range(0,len(flatList_responses))]
    temp2_responses = [0 if i == 2 else i for i in temp2_responses]
    responses = np.reshape(temp2_responses, [8,50])
    
    return trialType, responses


def get_decMatrices_and_aPrimes(data):
    trialType, responses = get_trialTypes_and_responses(data)
    specificTypes = get_blockType(data)
    block1_trialType = trialType[0]
    block1_responses = responses[0]

    block2_trialType = trialType[1]
    block2_responses = responses[1]

    block3_trialType = trialType[2]
    block3_responses = responses[2]

    block4_trialType = trialType[3]
    block4_responses = responses[3]

    block5_trialType = trialType[4]
    block5_responses = responses[4]

    block6_trialType = trialType[5]
    block6_responses = responses[5]

    block7_trialType = trialType[6]
    block7_responses = responses[6]

    block8_trialType = trialType[7]
    block8_responses = responses[7]

    run_hitRates = [] # store all the hit rates for the blocks in this run (1st val is hit rate for block 1, etc.)
    run_missRates = []
    run_FAs = []
    run_CRs = []
    run_aprimes = []


    # code: Hit = 1, Miss = -1, False Alarm = -2, Correct Rejection = 2
    # block 1
    block1_results = np.zeros(len(trialType[0]))
    for i in range(0,len(block1_results)):
        if (block1_trialType[i] == 1 and block1_responses[i] == 1): # hit 
            block1_results[i] = 1
        elif (block1_trialType[i] == 1 and block1_responses[i] == 0): # miss
            block1_results[i] = -1
        elif (block1_trialType[i] == 0 and block1_responses[i] == 1): # false alarm
            block1_results[i] = -2
        elif (block1_trialType[i] == 0 and block1_responses[i] == 0): # correct rejection 
            block1_results[i] = 2

    block1_hits = np.where(block1_results == 1)
    block1_misses = np.where(block1_results == -1)
    block1_FAs = np.where(block1_results == -2)
    block1_CRs = np.where(block1_results == 2)
    block1_hit_rate = len(block1_hits[0])/(len(block1_hits[0]) + len(block1_misses[0]))
    run_hitRates.append(block1_hit_rate)
    block1_miss_rate = len(block1_misses[0])/(len(block1_hits[0]) + len(block1_misses[0]))
    run_missRates.append(block1_miss_rate)
    block1_FA_rate = len(block1_FAs[0])/(len(block1_FAs[0]) + len(block1_CRs[0]))
    run_FAs.append(block1_FA_rate)
    block1_CR_rate = len(block1_CRs[0])/(len(block1_FAs[0]) + len(block1_CRs[0]))
    run_CRs.append(block1_CR_rate)

    block1_aprime = aprime(block1_hit_rate, block1_FA_rate)
    run_aprimes.append(block1_aprime)

    
    # block 2
    block2_results = np.zeros(len(trialType[0]))
    for i in range(0,len(block2_results)):
        if (block2_trialType[i] == 1 and block2_responses[i] == 1): # hit 
            block2_results[i] = 1
        elif (block2_trialType[i] == 1 and block2_responses[i] == 0): # miss
            block2_results[i] = -1
        elif (block2_trialType[i] == 0 and block2_responses[i] == 1): # false alarm
            block2_results[i] = -2
        elif (block2_trialType[i] == 0 and block2_responses[i] == 0): # correct rejection 
            block2_results[i] = 2

    block2_hits = np.where(block2_results == 1)
    block2_misses = np.where(block2_results == -1)
    block2_FAs = np.where(block2_results == -2)
    block2_CRs = np.where(block2_results == 2)
    block2_hit_rate = len(block2_hits[0])/(len(block2_hits[0]) + len(block2_misses[0]))
    run_hitRates.append(block2_hit_rate)
    block2_miss_rate = len(block2_misses[0])/(len(block2_hits[0]) + len(block2_misses[0]))
    run_missRates.append(block2_miss_rate)
    block2_FA_rate = len(block2_FAs[0])/(len(block2_FAs[0]) + len(block2_CRs[0]))
    run_FAs.append(block2_FA_rate)
    block2_CR_rate = len(block2_CRs[0])/(len(block2_FAs[0]) + len(block2_CRs[0]))
    run_CRs.append(block2_CR_rate)

    block2_aprime = aprime(block2_hit_rate, block2_FA_rate)
    run_aprimes.append(block2_aprime)
       

    # block 3
    block3_results = np.zeros(len(trialType[0]))
    for i in range(0,len(block3_results)):
        if (block3_trialType[i] == 1 and block3_responses[i] == 1): # hit 
            block3_results[i] = 1
        elif (block3_trialType[i] == 1 and block3_responses[i] == 0): # miss
            block3_results[i] = -1
        elif (block3_trialType[i] == 0 and block3_responses[i] == 1): # false alarm
            block3_results[i] = -2
        elif (block3_trialType[i] == 0 and block3_responses[i] == 0): # correct rejection 
            block3_results[i] = 2

    block3_hits = np.where(block3_results == 1)
    block3_misses = np.where(block3_results == -1)
    block3_FAs = np.where(block3_results == -2)
    block3_CRs = np.where(block3_results == 2)
    block3_hit_rate = len(block3_hits[0])/(len(block3_hits[0]) + len(block3_misses[0]))
    run_hitRates.append(block3_hit_rate)
    block3_miss_rate = len(block3_misses[0])/(len(block3_hits[0]) + len(block3_misses[0]))
    run_missRates.append(block3_miss_rate)
    block3_FA_rate = len(block3_FAs[0])/(len(block3_FAs[0]) + len(block3_CRs[0]))
    run_FAs.append(block3_FA_rate)
    block3_CR_rate = len(block3_CRs[0])/(len(block3_FAs[0]) + len(block3_CRs[0]))
    run_CRs.append(block3_CR_rate)

    block3_aprime = aprime(block3_hit_rate, block3_FA_rate)
    run_aprimes.append(block3_aprime)


    # block 4
    block4_results = np.zeros(len(trialType[0]))
    for i in range(0,len(block4_results)):
        if (block4_trialType[i] == 1 and block4_responses[i] == 1): # hit 
            block4_results[i] = 1
        elif (block4_trialType[i] == 1 and block4_responses[i] == 0): # miss
            block4_results[i] = -1
        elif (block4_trialType[i] == 0 and block4_responses[i] == 1): # false alarm
            block4_results[i] = -2
        elif (block4_trialType[i] == 0 and block4_responses[i] == 0): # correct rejection 
            block4_results[i] = 2

    block4_hits = np.where(block4_results == 1)
    block4_misses = np.where(block4_results == -1)
    block4_FAs = np.where(block4_results == -2)
    block4_CRs = np.where(block4_results == 2)
    block4_hit_rate = len(block4_hits[0])/(len(block4_hits[0]) + len(block4_misses[0]))
    run_hitRates.append(block4_hit_rate)
    block4_miss_rate = len(block4_misses[0])/(len(block4_hits[0]) + len(block4_misses[0]))
    run_missRates.append(block4_miss_rate)
    block4_FA_rate = len(block4_FAs[0])/(len(block4_FAs[0]) + len(block4_CRs[0]))
    run_FAs.append(block4_FA_rate)
    block4_CR_rate = len(block4_CRs[0])/(len(block4_FAs[0]) + len(block4_CRs[0]))
    run_CRs.append(block4_CR_rate)

    block4_aprime = aprime(block4_hit_rate, block4_FA_rate)
    run_aprimes.append(block4_aprime)

    # block 5
    block5_results = np.zeros(len(trialType[0]))
    for i in range(0,len(block5_results)):
        if (block5_trialType[i] == 1 and block5_responses[i] == 1): # hit 
            block5_results[i] = 1
        elif (block5_trialType[i] == 1 and block5_responses[i] == 0): # miss
            block5_results[i] = -1
        elif (block5_trialType[i] == 0 and block5_responses[i] == 1): # false alarm
            block5_results[i] = -2
        elif (block5_trialType[i] == 0 and block5_responses[i] == 0): # correct rejection 
            block5_results[i] = 2

    block5_hits = np.where(block5_results == 1)
    block5_misses = np.where(block5_results == -1)
    block5_FAs = np.where(block5_results == -2)
    block5_CRs = np.where(block5_results == 2)
    block5_hit_rate = len(block5_hits[0])/(len(block5_hits[0]) + len(block5_misses[0]))
    run_hitRates.append(block5_hit_rate)
    block5_miss_rate = len(block5_misses[0])/(len(block5_hits[0]) + len(block5_misses[0]))
    run_missRates.append(block5_miss_rate)
    block5_FA_rate = len(block5_FAs[0])/(len(block5_FAs[0]) + len(block5_CRs[0]))
    run_FAs.append(block5_FA_rate)
    block5_CR_rate = len(block5_CRs[0])/(len(block5_FAs[0]) + len(block5_CRs[0]))
    run_CRs.append(block5_CR_rate)

    block5_aprime = aprime(block5_hit_rate, block5_FA_rate)
    run_aprimes.append(block5_aprime)



    # block 6
    block6_results = np.zeros(len(trialType[0]))
    for i in range(0,len(block6_results)):
        if (block6_trialType[i] == 1 and block6_responses[i] == 1): # hit 
            block6_results[i] = 1
        elif (block6_trialType[i] == 1 and block6_responses[i] == 0): # miss
            block6_results[i] = -1
        elif (block6_trialType[i] == 0 and block6_responses[i] == 1): # false alarm
            block6_results[i] = -2
        elif (block6_trialType[i] == 0 and block6_responses[i] == 0): # correct rejection 
            block6_results[i] = 2

    block6_hits = np.where(block6_results == 1)
    block6_misses = np.where(block6_results == -1)
    block6_FAs = np.where(block6_results == -2)
    block6_CRs = np.where(block6_results == 2)
    block6_hit_rate = len(block6_hits[0])/(len(block6_hits[0]) + len(block6_misses[0]))
    run_hitRates.append(block6_hit_rate)
    block6_miss_rate = len(block6_misses[0])/(len(block6_hits[0]) + len(block6_misses[0]))
    run_missRates.append(block6_miss_rate)
    block6_FA_rate = len(block6_FAs[0])/(len(block6_FAs[0]) + len(block6_CRs[0]))
    run_FAs.append(block6_FA_rate)
    block6_CR_rate = len(block6_CRs[0])/(len(block6_FAs[0]) + len(block6_CRs[0]))
    run_CRs.append(block6_CR_rate)

    block6_aprime = aprime(block6_hit_rate, block6_FA_rate)
    run_aprimes.append(block6_aprime)



    # block 7
    block7_results = np.zeros(len(trialType[0]))
    for i in range(0,len(block7_results)):
        if (block7_trialType[i] == 1 and block7_responses[i] == 1): # hit 
            block7_results[i] = 1
        elif (block7_trialType[i] == 1 and block7_responses[i] == 0): # miss
            block7_results[i] = -1
        elif (block7_trialType[i] == 0 and block7_responses[i] == 1): # false alarm
            block7_results[i] = -2
        elif (block7_trialType[i] == 0 and block7_responses[i] == 0): # correct rejection 
            block7_results[i] = 2

    block7_hits = np.where(block7_results == 1)
    block7_misses = np.where(block7_results == -1)
    block7_FAs = np.where(block7_results == -2)
    block7_CRs = np.where(block7_results == 2)
    block7_hit_rate = len(block7_hits[0])/(len(block7_hits[0]) + len(block7_misses[0]))
    run_hitRates.append(block7_hit_rate)
    block7_miss_rate = len(block7_misses[0])/(len(block7_hits[0]) + len(block7_misses[0]))
    run_missRates.append(block7_miss_rate)
    block7_FA_rate = len(block7_FAs[0])/(len(block7_FAs[0]) + len(block7_CRs[0]))
    run_FAs.append(block7_FA_rate)
    block7_CR_rate = len(block7_CRs[0])/(len(block7_FAs[0]) + len(block7_CRs[0]))
    run_CRs.append(block7_CR_rate)

    block7_aprime = aprime(block7_hit_rate, block7_FA_rate)
    run_aprimes.append(block7_aprime)


    # block 8
    block8_results = np.zeros(len(trialType[0]))
    for i in range(0,len(block8_results)):
        if (block8_trialType[i] == 1 and block8_responses[i] == 1): # hit 
            block8_results[i] = 1
        elif (block8_trialType[i] == 1 and block8_responses[i] == 0): # miss
            block8_results[i] = -1
        elif (block8_trialType[i] == 0 and block8_responses[i] == 1): # false alarm
            block8_results[i] = -2
        elif (block8_trialType[i] == 0 and block8_responses[i] == 0): # correct rejection 
            block8_results[i] = 2

    block8_hits = np.where(block8_results == 1)
    block8_misses = np.where(block8_results == -1)
    block8_FAs = np.where(block8_results == -2)
    block8_CRs = np.where(block8_results == 2)
    block8_hit_rate = len(block8_hits[0])/(len(block8_hits[0]) + len(block8_misses[0]))
    run_hitRates.append(block8_hit_rate)
    block8_miss_rate = len(block8_misses[0])/(len(block8_hits[0]) + len(block8_misses[0]))
    run_missRates.append(block8_miss_rate)
    block8_FA_rate = len(block8_FAs[0])/(len(block8_FAs[0]) + len(block8_CRs[0]))
    run_FAs.append(block8_FA_rate)
    block8_CR_rate = len(block8_CRs[0])/(len(block8_FAs[0]) + len(block8_CRs[0]))
    run_CRs.append(block8_CR_rate)

    block8_aprime = aprime(block8_hit_rate, block8_FA_rate)
    run_aprimes.append(block8_aprime)


    return run_hitRates, run_missRates, run_FAs, run_CRs, run_aprimes, specificTypes 






