#!/bin/bash

PROJECT_DIR=/data/jux/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives
COMMON_AMYG=/data/jux/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/mni_anat/LAMYG_in_MNI_overlapping.nii.gz # where to save
for subjectNumber in "1" "2" "3" "4" "5" "101" "102" "103" "104" "105" "106" "107" "108" ; do
SUBJECT=sub-$(printf "%03d" $subjectNumber)

for sessionNumber in "1" "3" ; do
SES=ses-$(printf "%02d" $sessionNumber)
echo $SES
BOLD_DIR=$PROJECT_DIR/fmriprep/${SUBJECT}/${SES}/func
# do for each run
for runNumber in "1" "2" ; do
RUN=run-$(printf "%02d" $runNumber)
FSL_DIR=${PROJECT_DIR}/fsl/first_level/${SUBJECT}/${SES}/faces${runNumber}_MNI.feat
filtered_data=${FSL_DIR}/filtered_func_data.nii.gz
fslmeants -i $filtered_data -m $COMMON_AMYG -o ${FSL_DIR}/LAMYG_meants_task-faces_${RUN}.txt

done 
done

done
