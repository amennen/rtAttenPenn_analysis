# make master resting state script for given number of subjects
# PURPOSE: make sure all subjects are included in case you need to rerun

# Steps:
# 1. update FD text files: ses 1, ses 3, average over ses 1 and ses 3 (DONE)
# 2. check if confounds exist or not, if they don't --> update them (DONE)
# 3. check if AFNI_3dttproject (AFNI_resting.py) has been run --> if not run it on subject (DONE)
# 4. Make new amygdala mask including all subjects (DONE)
# 5. Run get_average_amyg_resting_and_corr.py for all subjects (delete previous files) (DONE)
# 6. Run 3dttest with those subjects and given mask


import glob
import os
import pandas as pd
import numpy as np
from subprocess import call
import nilearn.masking

fmriprep_out="/data/jux/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/fmriprep"
reg_save_dir='/data/jux/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/resting/confound_EVs'
trunc_save_dir = '/data/jux/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/resting/trunc'
noise_save_dir = '/data/jux/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/resting/clean'
second_level = noise_save_dir + '/' + 'group_level'
FP_mask = '/data/jux/cnds/amennen/rtAttenPenn/MNI_things/Yeo2011_6Network_mask_reoriented_resampled.nii.gz'
FP_mask = '/data/jux/cnds/amennen/rtAttenPenn/MNI_things/Yeo2011_6Network_mask_reoriented_resampled.nii.gz'
COMMON_DIR='/data/jux/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/mni_anat'
common_base = 'dlPFC_in_MNI'
dlPFC_mask = COMMON_DIR + '/' + common_base + '_overlapping' + '.nii.gz'
amyg_base = 'LAMYG_in_MNI'
amyg_mask = COMMON_DIR + '/' + 'LAMYG_in_MNI' + '_overlapping.nii.gz'

def getMeanFD_rest(subjectNum,subjectDay):
    fmriprep_out="/data/jux/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/fmriprep"
    ses_id = 'ses-{0:02d}'.format(subjectDay)
    bids_id = 'sub-{0:03d}'.format(subjectNum)
    day_path=os.path.join(fmriprep_out,bids_id,ses_id, 'func')
    fn = glob.glob(os.path.join(day_path, '*task-rest*confounds.tsv'))
    nToDelete = 4
    z = pd.read_csv(fn[0], sep='\t')
    FD = z['FramewiseDisplacement']
    meanFD = np.mean(FD[nToDelete:])
    return meanFD

def makeFD_mat(subjectVec,savePath):
    columns = ['subj', 'FD']
    nsub = len(subjectVec)

    sessions = [1,3]
    data_ses1 = []
    data_ses2 = []
    data_avg = []
    for s in np.arange(nsub):
        subjectNum = subjectVec[s]
        bids_id = 'sub-{0:03d}'.format(subjectNum)
        meanFD1 = getMeanFD_rest(subjectNum,1)
        meanFD2 = getMeanFD_rest(subjectNum,3)
        avg_FD = np.mean([meanFD1,meanFD2])

        data_ses1.append((bids_id,meanFD1))
        data_ses2.append((bids_id,meanFD2))
        data_avg.append((bids_id,avg_FD))

    df1 = pd.DataFrame(data=data_ses1,columns=columns)
    ses_id = 'ses-{0:02d}'.format(1)
    df1.to_csv(os.path.join(savePath,'FD_covar_{0}.txt'.format(ses_id)), sep = ' ', index=False)

    df2 = pd.DataFrame(data=data_ses2,columns=columns)
    ses_id = 'ses-{0:02d}'.format(3)
    df1.to_csv(os.path.join(savePath,'FD_covar_{0}.txt'.format(ses_id)), sep = ' ', index=False)

    df = pd.DataFrame(data=data_avg,columns=columns)
    df.to_csv(os.path.join(savePath,'FD_covar_SES_mean.txt'), sep = ' ', index=False)

def createDerivativeConfounds(subjectNum,fmriprep_out,reg_save_dir,trunc_save_dir):
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

                            dest_path = reg_save_dir + '/' + bids_id + '/' + ses_id
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
                            command = 'fslroi %s %s %i %i' % (rest_nifti,full_save_path,nToDelete,np.shape(MASTERDF)[0])
                            call(command,shell=True)

