#!/bin/bash

# Purpose: register given cope to MNI template for group analysis


set -e

MASK_DIR=/data/jag/cnds/amennen/rtAttenPenn/MNI_things
FIRSTLEVEL_DIR=/data/jag/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/fsl/first_level
FMRIPREP_DIR=/data/jag/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/fmriprep
FSF_DIR=$FIRSTLEVEL_DIR/fsf
SECONDLEVEL_DIR=/data/jag/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/fsl/second_level

subjectNumber=$1
SUBJECT=sub-$(printf "%03d" $subjectNumber)
SUBJECT_DIR=$SECONDLEVEL_DIR/${SUBJECT}
SUBJECT_ANAT_DIR=${FMRIPREP_DIR}/${SUBJECT}/ses-01/anat

# do this for both sessions

sessionNumber=1
SES=ses-$(printf "%02d" $sessionNumber)
SES_DIR=${SUBJECT_DIR}/${SES}

for c in 5 6
do
	# make a fake feats folder
	echo " cope number is: $c"
	FEAT_DIR=${SES_DIR}/faces_T1w_final.gfeat/cope${c}.feat/stats
	FAKE_FEAT_DIR=${SES_DIR}/faces_T1w_final_space-MNI152NLin2009cAsym.gfeat/cope${c}.feat/stats
	mkdir -pv $FAKE_FEAT_DIR

	COPE_IMG=${FEAT_DIR}/cope1.nii.gz
	antsApplyTransforms -i ${FEAT_DIR}/cope1.nii.gz -r ${MASK_DIR}/mni_icbm152_t1_tal_nlin_asym_09c_BOLD_brain_Penn.nii.gz \
	-t [${SUBJECT_ANAT_DIR}/${SUBJECT}_${SES}_T1w_target-MNI152NLin2009cAsym_warp.h5,0] \
	-n NearestNeighbor -o ${FAKE_FEAT_DIR}/cope1_space-MNI152NLin2009cAsym.nii.gz
done

# TO DO: DOWNLOAD MNI template and make into BOLD slicing and resolution*** do it on scotty and then save in Penn!!

