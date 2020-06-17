#! /bin/bash

# Run using something like:
# ./run_fmriprep.sh |& tee ../derivatives/logs/run_fmriprep.txt 

bids_dir=/data/jag/cnds/amennen/rtAttenPenn/fmridata/Nifti

singularity run --cleanenv \
    --home $bids_dir:/home \
    /data/jag/cnds/amennen/singularity/fmriprep/fmriprep-v1.0.11.sqsh \
    --participant-label sub-$1 \
    --mem_mb 5000 \
    --fs-license-file /home/code/license.txt --no-submm-recon \
    --bold2t1w-dof 9 --nthreads 32 --omp-nthreads 4 \
    --output-space T1w template fsaverage6 \
    --template MNI152NLin2009cAsym \
    --use-syn-sdc --write-graph --work-dir /home/derivatives/work \
    /home /home/derivatives participant
