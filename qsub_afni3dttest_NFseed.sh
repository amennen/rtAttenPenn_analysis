#!/bin/bash

# Set current working directory
#$ -wd '/data/jux/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/logs/'
# #$ -cwd
#$ -j y
#$ -m ea
#$ -M anne.mennen@pennmedicine.upenn.edu
#$ -N afni_3ddtest_NFseed
#$ -w e
#$ -l h_rt=8:00:00
#$ -l h_vmem=8.5G
#$ -l s_vmem=8G
##### #$ -l h_data=30G


echo SGE_TASK_ID: $SGE_TASK_ID
date 

# Set subject ID based on array index

conda activate rtAtten
echo "starting script"
cd /data/jux/cnds/amennen/rtAttenPenn/fmridata/Nifti/code/
#python AFNI_3dttest_NFseed_neg.py
python AFNI_3dttest_NFseed_neg_diff.py

# Run fMRIPrep script with participant argument
echo "Finished AFNI_3dttest_NFseed"
date
