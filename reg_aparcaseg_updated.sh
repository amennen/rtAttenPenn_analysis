#!/bin/bash
#
# purpose: register given aparc.aseg.mgz files to given functional day to later use for ROIs
# For given subject, will go through their fmriprep folder to register for each day, 
# saving in that day's func folder

# NEW: have it so it uses the updated registration method

set -e

make_amygdala=1
make_mfg=0
make_dlpfc=1
register_new_subject=1


PROJECT_DIR=/data/jux/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives

#for subjectNumber in "1" "2" "3" "4" "5" "7" "101" "102" "103" "104" "105" "106" "107" "108" "109" ; do
for subjectNumber in  "12" ; do
#for subjectNumber in "112" ; do
SUBJECT=sub-$(printf "%03d" $subjectNumber)
echo $SUBJECT
FREESURFER_DIR=$PROJECT_DIR/freesurfer/$SUBJECT/mri

# have it register to the first functional run, whatever the functional run is (faces for 1/3, gonogo 1 on ses 2)
#make sure to eat vegeteables everyday

for sessionNumber in `seq 1 3`; do
SES=ses-$(printf "%02d" $sessionNumber)
echo $SES
BOLD_DIR=$PROJECT_DIR/fmriprep/${SUBJECT}/${SES}/func
if [ $sessionNumber -eq 1 ]
then
BOLD_EX=$BOLD_DIR/${SUBJECT}_${SES}_task-faces_rec-uncorrected_run-01_bold_space-T1w_preproc.nii.gz
MASK_EX=$BOLD_DIR/${SUBJECT}_${SES}_task-faces_rec-uncorrected_run-01_bold_space-T1w_brainmask.nii.gz
else
BOLD_EX=$BOLD_DIR/${SUBJECT}_${SES}_task-gonogo_rec-uncorrected_run-01_bold_space-T1w_preproc.nii.gz
MASK_EX=$BOLD_DIR/${SUBJECT}_${SES}_task-gonogo_rec-uncorrected_run-01_bold_space-T1w_brainmask.nii.gz
fi

if [ $register_new_subject -eq 1 ]
then
	fslmaths $BOLD_EX -Tmean -mas $MASK_EX $BOLD_DIR/fmriprep_BOLD_T1w_preproc_Tmean.nii.gz
	mri_convert $BOLD_DIR/fmriprep_BOLD_T1w_preproc_Tmean.nii.gz $BOLD_DIR/fmriprep_BOLD_T1w_preproc_Tmean.mgz
	# NEW:
	mri_label2vol --seg $FREESURFER_DIR/aparc+aseg.mgz --temp $BOLD_DIR/fmriprep_BOLD_T1w_preproc_Tmean.mgz \
		--o $BOLD_DIR/aparc+aseg-in-BOLD.nii.gz --fillthresh 0.5 --regheader $FREESURFER_DIR/aparc+aseg.mgz
	mri_label2vol --seg $FREESURFER_DIR/aparc.a2009s+aseg.mgz --temp $BOLD_DIR/fmriprep_BOLD_T1w_preproc_Tmean.mgz \
		--o $BOLD_DIR/aparc.a2009+aseg-in-BOLD.nii.gz --fillthresh 0.5 --regheader $FREESURFER_DIR/aparc.a2009s+aseg.mgz
fi
# check registration
#fslview $BOLD_DIR/aparc+aseg-in-BOLD.nii.gz $BOLD_DIR/${SUBJECT}_${SES}_task-gonogo_rec-uncorrected_run-01_bold_space-T1w_label-aparcaseg_roi.nii.gz


#mri_convert -rl $BOLD_DIR/fmriprep_BOLD_T1w_preproc_Tmean.mgz -rt nearest $FREESURFER_DIR/aparc+aseg.mgz $BOLD_DIR/aparc+aseg_CONVERTED2BOLD.nii.gz
#mri_convert -rl $BOLD_DIR/fmriprep_BOLD_T1w_preproc_Tmean.mgz -rt nearest $FREESURFER_DIR/aparc.a2009s+aseg.mgz $BOLD_DIR/aparc.a2009+aseg_CONVERTED2BOLD.nii.gz

