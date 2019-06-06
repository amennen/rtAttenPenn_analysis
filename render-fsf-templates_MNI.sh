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
BOLD_DATA=/data/jag/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/fmriprep/${SUBJECT}/ses-01/func/${SUBJECT}_ses-01_task-faces_rec-uncorrected_run-01_bold_space-T1w_preproc.nii.gz
mkdir -pv $SUBJECT_DIR/ses-01
mkdir -pv $SUBJECT_DIR/ses-02
mkdir -pv $SUBJECT_DIR/ses-03


echo "creating directory for $SUBJECT"
function render_firstlevel_faces {
  fsf_template=$1
  output_dir=$2
  data_file_prefix=$3
  confound_file=$4
  fearful_timing=$5
  happy_timing=$6
  neutral_timing=$7
  object_timing=$8
  
  
  # note: the following replacements put absolute paths into the fsf file. this
  #       is necessary because FEAT changes directories internally
  cat $fsf_template \
    | sed "s:<?= \$OUTPUT_DIR ?>:$output_dir:g" \
    | sed "s:<?= \$DATA_FILE_PREFIX ?>:$data_file_prefix:g" \
    | sed "s:<?= \$CONFOUND_FILE ?>:$confound_file:g" \
    | sed "s:<?= \$FEARFUL_FILE ?>:$fearful_timing:g" \
    | sed "s:<?= \$HAPPY_FILE ?>:$happy_timing:g" \
    | sed "s:<?= \$NEUTRAL_FILE ?>:$neutral_timing:g" \
	| sed "s:<?= \$OBJECT_FILE ?>:$object_timing:g" \
	
}

# output_dir: where you want the output feat processing to go
# num_vols: number of TR's
# data_file_prefix: the nifti file directory
# reference file directory
# outputfield map image

# 1. day 1, faces 1
sessionNumber=1
SES=ses-$(printf "%02d" $sessionNumber)
runNumber=1
RUN=run-$(printf "%02d" $runNumber)
if [ $runNumber -eq 1 ]; then char=A ; else char=B; fi

render_firstlevel_faces $FSF_DIR/faces_MNI.fsf.template \
                  $SUBJECT_DIR/${SES}/faces${runNumber}_MNI.feat \
                  $FMRIPREP_DIR/${SUBJECT}/${SES}/func/${SUBJECT}_${SES}_task-faces_rec-uncorrected_${RUN}_bold_space-MNI152NLin2009cAsym_preproc.nii.gz \
                  $FIRSTLEVEL_DIR/confound_EVs/${SUBJECT}/${SES}/${SUBJECT}_${SES}_task-faces_rec-uncorrected_${RUN}_bold_confounds.tsv \
                  $FIRSTLEVEL_DIR/timing_files/${SUBJECT}/${SES}/${char}_fearful.txt \
                  $FIRSTLEVEL_DIR/timing_files/${SUBJECT}/${SES}/${char}_happy.txt \
                  $FIRSTLEVEL_DIR/timing_files/${SUBJECT}/${SES}/${char}_neutral.txt \
                  $FIRSTLEVEL_DIR/timing_files/${SUBJECT}/${SES}/${char}_object.txt > $FIRSTLEVEL_DIR/${SUBJECT}/${SES}/faces${runNumber}_MNI.fsf
                   
# 2. day 1, faces 2
sessionNumber=1
SES=ses-$(printf "%02d" $sessionNumber)
runNumber=2
RUN=run-$(printf "%02d" $runNumber)
if [ $runNumber -eq 1 ]; then char=A ; else char=B; fi

