#!/bin/bash

# PURPOSE: MAKE 1 OVERLAPPING AMYGDALA MASK AND 1 OVERLAPPING BRAIN MASK IN MNI SPACE

#STEPS:

# FOR EACH SUBJECT/SESSION, CONVERT AMYGDALA MASK INTO MNI SPACE W/ NN INTERPOLATION
# MAKE OVERLAP OF ALL SUBJECTS

PROJECT_DIR=/data/jag/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives

# first transform all amygdala files into MNI space
for subjectNumber in "1" "2" "3" "4" "5" "101" "102" "103" "104" "105" "106" "107" "108" ; do
SUBJECT=sub-$(printf "%03d" $subjectNumber)
transform=$PROJECT_DIR/fmriprep/${SUBJECT}/ses-01/anat/${SUBJECT}_ses-01_T1w_target-MNI152NLin2009cAsym_warp.h5

for sessionNumber in "1" "3" ; do
SES=ses-$(printf "%02d" $sessionNumber)
echo $SES
BOLD_DIR=$PROJECT_DIR/fmriprep/${SUBJECT}/${SES}/func
# antsApplyTransforms --default-value 0 --float 1 --interpolation \
# LanczosWindowedSinc -d 3 -e 3 --input {0} --reference-image {1} --output {2}{3}_space-MNI.nii.gz \
# --transform {4}{5}_2ref.txt --transform {6} --transform {7} -v 1 
# .format(full_nifti_name,cfg.MNI_ref_filename,cfg.subject_reg_dir,base_nifti_name,cfg.subject_reg_dir,base_nifti_name,cfg.BOLD_to_T1,cfg.T1_to_MNI)

# conversion: from T1w space --> MNI space
antsApplyTransforms \
-v 0 \
-i $BOLD_DIR/LAMYG.nii.gz \
-r /data/jag/cnds/amennen/rtAttenPenn/MNI_things/mni_icbm152_t1_tal_nlin_asym_09c_BOLD_brain_Penn.nii.gz \
-t [$transform,0] \
-n NearestNeighbor \
-o $BOLD_DIR/LAMYG_in_MNI.nii.gz \

done

done


# GET BRAIN MASK OF MNI SPACE OF ALL SUBJECTS
# MAKE OVERLAP MERGE

# GET LARGE DLPFC MASK
# MAKE OVERLAP MERGEE (can come later)