# for amygdala masks: 
if [ $make_amygdala -eq 1 ]
then
	fslmaths $BOLD_DIR/aparc+aseg-in-BOLD.nii.gz -thr 18 -uthr 18 -bin $BOLD_DIR/LAMYG.nii.gz
	fslmaths $BOLD_DIR/aparc+aseg-in-BOLD.nii.gz  -thr 54 -uthr 54 -bin $BOLD_DIR/RAMYG.nii.gz
	# at first didn't binarize but didn't matter because they weren't overlapping at all but this is for the future
	fslmaths $BOLD_DIR/LAMYG.nii.gz -add $BOLD_DIR/RAMYG.nii.gz -bin $BOLD_DIR/AMYG.nii.gz
fi

if [ $make_mfg -eq 1 ]
then
	fslmaths $BOLD_DIR/aparc.a2009+aseg-in-BOLD.nii.gz -thr 11115 -uthr 11115 -bin $BOLD_DIR/LMFG.nii.gz
	fslmaths $BOLD_DIR/aparc.a2009+aseg-in-BOLD.nii.gz  -thr 12115 -uthr 12115 -bin $BOLD_DIR/RMFG.nii.gz
	# at first didn't binarize but didn't matter because they weren't overlapping at all but this is for the future
	fslmaths $BOLD_DIR/LMFG.nii.gz -add $BOLD_DIR/RMFG.nii.gz -bin $BOLD_DIR/MFG.nii.gz
fi

if [ $make_dlpfc -eq 1 ]
then
        fslmaths $BOLD_DIR/aparc.a2009+aseg-in-BOLD.nii.gz -thr 11115 -uthr 11115 -bin $BOLD_DIR/LMFG.nii.gz
        fslmaths $BOLD_DIR/aparc.a2009+aseg-in-BOLD.nii.gz  -thr 12115 -uthr 12115 -bin $BOLD_DIR/RMFG.nii.gz
        fslmaths $BOLD_DIR/aparc.a2009+aseg-in-BOLD.nii.gz -thr 11116 -uthr 11116 -bin $BOLD_DIR/LSFG.nii.gz
        fslmaths $BOLD_DIR/aparc.a2009+aseg-in-BOLD.nii.gz -thr 12116 -uthr 12116 -bin $BOLD_DIR/RSFG.nii.gz
        fslmaths $BOLD_DIR/aparc.a2009+aseg-in-BOLD.nii.gz -thr 11153 -uthr 11153 -bin $BOLD_DIR/LIFS.nii.gz
        fslmaths $BOLD_DIR/aparc.a2009+aseg-in-BOLD.nii.gz -thr 12153 -uthr 12153 -bin $BOLD_DIR/RIFS.nii.gz
        fslmaths $BOLD_DIR/aparc.a2009+aseg-in-BOLD.nii.gz -thr 11154 -uthr 11154 -bin $BOLD_DIR/LMFS.nii.gz
        fslmaths $BOLD_DIR/aparc.a2009+aseg-in-BOLD.nii.gz -thr 12154 -uthr 12154 -bin $BOLD_DIR/RMFS.nii.gz
        fslmaths $BOLD_DIR/aparc.a2009+aseg-in-BOLD.nii.gz -thr 11155 -uthr 11155 -bin $BOLD_DIR/LSFS.nii.gz
        fslmaths $BOLD_DIR/aparc.a2009+aseg-in-BOLD.nii.gz -thr 12155 -uthr 12155 -bin $BOLD_DIR/RSFS.nii.gz
        # at first didn't binarize but didn't matter because they weren't overlapping at all but this is for the future
        fslmaths $BOLD_DIR/LMFG.nii.gz -add $BOLD_DIR/RMFG.nii.gz -add $BOLD_DIR/LSFG.nii.gz -add $BOLD_DIR/RSFG.nii.gz -add $BOLD_DIR/LIFS.nii.gz -add $BOLD_DIR/RIFS.nii.gz -add $BOLD_DIR/LMFS.nii.gz -add $BOLD_DIR/RMFS.nii.gz -add $BOLD_DIR/LSFS.nii.gz -add $BOLD_DIR/RSFS.nii.gz -bin $BOLD_DIR/dlPFC.nii.gz
fi


done


done

