import os
import glob
from shutil import copyfile
import pandas as pd
import json
import numpy as np
from subprocess import call
import sys
import nilearn
from nilearn.image import new_img_like, load_img
from nilearn.input_data import NiftiMasker
from nilearn import plotting,masking
import matplotlib.pyplot as plt



def getZCorrelationImg(voxelTimeSeries,runData,brainMasker):
    seed_to_voxel_correlations = (np.dot(voxelTimeSeries.T, runData) /
                              runData.shape[0]
                              )
    seed_to_voxel_correlations_fisher_z = np.arctanh(seed_to_voxel_correlations)

    seed_to_voxel_correlations_fisher_z_img = brain_masker.inverse_transform(
    seed_to_voxel_correlations_fisher_z.T)
    return seed_to_voxel_correlations_fisher_z_img

def transition_matrix_shift(transitions,nstates,nshift):
    n=nstates
    transition_dict={}
    M = [[0]*n for _ in range(n)]
    index=0
    for (i,j) in zip(transitions,transitions[nshift:]):
        M[i][j] += 1
        if (i,j) not in transition_dict.keys():
            # this means hasn't been initialized yet so we have to initialize
            transition_dict[(i,j)] = []
        transition_dict[(i,j)] = transition_dict[(i,j)] + [index]
        index+=1

    #now convert to probabilities:
    for row in M:
        s = sum(row)
        if s > 0:
            row[:] = [f/s for f in row]
    return M,transition_dict


def change_percent(current,previous):
    percent_change = ((float(current)-previous)/previous)*100
    return percent_change

def change_subtract(current,previous):
    change = current - previous
    return change


def calculateTransitionMatrixForRun(this_run_data,nshift1,nshift2,bins):
    nbins=len(bins)
    indices = np.digitize(this_run_data,bins)
    indices[np.argwhere(indices==len(bins))] = len(bins) - 1
    indices_0ind = indices.copy() - 1
    M1,td1 = transition_matrix_shift(indices_0ind,nbins-1,nshift1)
    M2,td2 = transition_matrix_shift(indices_0ind,nbins-1,nshift2)
    return td1,td2

def calculate_amg_change_per_matrix(amygdala_timecourse,td1,td2,nshift1,nshift2,bins):
    # average the results from shifting 2 and 3 TRs together
    # first td1
    
    nbins=len(bins)
    nstates=nbins-1

    n_transitions_run = len(td1.keys())
    #AMYG_1 = [[np.nan]*nstates for _ in range(nstates)]
    AMYG_1 = np.zeros((nstates,nstates)) *np.nan
    for this_transition in td1.keys():
        #print(this_transition)
        this_transition_indices = td1[this_transition]
        n_indices = len(this_transition_indices)
        amyg_change = np.zeros((n_indices,))
        for t in np.arange(n_indices):
            index1 = this_transition_indices[t]
            index2 = this_transition_indices[t]+nshift1
            amyg_change[t] = change_subtract(amygdala_timecourse[index2],amygdala_timecourse[index1])
        # now get average change for that transition
        average_amyg_change = np.mean(amyg_change)
        array_this_transition = np.array(this_transition)
        AMYG_1[array_this_transition[0],array_this_transition[1]] = average_amyg_change


    # now repeat for nshift2
    n_transitions_run = len(td2.keys())
    #AMYG_2 = [[np.nan]*nstates for _ in range(nstates)]
    AMYG_2 = np.zeros((nstates,nstates)) *np.nan

    for this_transition in td2.keys():
        #print(this_transition)
        this_transition_indices = td2[this_transition]
        n_indices = len(this_transition_indices)
        amyg_change = np.zeros((n_indices,))
        for t in np.arange(n_indices):
            index1 = this_transition_indices[t]
            index2 = this_transition_indices[t]+nshift2
            amyg_change[t] = change_subtract(amygdala_timecourse[index2],amygdala_timecourse[index1])
        # now get average change for that transition
        average_amyg_change = np.mean(amyg_change)
        AMYG_2[this_transition[0],this_transition[1]] = average_amyg_change
    # now average both together
    M_combined = np.concatenate((AMYG_1[:,:,np.newaxis],AMYG_2[:,:,np.newaxis]),axis=2)
    M = np.nanmean(M_combined,axis=2)
    return M # so this is for a specific run!



fmriprep_out="/data/jux/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/fmriprep"
trunc_save_dir = '/data/jux/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/afni/first_level/neurofeedback/trunc'
noise_save_dir = '/data/jux/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/afni/first_level/neurofeedback/clean'
confounds_dir = '/data/jux/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/fsl/first_level/confound_EVs'
whole_brain_mask = '/data/jux/cnds/amennen/rtAttenPenn/MNI_things/mni_icbm152_t1_tal_nlin_asym_09c_BOLD_mask_Penn.nii'
rtAttenPath = '/data/jux/cnds/amennen/rtAttenPenn/fmridata/behavdata/gonogo'
amygdala_mask = '/data/jux/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/mni_anat/LAMYG_in_MNI_overlapping.nii.gz'


