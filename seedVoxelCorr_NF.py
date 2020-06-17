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
from nilearn import plotting
import matplotlib.pyplot as plt



def getZCorrelationImg(voxelTimeSeries,runData,brainMasker):
    seed_to_voxel_correlations = (np.dot(voxelTimeSeries.T, runData) /
                              runData.shape[0]
                              )
    seed_to_voxel_correlations_fisher_z = np.arctanh(seed_to_voxel_correlations)

    seed_to_voxel_correlations_fisher_z_img = brain_masker.inverse_transform(
    seed_to_voxel_correlations_fisher_z.T)
    return seed_to_voxel_correlations_fisher_z_img

fmriprep_out="/data/jux/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/fmriprep"
trunc_save_dir = '/data/jux/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/afni/first_level/neurofeedback/trunc'
noise_save_dir = '/data/jux/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/afni/first_level/neurofeedback/clean'
confounds_dir = '/data/jux/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/fsl/first_level/confound_EVs'
whole_brain_mask = '/data/jux/cnds/amennen/rtAttenPenn/MNI_things/mni_icbm152_t1_tal_nlin_asym_09c_BOLD_mask_Penn.nii'
rtAttenPath = '/data/jux/cnds/amennen/rtAttenPenn/fmridata/behavdata/gonogo'
amygdala_mask = '/data/jux/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/mni_anat/LAMYG_in_MNI_overlapping.nii.gz'


subjects = np.array([1,2,3,4,5,6,7,8,9,10,11,101, 102,103,104,105,106, 107,108,109,110,111,112,113,114])

# subjects 106,3,107,4,108 got resting state
#subjectNum = 106
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

        # now extract the specific time points


        brain_time_series_NF_only = brain_time_series[ind_take,:]
        print(np.shape(brain_time_series_NF_only))


        # next: get corresponding 100 TR voxels
        this_run_data = categSep[r,:]
        scene_indices = np.argwhere(this_run_data>0)[:,0]
        face_indices = np.argwhere(this_run_data<0)[:,0]

        # seed_to_voxel_correlations = (np.dot(brain_time_series_NF_only.T, this_run_data) /
        #                               this_run_data.shape[0]
        #                               )
        # seed_to_voxel_correlations_fisher_z = np.arctanh(seed_to_voxel_correlations)

        # seed_to_voxel_correlations_fisher_z_img = brain_masker.inverse_transform(
        #     seed_to_voxel_correlations_fisher_z.T)
        seed_to_voxel_correlations_fisher_z_img = getZCorrelationImg(brain_time_series_NF_only,this_run_data,brain_masker)
        clean_path = noise_save_dir + '/' + bids_id + '/' + ses_id
        if not os.path.exists(clean_path):
            os.makedirs(clean_path)
        full_filename_out = os.path.join(clean_path,'CATEGSEP_seed_correlation_'+run_id+'.nii.gz')
        seed_to_voxel_correlations_fisher_z_img.to_filename(full_filename_out)


        # now do for pos and negative
        n_scene = len(scene_indices)
        brain_pos_NF = brain_time_series_NF_only[scene_indices,:]
        categsep_pos = this_run_data[scene_indices]
        pos_seed_to_voxel_correlations_fisher_z_img = getZCorrelationImg(brain_pos_NF,categsep_pos,brain_masker)
        full_filename_out = os.path.join(clean_path,'CATEGSEP_seed_correlation_POS_'+run_id+'.nii.gz')
        pos_seed_to_voxel_correlations_fisher_z_img.to_filename(full_filename_out)

        n_face = len(face_indices)
        brain_neg_NF = brain_time_series_NF_only[face_indices,:]
        categsep_neg = this_run_data[face_indices]
        neg_seed_to_voxel_correlations_fisher_z_img = getZCorrelationImg(brain_neg_NF,categsep_neg,brain_masker)
        full_filename_out = os.path.join(clean_path,'CATEGSEP_seed_correlation_NEG_'+run_id+'.nii.gz')
        neg_seed_to_voxel_correlations_fisher_z_img.to_filename(full_filename_out)

        # print( np.shape(seed_to_voxel_correlations))
        # print("Seed-to-voxel correlation: min = %.3f; max = %.3f" % (
        #     seed_to_voxel_correlations.min(), seed_to_voxel_correlations.max()))
        # print("Seed-to-voxel correlation Fisher-z transformed: min = %.3f; max = %.3f"
        #       % (seed_to_voxel_correlations_fisher_z.min(),
        #          seed_to_voxel_correlations_fisher_z.max()
        #          )
        #       )
        # seed_to_voxel_correlations_img = brain_masker.inverse_transform(
        #     seed_to_voxel_correlations.T)
        # display = plotting.plot_stat_map(seed_to_voxel_correlations_img,bg_img=whole_brain_mask,
        #                                  title="Seed-to-voxel correlation (PCC seed)"
        #                                  )
        # plt.show()