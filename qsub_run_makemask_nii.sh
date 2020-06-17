#!/bin/bash

# Run within BIDS code/ directory:
# sbatch slurm_mriqc.sh

# Set current working directory
#$ -wd '/data/jux/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/logs/'
# #$ -cwd
#$ -t 12,27
#$ -j y
#$ -m ea
#$ -M anne.mennen@pennmedicine.upenn.edu
#$ -N register_perception_attention
#$ -w e
#$ -l h_rt=0:10:00
#$ -l h_vmem=5.5G
#$ -l s_vmem=5G

conda activate rtAtten
ROI_DIR=/data/jux/cnds/amennen/rtAttenPenn/MNI_things/faces_places_attn
perception_ROI=$ROI_DIR/faces_places_masked.nii.gz 
attention_ROI=$ROI_DIR/attention_masked.nii.gz
data_path=/data/jux/cnds/amennen/rtAttenPenn/fmridata/behavdata/gonogo
functionalFN=exfunc
functional2FN=exfunc2
highres2exfunc_mat=highres2example_func
code_path=/data/jux/cnds/amennen/rtAttenPenn/fmridata/Nifti/code

# first you have to apply the saved transformations
subject_vector=( 1 2 3 4 5 6 7 8 9 10 11 12 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115)
subjectNum=${subject_vector[$SGE_TASK_ID - 1]}
# for day 1
dayNum=1
subject_reg_path=$data_path/subject$subjectNum/day$dayNum/reg
cd $subject_reg_path
echo "moving into folder: $subject_reg_path"
applywarp -v -i $perception_ROI -r $functionalFN'.'nii.gz -o perception'_'exfunc.nii.gz -w standard2highres_warp.nii.gz --postmat=$highres2exfunc_mat'.'mat
applywarp -v -i $attention_ROI -r $functionalFN'.'nii.gz -o attention'_'exfunc.nii.gz -w standard2highres_warp.nii.gz --postmat=$highres2exfunc_mat'.'mat
cd $code_path
python makemask_day.py $subjectNum $dayNum $data_path 

# for day 2/3
dayNum=2
subject_day1_path=$data_path/subject$subjectNum/day1/reg
subject_reg_path=$data_path/subject$subjectNum/day$dayNum/reg
cd $subject_reg_path
echo "moving into folder: $subject_reg_path"
flirt -v -in $subject_day1_path/perception_exfunc -ref $functional2FN'.'nii.gz -applyxfm -init func12func2.mat -interp nearestneighbour -out perception2func2
flirt -v -in $subject_day1_path/attention_exfunc -ref $functional2FN'.'nii.gz -applyxfm -init func12func2.mat -interp nearestneighbour -out attention2func2
cd $code_path
python makemask_day.py $subjectNum $dayNum $data_path 

dayNum=3
subject_reg_path=$data_path/subject$subjectNum/day$dayNum/reg
cd $subject_reg_path
echo "moving into folder: $subject_reg_path"
flirt -v -in $subject_day1_path/perception_exfunc -ref $functional2FN'.'nii.gz -applyxfm -init func12func2.mat -interp nearestneighbour -out perception2func2
flirt -v -in $subject_day1_path/attention_exfunc -ref $functional2FN'.'nii.gz -applyxfm -init func12func2.mat -interp nearestneighbour -out attention2func2
cd $code_path
python makemask_day.py $subjectNum $dayNum $data_path 



echo "done!"
