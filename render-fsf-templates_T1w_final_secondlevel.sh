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
FSF_DIR=$SECONDLEVEL_DIR/fsf # new template in level 2 directory

subjectNumber=$1
SUBJECT=sub-$(printf "%03d" $subjectNumber)
SUBJECT_DIR_FIRSTLEVEL=$FIRSTLEVEL_DIR/${SUBJECT}
SUBJECT_DIR_SECONDLEVEL=$SECONDLEVEL_DIR/${SUBJECT}
mkdir -pv $SUBJECT_DIR_SECONDLEVEL/ses-01
mkdir -pv $SUBJECT_DIR_SECONDLEVEL/ses-02
mkdir -pv $SUBJECT_DIR_SECONDLEVEL/ses-03


echo "creating directory for $SUBJECT"
function render_secondlevel_faces {
  fsf_template=$1
  output_dir=$2
  feat_directory_1=$3
  feat_directory_2=$4
  
  
  # note: the following replacements put absolute paths into the fsf file. this
  #       is necessary because FEAT changes directories internally
  cat $fsf_template \
    | sed "s:<?= \$OUTPUT_DIR ?>:$output_dir:g" \
    | sed "s:<?= \$FEAT_DIRECTORY_1 ?>:$feat_directory_1:g" \
    | sed "s:<?= \$FEAT_DIRECTORY_2 ?>:$feat_directory_2:g" \
	
}

sessionNumber=1
SES=ses-$(printf "%02d" $sessionNumber)
# now do for runs 1 and 2
render_secondlevel_faces $FSF_DIR/faces_MNI.fsf.template \
                  $SUBJECT_DIR_SECONDLEVEL/${SES}/faces_T1w_final.gfeat \
                  $SUBJECT_DIR_FIRSTLEVEL/${SES}/faces1_T1w_final.feat \
                  $SUBJECT_DIR_FIRSTLEVEL/${SES}/faces2_T1w_final.feat > $SUBJECT_DIR_SECONDLEVEL/${SES}/faces_T1w_final.fsf

sessionNumber=3
SES=ses-$(printf "%02d" $sessionNumber)

# now do for runs 1 and 2
render_secondlevel_faces $FSF_DIR/faces_MNI.fsf.template \
                  $SUBJECT_DIR_SECONDLEVEL/${SES}/faces_T1w_final.gfeat \
                  $SUBJECT_DIR_FIRSTLEVEL/${SES}/faces1_T1w_final.feat \
                  $SUBJECT_DIR_FIRSTLEVEL/${SES}/faces2_T1w_final.feat > $SUBJECT_DIR_SECONDLEVEL/${SES}/faces_T1w_final.fsf


# variables to change:
# OUTPUTDIR
# feat directory 1
# feat directory 2
