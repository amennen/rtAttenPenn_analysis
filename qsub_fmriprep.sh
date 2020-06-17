#!/bin/bash

# Run within BIDS code/ directory:
# sbatch slurm_mriqc.sh

# Set current working directory
#$ -wd '/data/jux/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/logs/'
# #$ -cwd
#$ -t 12
#$ -j y
#$ -m ea
#$ -M anne.mennen@pennmedicine.upenn.edu
#$ -N fmriprep
#$ -w e
#$ -binding linear:4
#$ -pe unihost 4
#$ -l h_rt=72:00:00
#$ -l h_vmem=5.5G
#$ -l s_vmem=5G
##### #$ -l h_data=30G


echo SGE_TASK_ID: $SGE_TASK_ID
date 

# Set subject ID based on array index
subject_vector=( 1 2 3 4 5 6 7 8 9 10 11 12 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 )
subject=${subject_vector[$SGE_TASK_ID - 1]}
printf -v subj "%03d" $subject

# Run fMRIPrep script with participant argument
echo "Running FMRIPREP on sub-$subj"

bash /data/jux/cnds/amennen/rtAttenPenn/fmridata/Nifti/code/run_fmriprep.sh $subj

echo "Finished running FMRIPREP on sub-$subj"
date
