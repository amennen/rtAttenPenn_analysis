#!/bin/bash
#
# purpose: register given aparc.aseg.mgz files to given functional day to later use for ROIs
# For given subject, will go through their fmriprep folder to register for each day, 
# saving in that day's func folder

set -e

make_amygdala=1

PROJECT_DIR=/data/jag/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives

#for subjectNumber in "1" "2" "101" "102" ; do
for subjectNumber in "106" ; do
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

fslmaths $BOLD_EX -Tmean -mas $MASK_EX $BOLD_DIR/fmriprep_BOLD_T1w_preproc_Tmean.nii.gz
mri_convert $BOLD_DIR/fmriprep_BOLD_T1w_preproc_Tmean.nii.gz $BOLD_DIR/fmriprep_BOLD_T1w_preproc_Tmean.mgz
mri_convert -rl $BOLD_DIR/fmriprep_BOLD_T1w_preproc_Tmean.mgz -rt nearest $FREESURFER_DIR/aparc+aseg.mgz $BOLD_DIR/aparc+aseg_CONVERTED2BOLD.nii.gz
mri_convert -rl $BOLD_DIR/fmriprep_BOLD_T1w_preproc_Tmean.mgz -rt nearest $FREESURFER_DIR/aparc.a2009s+aseg.mgz $BOLD_DIR/aparc.a2009+aseg_CONVERTED2BOLD.nii.gz

# for amygdala masks: 
if [ $make_amygdala -eq 1 ]
then
	fslmaths $BOLD_DIR/aparc+aseg_CONVERTED2BOLD.nii.gz -thr 18 -uthr 18 -bin $BOLD_DIR/LAMYG.nii.gz
	fslmaths $BOLD_DIR/aparc+aseg_CONVERTED2BOLD.nii.gz  -thr 54 -uthr 54 -bin $BOLD_DIR/RAMYG.nii.gz
	# at first didn't binarize but didn't matter because they weren't overlapping at all but this is for the future
	fslmaths $BOLD_DIR/LAMYG.nii.gz -add $BOLD_DIR/RAMYG.nii.gz -bin $BOLD_DIR/AMYG.nii.gz
fi
done


done
