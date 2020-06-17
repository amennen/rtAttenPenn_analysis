#! /bin/bash

# Run using something like:
# ./run_mriqc.sh |& tee ../derivatives/logs/run_mriqc.txt 

bids_dir=/jukebox/hasson/snastase/stories/21styear

singularity run --cleanenv \
    --bind $bids_dir:/home \
    /jukebox/hasson/singularity/mriqc/mriqc-v0.10.4.sqsh \
    --correct-slice-timing --modalities T1w bold \
    --nprocs 8 -w /home/derivatives/work \
    /home /home/derivatives/mriqc group
