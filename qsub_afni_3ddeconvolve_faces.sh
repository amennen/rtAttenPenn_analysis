#!/bin/bash

# Run within BIDS code/ directory:
# sbatch slurm_mriqc.sh

# Set current working directory
#$ -wd '/data/jux/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/logs/'
# #$ -cwd
#$ -t 1-25
#$ -j y
#$ -m ea
#$ -M anne.mennen@pennmedicine.upenn.edu
#$ -N AFNI_3ddeconvolve
#$ -w e
#$ -l h_rt=1:00:00
#$ -l h_vmem=5.5G
#$ -l s_vmem=5G
##### #$ -l h_data=30G


echo SGE_TASK_ID: $SGE_TASK_ID
date 

# Set subject ID based on array index
subject_vector=( 1 2 3 4 5 6 7 8 9 10 11 101 102 103 104 105 106 107 108 109 110 111 112 113 114)
subject=${subject_vector[$SGE_TASK_ID - 1]}
printf -v subj "%03d" $subject

conda activate rtAtten
cd /data/jux/cnds/amennen/rtAttenPenn/fmridata/Nifti/code/

echo "starting script"
#python AFNI_3ddeconvolve_faces_trials_TENT.py $subject
python AFNI_3dTproject_faces.py $subject
# Run fMRIPrep script with participant argument
echo "Finished 3ddeconvolve on sub-$subj"
date
