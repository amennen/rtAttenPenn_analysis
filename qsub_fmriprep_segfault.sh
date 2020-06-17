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
#$ -N fmriprep
#$ -w e
#$ -binding linear:4
#$ -pe unihost 8
#$ -l h_rt=30:00:00
#$ -l h_vmem=5.5G
#$ -l s_vmem=5G
##### #$ -l h_data=30G


echo SGE_TASK_ID: $SGE_TASK_ID
date 

# Set subject ID based on array index
subject_vector=( 1 2 101 102 103 104)
subject=${subject_vector[$SGE_TASK_ID - 1]}
printf -v subj "%03d" $subject

# Run fMRIPrep script with participant argument
echo "Running FMRIPREP on sub-$subj"

bash /data/jag/cnds/amennen/rtAttenPenn/fmridata/Nifti/code/run_fmriprep.sh $subj

echo "Finished running FMRIPREP on sub-$subj"
date