subjects = np.array([1,2,3,4,5,6,7,8,9,10,11,101, 102,103,104,105,106, 107,108,109,110,111,112,113,114])
bins = [-1.   , -0.975, -0.9, -0.8 ,-0.7,-0.55,-0.4,-0.2,0,0.2,0.4,0.55,0.7, 0.8 ,  0.9 , 0.975, 1. ]
nbins=len(bins)

subjectNum = np.int(sys.argv[1])
bids_id = 'sub-{0:03d}'.format(subjectNum)
print(bids_id)
sessions = [1,2,3]
TRshift=2
all_time_points = np.zeros((232,)).astype(int)
x1 = np.arange(116,141) + TRshift
x2 = np.arange(144,169) + TRshift
x3 = np.arange(172,197) + TRshift
x4 = np.arange(200,225) + TRshift
all_time_points[x1] = 1
all_time_points[x2] = 1
all_time_points[x3] = 1
all_time_points[x4] = 1
ind_take = np.argwhere(all_time_points)[:,0]
d1_runs = 6
d2_runs = 8
d3_runs = 7
nshift1=2
nshift2=3
nstates=nbins-1

all_amg_changes = np.zeros((nstates,nstates,8,len(sessions)))
for subjectDay in sessions:
    ses_id = 'ses-{0:02d}'.format(subjectDay)
    print(ses_id)
    # now get the number of neurofeedback runs by looking in the confounds folder
    confounds_path = confounds_dir + '/' + bids_id + '/' + ses_id
    #fmriprep_path = fmriprep_out + '/' + bids_id + '/' + ses_id + '/' +'func'
    trunc_path = trunc_save_dir + '/' + bids_id + '/' + ses_id
    # now get all the nf runs
    all_NF_runs = glob.glob(os.path.join(confounds_path, '*task-gonogo_rec-uncorrected*.1D'))
    n_runs = len(all_NF_runs)


    subjectDir = rtAttenPath + '/' + 'subject' + str(subjectNum)
    outfile = subjectDir + '/' 'offlineAUC_RTCS.npz'    
    z=np.load(outfile)
    if subjectNum == 106:
        d1_runs = 5
    else:
        d1_runs = 6
    CS = z['csOverTime'] # n NF runs x 100 TRs x 3 days
    nTR = np.shape(CS)[1]

    if subjectDay==1:
        categSep = CS[0:d1_runs,:,0]
        nRuns = d1_runs
    elif subjectDay==2:
        categSep = CS[0:d2_runs,:,1]
        nRuns = d2_runs
    elif subjectDay==3:
        categSep = CS[0:d3_runs,:,2]
        nRuns = d3_runs

    for r in np.arange(nRuns):
        run_id = 'run-{0:02d}'.format(r+2)
        print(run_id)
        confound_fn = glob.glob(os.path.join(confounds_path, '*gonogo_rec-uncorrected_'+run_id+'*.tsv'))[0]
        fmriprep_fn = glob.glob(os.path.join(trunc_path,'*task-gonogo_rec-uncorrected_' + run_id +'_bold_space-MNI*preproc*'))[0]

        brain_masker = NiftiMasker(smoothing_fwhm=5,detrend=False,standardize=True,high_pass=0.005,t_r=2,verbose=0,mask_img=whole_brain_mask)
        brain_time_series = brain_masker.fit_transform(fmriprep_fn,
                                               confounds=[confound_fn])
        print(np.shape(brain_time_series)) # now 232 by nvoxels masked

        brain_time_series_NF_only = brain_time_series[ind_take,:]
        print(np.shape(brain_time_series_NF_only))
        # now we want to convert this back so we can extract amygdala data
        brain_time_series_NF_3D = brain_masker.inverse_transform(brain_time_series_NF_only)
        amyg_ts = nilearn.masking.apply_mask(brain_time_series_NF_3D,amygdala_mask) # now 100 x 19 voxels
        # average over 19 voxels
        average_amygdala_ts = np.mean(amyg_ts,axis=1)
        # next: get corresponding 100 TR voxels
        this_run_data = categSep[r,:]
        # get transitions
        td1,td2=calculateTransitionMatrixForRun(this_run_data,nshift1,nshift2,bins)
        M = calculate_amg_change_per_matrix(average_amygdala_ts,td1,td2,nshift1,nshift2,bins)

        all_amg_changes[:,:,r,subjectDay-1] = M

save_path = "{0}/{1}/{2}/amygdala_changes.npy".format(noise_save_dir,bids_id,ses_id)
np.save(save_path,all_amg_changes)



