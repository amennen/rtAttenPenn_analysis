#!/bin/bash

# Set current working directory
#$ -wd '/data/jux/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/logs/'
# #$ -cwd
#$ -j y
#$ -m ea
#$ -M anne.mennen@pennmedicine.upenn.edu
#$ -N afni_3ddtest_faces
#$ -w e
#$ -l h_rt=2:00:00
#$ -l h_vmem=5.5G
#$ -l s_vmem=5G
##### #$ -l h_data=30G


echo SGE_TASK_ID: $SGE_TASK_ID
date 

# Set subject ID based on array index

conda activate rtAtten
echo "starting script"
cd /data/jux/cnds/amennen/rtAttenPenn/fmridata/Nifti/code/
#python AFNI_3dttest_faces_PFCmask_subtracted.py
#python clustSim_faces.py
python AFNI_3dttest_faces_PFCmask.py

# Run fMRIPrep script with participant argument
echo "Finished AFNI_3dttest_faces_PFC_mask"
date
