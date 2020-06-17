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
FSF_DIR=$FIRSTLEVEL_DIR/fsf

subjectNumber=$1
SUBJECT=sub-$(printf "%03d" $subjectNumber)
SUBJECT_DIR=$FIRSTLEVEL_DIR/${SUBJECT}


sessionNumber=1
SES=ses-$(printf "%02d" $sessionNumber)
runNumber=1
RUN=run-$(printf "%02d" $runNumber)
echo "Running for $SUBJECT : $SES : $RUN"
feat $SUBJECT_DIR/${SES}/faces${runNumber}_MNI.fsf

sessionNumber=1
SES=ses-$(printf "%02d" $sessionNumber)
runNumber=2
RUN=run-$(printf "%02d" $runNumber)
echo "Running for $SUBJECT : $SES : $RUN"
feat $SUBJECT_DIR/${SES}/faces${runNumber}_MNI.fsf

sessionNumber=3
SES=ses-$(printf "%02d" $sessionNumber)
runNumber=1
RUN=run-$(printf "%02d" $runNumber)
echo "Running for $SUBJECT : $SES : $RUN"
feat $SUBJECT_DIR/${SES}/faces${runNumber}_MNI.fsf

sessionNumber=3
SES=ses-$(printf "%02d" $sessionNumber)
runNumber=2
RUN=run-$(printf "%02d" $runNumber)
echo "Running for $SUBJECT : $SES : $RUN"
feat $SUBJECT_DIR/${SES}/faces${runNumber}_MNI.fsf
