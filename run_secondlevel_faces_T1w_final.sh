#!/bin/bash
#
# render-fsf-templates.sh fills in templated fsf files so FEAT can use them
# original author: mason simon (mgsimon@princeton.edu)
# this script was provided by NeuroPipe. modify it to suit your needs
#
# refer to the secondlevel neuropipe tutorial to see an example of how
# to use this script

set -e

FIRSTLEVEL_DIR=/data/jag/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/fsl/first_level
FMRIPREP_DIR=/data/jag/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/fmriprep
SECONDLEVEL_DIR=/data/jag/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/fsl/second_level

subjectNumber=$1
SUBJECT=sub-$(printf "%03d" $subjectNumber)
SUBJECT_DIR=$SECONDLEVEL_DIR/${SUBJECT}


sessionNumber=1
SES=ses-$(printf "%02d" $sessionNumber)
echo "Running for $SUBJECT : $SES"
feat $SUBJECT_DIR/${SES}/faces_T1w_final.fsf

sessionNumber=3
SES=ses-$(printf "%02d" $sessionNumber)
echo "Running for $SUBJECT : $SES"
feat $SUBJECT_DIR/${SES}/faces_T1w_final.fsf