def run_3dTproject(subjectNum,reg_save_dir,trunc_save_dir,noise_save_dir):
    bids_id = 'sub-{0:03d}'.format(subjectNum)
    print(bids_id)
    sessions = [1,3]
    for s in sessions:
        subjectDay = s
        ses_id = 'ses-{0:02d}'.format(subjectDay)
        print(ses_id)
        # get regression file 
        confounds_path = reg_save_dir + '/' + bids_id + '/' + ses_id
        confound_fn = glob.glob(os.path.join(confounds_path, '*.1D'))
        confound_fn = confound_fn[0]

        # get nifti file
        nifti_path = trunc_save_dir + '/' + bids_id + '/' + ses_id
        nifti_fn = glob.glob(os.path.join(nifti_path, '*.nii.gz'))
        nifti_fn = nifti_fn[0]

        # specify where to save cleaned version
        subj_clean_path = noise_save_dir + '/' + bids_id + '/' + ses_id
        if not os.path.exists(subj_clean_path):
            os.makedirs(subj_clean_path)

        command = ("3dTproject -polort 2 -blur 6 -passband 0.01 0.08 "
                        "-input {0} ".format(nifti_fn) +
                        "-ort {0} ".format(confound_fn) +
                        "-prefix {0}/{1}_{2}_task_rest_glm.nii.gz".format(subj_clean_path,bids_id,ses_id))
        call(command,shell=True)

def create_overlapping_masks(subjectVec,mask,fmriprep_out,COMMON_DIR):
    all_masks_list = []
    for s in np.arange(len(subjectVec)):
        bids_id = 'sub-{0:03d}'.format(subjectVec[s])
        for ses in np.array([1,3]):
            ses_id = 'ses-{0:02d}'.format(ses)
            if mask == 'whole_brain':
                subject_mask = fmriprep_out + '/' + bids_id + '/' + ses_id + '/' + 'func' + '/' + bids_id + '_' + ses_id + '_task-faces_rec-uncorrected_run-01_bold_space-MNI152NLin2009cAsym_brainmask.nii.gz'
            else:
                subject_mask = fmriprep_out + '/' + bids_id + '/' + ses_id + '/' + 'func' + '/' + mask
            all_masks_list.append(subject_mask)
    if mask == 'dlPFC_in_MNI.nii.gz':
        threshold = 0.5
    elif mask == 'LAMYG_in_MNI.nii.gz':
        threshold = 0.5 # to if it aligns with at least half of the subjects
    elif mask == 'whole_brain':
        threshold = 1 # to only keep the things that align in everyone
    common = nilearn.masking.intersect_masks(all_masks_list, threshold=threshold, connected=False)
    common_base = mask.split('.')[0]
    full_common_path = COMMON_DIR + '/' + common_base + '_overlapping' + '.nii.gz'
    common.to_filename(full_common_path)
    return full_common_path

def run_get_average_amg_resting_and_corr(subjectNum,noise_save_dir,mask_name):
    bids_id = 'sub-{0:03d}'.format(subjectNum)
    sessions = [1,3]
    for s in sessions:
        subjectDay = s
        ses_id = 'ses-{0:02d}'.format(subjectDay)
        print(ses_id)

        # specify where to save cleaned version
        subj_clean_path = noise_save_dir + '/' + bids_id + '/' + ses_id
        preproc_output = "{0}/{1}_{2}_task_rest_glm.nii.gz".format(subj_clean_path,bids_id,ses_id)
        saved_average = "{0}/{1}_{2}_task_rest_LAMYG_avg".format(subj_clean_path,bids_id,ses_id)
        command = ("3dmaskave -quiet -mask {0} {1} > {2}.1D".format(mask_name,preproc_output,saved_average))
        call(command,shell=True)

        # now create correlation matrix
        saved_correlation = "{0}/{1}_{2}_task_rest_corr_LAMYG.nii.gz".format(subj_clean_path,bids_id,ses_id)
        command = ("3dfim+ -bucket {0} -fim_thr 0 -out Correlation -ideal_file {1}.1D -input {2}".format(saved_correlation,saved_average,preproc_output))
        call(command,shell=True)

        # transform to z transform
        saved_z = "{0}/{1}_{2}_task_rest_corr_r2z_LAMYG.nii.gz".format(subj_clean_path,bids_id,ses_id)
        command = ("3dcalc -a {0} -expr 'log((1+a)/(1-a))/2' -prefix {1}".format(saved_correlation,saved_z))
        call(command,shell=True)


