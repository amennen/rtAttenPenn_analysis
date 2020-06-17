# purpose: fix feat directories to be able to run higher level analyses in fsl

set -e

FIRSTLEVEL_DIR=/data/jag/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/fsl/first_level
FMRIPREP_DIR=/data/jag/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/fmriprep
FSF_DIR=$FIRSTLEVEL_DIR/fsf

subjectNumber=$1
SUBJECT=sub-$(printf "%03d" $subjectNumber)
SUBJECT_DIR=$FIRSTLEVEL_DIR/${SUBJECT}

# now fix for each session/run
# 1. remove mat files in /reg
# 2. replace with identity
# 3. cp mean-func as the standard so nothing is changing
sessionNumber=1
SES=ses-$(printf "%02d" $sessionNumber)
runNumber=1
RUN=run-$(printf "%02d" $runNumber)

FEAT_DIR=$SUBJECT_DIR/${SES}/faces${runNumber}_T1w_final.feat 
rm ${FEAT_DIR}/reg/*.mat
cp $FSLDIR/etc/flirtsch/ident.mat ${FEAT_DIR}/reg/example_func2standard.mat 
cp ${FEAT_DIR}/mean_func.nii.gz ${FEAT_DIR}/reg/standard.nii.gz

sessionNumber=1
SES=ses-$(printf "%02d" $sessionNumber)
runNumber=2
RUN=run-$(printf "%02d" $runNumber)

FEAT_DIR=$SUBJECT_DIR/${SES}/faces${runNumber}_T1w_final.feat 
rm ${FEAT_DIR}/reg/*.mat
cp $FSLDIR/etc/flirtsch/ident.mat ${FEAT_DIR}/reg/example_func2standard.mat 
cp ${FEAT_DIR}/mean_func.nii.gz ${FEAT_DIR}/reg/standard.nii.gz

sessionNumber=3
SES=ses-$(printf "%02d" $sessionNumber)
runNumber=1
RUN=run-$(printf "%02d" $runNumber)

FEAT_DIR=$SUBJECT_DIR/${SES}/faces${runNumber}_T1w_final.feat 
rm ${FEAT_DIR}/reg/*.mat
cp $FSLDIR/etc/flirtsch/ident.mat ${FEAT_DIR}/reg/example_func2standard.mat 
cp ${FEAT_DIR}/mean_func.nii.gz ${FEAT_DIR}/reg/standard.nii.gz

sessionNumber=3
SES=ses-$(printf "%02d" $sessionNumber)
runNumber=2
RUN=run-$(printf "%02d" $runNumber)

FEAT_DIR=$SUBJECT_DIR/${SES}/faces${runNumber}_T1w_final.feat 
rm ${FEAT_DIR}/reg/*.mat
cp $FSLDIR/etc/flirtsch/ident.mat ${FEAT_DIR}/reg/example_func2standard.mat 
cp ${FEAT_DIR}/mean_func.nii.gz ${FEAT_DIR}/reg/standard.nii.gz
