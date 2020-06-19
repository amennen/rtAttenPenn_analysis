#!/bin/bash


# Purpose: combine amygdala mask and Power atlas to be loaded together into functions

# make sure you have already followed the steps to update this mask with each new subject
#amygdala_mask = '/data/jux/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/mni_anat/LAMYG_in_MNI_overlapping.nii.gz'

# first multiply the amygdala mask by 265 for it's label number
fslmaths /data/jux/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/mni_anat/LAMYG_in_MNI_overlapping.nii.gz -mul 265 /data/jux/cnds/amennen/Power/amygdala_mul265.nii.gz

# then add it to the Power atlas
fslmaths /data/jux/cnds/amennen/Power/amygdala_mul265.nii.gz -add /data/jux/cnds/amennen/Power/power264MNI_resampled.nii.gz /data/jux/cnds/amennen/Power/power264MNI_resampled_amygdala.nii.gz 
