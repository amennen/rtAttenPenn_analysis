#!/bin/bash

# Run within BIDS code/ directory:
# sbatch slurm_mriqc.sh

# Set current working directory
#$ -wd '/data/jag/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/logs/'
# #$ -cwd
#$ -t 6
#$ -j y
#$ -m ea
#$ -M anne.mennen@pennmedicine.upenn.edu
#$ -N retrainAndTest
#$ -w e
#$ -l h_rt=2:00:00
#$ -l h_vmem=5.5G
#$ -l s_vmem=5G
##### #$ -l h_data=30G


echo SGE_TASK_ID: $SGE_TASK_ID
date 

# Set subject ID based on array index
subject_vector=( 1 2 3 4 5 6 101 102 103 104 105 106 107 108)
subject=${subject_vector[$SGE_TASK_ID - 1]}
printf -v subj "%03d" $subject

cd /data/jag/cnds/amennen/brainiak/rtAttenPenn_cloud
conda activate rtAtten
echo "starting script"
python anne_additions/train_test_python_classifier.py $subject
# Run fMRIPrep script with participant argument
echo "Finished running train-test script on sub-$subj"
date