#### MAIN ANALYSES HERE

HC_subjects = [3 ,4 ,5 ,6,7,8,9,10,11]
MDD_subjects = [106 ,107 ,108 ,109,110,111,112,113,114]
all_subjects = HC_subjects + MDD_subjects
nSubjects = len(all_subjects)
makeFD_mat(all_subjects,second_level)
sessions = [1,3]
# check if all confound files exist for all subjects (just check ses 3) --> if they don't --> make them for that subject
for s in np.arange(nSubjects):
    subjectNum = all_subjects[s]
    bids_id = 'sub-{0:03d}'.format(subjectNum)
    ses_id = 'ses-{0:02d}'.format(3)
    confound_file = glob.glob(reg_save_dir + '/' + bids_id + '/' + ses_id + '/' + '*.1D')
    if len(confound_file) == 0:
        print('CREATING CONFOUNDS FOR SUBJECT %i' % subjectNum)
        createDerivativeConfounds(subjectNum,fmriprep_out,reg_save_dir,trunc_save_dir)
    elif len(confound_file) == 1:
        print('FOUND CONFOUNDS FOR SUBJECT %i' % subjectNum)

# next: check if 3dTproject has been run for each subject --> if not, rerun
for s in np.arange(nSubjects):
    subjectNum = all_subjects[s]
    bids_id = 'sub-{0:03d}'.format(subjectNum)
    ses_id = 'ses-{0:02d}'.format(3)
    subj_clean_path = noise_save_dir + '/' + bids_id + '/' + ses_id
    cleaned_nifti = glob.glob(subj_clean_path + '/' + '*task_rest_glm.nii.gz')
    print(subjectNum)
    print(len(cleaned_nifti))
    if len(cleaned_nifti) == 0:
        print('RUNNING 3dTproject FOR SUBJECT %i' % subjectNum)
        # WILL RUN FOR BOTH SESSIONS
        run_3dTproject(subjectNum,reg_save_dir,trunc_save_dir,noise_save_dir)
    else:
        print('FOUND 3dTproject OUTPUT FOR SUBJECT %i' % subjectNum)
# for new subject - run reg_aparcaseg_updated.sh after editing for new subject
# reg_amyg and reg_dlpfc too
# next: delete old amygdala mask and make a new one, then run overlapping for all subjects
if os.path.isfile(amyg_mask):
    print('DELETING PREVIOUS AMYG MASK')
    cmd = 'rm {0}'.format(amyg_mask)
    call(cmd,shell=True)
mask = amyg_base+'.nii.gz'
mask_name = create_overlapping_masks(all_subjects,mask,fmriprep_out,COMMON_DIR)


# next: Run get_average_amyg_resting_and_corr.py for all subjects (delete if already exist)
for s in np.arange(nSubjects):
    subjectNum = all_subjects[s]
    bids_id = 'sub-{0:03d}'.format(subjectNum)
    # first go through each day and delete sessions
    for ses in sessions:
        ses_id = 'ses-{0:02d}'.format(ses)
        subj_clean_path = noise_save_dir + '/' + bids_id + '/' + ses_id
        saved_average = "{0}/{1}_{2}_task_rest_LAMYG_avg.1D".format(subj_clean_path,bids_id,ses_id)
        if os.path.isfile(saved_average):
            print('FOUND AMYG OUTPUT FOR SUBJECT %i -- DELETING FIRST' % subjectNum)
            cmd = 'rm {0}'.format(saved_average)
            call(cmd,shell=True)
            #cmd = 'rm {0}/{1}_{2}_task_rest_glm.nii.gz'.format(subj_clean_path,bids_id,ses_id)
            #call(cmd,shell=True)
            cmd = "rm {0}/{1}_{2}_task_rest_corr_LAMYG.nii.gz".format(subj_clean_path,bids_id,ses_id)
            call(cmd,shell=True)
            cmd = "rm {0}/{1}_{2}_task_rest_corr_r2z_LAMYG.nii.gz".format(subj_clean_path,bids_id,ses_id)
            call(cmd,shell=True)
    run_get_average_amg_resting_and_corr(subjectNum,noise_save_dir,mask_name)

# NOW READY TO RUN GROUP ANALYSES!
# call qsub command to run AFNI_3dttest -- > make sure using same dlpfc mask as with faces task
