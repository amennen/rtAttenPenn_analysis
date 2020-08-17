#!/bin/bash

# purpose: make sphere based on ROI coordinates
# supply coordinates from thresholded--let's go with threshold of 5

ROIDIR=/data/jux/cnds/amennen/rtAttenPenn/MNI_things/clusters
STANDARD=/data/jux/cnds/amennen/rtAttenPenn/MNI_things/mni_icbm152_t1_tal_nlin_asym_09c_BOLD_brain_Penn.nii.gz

c=1
ROI_IND=(25 49 39) # 

c=2
ROI_IND=(38 50 35) # 

c=3
ROI_IND=(30 63 25) # 

c=4
ROI_IND=(33 64 23) # 

c=5
ROI_IND=(16 39 22) # 

c=6
ROI_IND=(16 39 22) # 

c=7
ROI_IND=(14 46 14) # 

c=8
ROI_IND=(13 44 16) # 

c=9
ROI_IND=(45 19 29) # 

c=10
ROI_IND=(24 42 19) # 

c=11
ROI_IND=(38 35 21)

c=12
ROI_IND=(24 34 20)

c=13
ROI_IND=(28 47 44)


fslmaths $STANDARD -mul 0 -add 1 -roi ${ROI_IND[0]} 1 ${ROI_IND[1]} 1 ${ROI_IND[2]} 1 0 1 ${ROIDIR}/cluster${c}.nii.gz -odt float
fslmaths ${ROIDIR}/cluster${c}.nii.gz -kernel sphere 6 -fmean -bin ${ROIDIR}/cluster${c}sphere.nii.gz


# # now add all of the clusters into one ROI
# fslmaths ${ROIDIR}/cluster1sphere_bin.nii.gz -add ${ROIDIR}/cluster2sphere_bin.nii.gz -add ${ROIDIR}/cluster3sphere_bin.nii.gz \
# 	-add ${ROIDIR}/cluster4sphere_bin.nii.gz -add ${ROIDIR}/cluster5sphere_bin.nii.gz -add ${ROIDIR}/cluster6sphere_bin.nii.gz \
# 	-add ${ROIDIR}/cluster7sphere_bin.nii.gz  -add ${ROIDIR}/cluster8sphere_bin.nii.gz  -add ${ROIDIR}/cluster9sphere_bin.nii.gz \
# 	-add ${ROIDIR}/cluster10sphere_bin.nii.gz \
# 	-bin ${ROIDIR}/top10clusters.nii.gz


# # now mask by the brain
