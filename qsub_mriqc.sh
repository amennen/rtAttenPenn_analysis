#!/bin/bash

# Run within BIDS code/ directory:
# sbatch slurm_mriqc.sh

# Set current working directory
#$ -wd '/data/jag/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/logs/'
# #$ -t 2-3
#$ -j y
#$ -m ea
#$ -M anne.mennen@pennmedicine.uphs.upenn.edu
#$ -N mriqc
#$ -w e
# #$ -binding linear:4
#$ -pe unihost 4
#$ -l h_rt=24:00:00
#$ -l h_vmem=5.5G
#$ -l s_vmem=5G

date 
#echo SGE_TASK_ID: $SGE_TASK_ID
# Set subject ID based on array index
subject_vector=( 1 2 101 102 103 104)
#subject=${subject_vector[$SGE_TASK_ID - 1]}
subject=2
printf -v subj "%03d" $subject

# Run fMRIPrep script with participant argument
echo "Running MRIQC on sub-$subj"

bash /data/jag/cnds/amennen/rtAttenPenn/fmridata/Nifti/code/run_mriqc.sh $subj

echo "Finished running MRIQC on sub-$subj"
date