render_firstlevel_faces $FSF_DIR/faces_MNI.fsf.template \
                  $SUBJECT_DIR/${SES}/faces${runNumber}_MNI.feat \
                  $FMRIPREP_DIR/${SUBJECT}/${SES}/func/${SUBJECT}_${SES}_task-faces_rec-uncorrected_${RUN}_bold_space-MNI152NLin2009cAsym_preproc.nii.gz \
                  $FIRSTLEVEL_DIR/confound_EVs/${SUBJECT}/${SES}/${SUBJECT}_${SES}_task-faces_rec-uncorrected_${RUN}_bold_confounds.tsv \
                  $FIRSTLEVEL_DIR/timing_files/${SUBJECT}/${SES}/${char}_fearful.txt \
                  $FIRSTLEVEL_DIR/timing_files/${SUBJECT}/${SES}/${char}_happy.txt \
                  $FIRSTLEVEL_DIR/timing_files/${SUBJECT}/${SES}/${char}_neutral.txt \
                  $FIRSTLEVEL_DIR/timing_files/${SUBJECT}/${SES}/${char}_object.txt > $FIRSTLEVEL_DIR/${SUBJECT}/${SES}/faces${runNumber}_MNI.fsf

# 3. day 2, faces 1
sessionNumber=3
SES=ses-$(printf "%02d" $sessionNumber)
runNumber=1
RUN=run-$(printf "%02d" $runNumber)
if [ $runNumber -eq 1 ]; then char=A ; else char=B; fi
render_firstlevel_faces $FSF_DIR/faces_MNI.fsf.template \
                  $SUBJECT_DIR/${SES}/faces${runNumber}_MNI.feat \
                  $FMRIPREP_DIR/${SUBJECT}/${SES}/func/${SUBJECT}_${SES}_task-faces_rec-uncorrected_${RUN}_bold_space-MNI152NLin2009cAsym_preproc.nii.gz \
                  $FIRSTLEVEL_DIR/confound_EVs/${SUBJECT}/${SES}/${SUBJECT}_${SES}_task-faces_rec-uncorrected_${RUN}_bold_confounds.tsv \
                  $FIRSTLEVEL_DIR/timing_files/${SUBJECT}/${SES}/${char}_fearful.txt \
                  $FIRSTLEVEL_DIR/timing_files/${SUBJECT}/${SES}/${char}_happy.txt \
                  $FIRSTLEVEL_DIR/timing_files/${SUBJECT}/${SES}/${char}_neutral.txt \
                  $FIRSTLEVEL_DIR/timing_files/${SUBJECT}/${SES}/${char}_object.txt > $FIRSTLEVEL_DIR/${SUBJECT}/${SES}/faces${runNumber}_MNI.fsf
# 3. day 2, faces 1
sessionNumber=3
SES=ses-$(printf "%02d" $sessionNumber)
runNumber=2
RUN=run-$(printf "%02d" $runNumber)
if [ $runNumber -eq 1 ]; then char=A ; else char=B; fi
render_firstlevel_faces $FSF_DIR/faces_MNI.fsf.template \
                  $SUBJECT_DIR/${SES}/faces${runNumber}_MNI.feat \
                  $FMRIPREP_DIR/${SUBJECT}/${SES}/func/${SUBJECT}_${SES}_task-faces_rec-uncorrected_${RUN}_bold_space-MNI152NLin2009cAsym_preproc.nii.gz \
                  $FIRSTLEVEL_DIR/confound_EVs/${SUBJECT}/${SES}/${SUBJECT}_${SES}_task-faces_rec-uncorrected_${RUN}_bold_confounds.tsv \
                  $FIRSTLEVEL_DIR/timing_files/${SUBJECT}/${SES}/${char}_fearful.txt \
                  $FIRSTLEVEL_DIR/timing_files/${SUBJECT}/${SES}/${char}_happy.txt \
                  $FIRSTLEVEL_DIR/timing_files/${SUBJECT}/${SES}/${char}_neutral.txt \
                  $FIRSTLEVEL_DIR/timing_files/${SUBJECT}/${SES}/${char}_object.txt > $FIRSTLEVEL_DIR/${SUBJECT}/${SES}/faces${runNumber}_MNI.fsf


