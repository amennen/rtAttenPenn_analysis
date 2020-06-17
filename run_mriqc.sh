#! /bin/bash

# Run using something like:
# ./run_mriqc.sh |& tee ../derivatives/logs/run_mriqc.txt 


bids_dir=/data/jag/cnds/amennen/rtAttenPenn/fmridata/Nifti

singularity run --cleanenv \
    --home $bids_dir:/home \
    /data/jag/cnds/amennen/singularity/mriqc/mriqc-v0.10.4.sqsh \
    --participant-label sub-$1 --correct-slice-timing \
    --nprocs 4 -w /home/derivatives/work \
    /home /home/derivatives/mriqc participant
