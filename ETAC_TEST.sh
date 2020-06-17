
# purpose: see if overlapping voxels in pos/negative mask
# in this directory /data/jux/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/resting/clean/group_level/ses-01
3dbucket -prefix stats_dlPFC_MDD_minus_HC.nii.gz stats_dlPFC.ttest.nii.gz[0]

3dcalc -a ses-01_stats_ACC_dlPFC_mask.test1.ETACmask.global.1pos.5perc.nii.gz -b stats_dlPFC_MDD_minus_HC.nii.gz -expr 'a*b' -prefix posmask_times_stats.nii.gz
3dinfo -min posmask_times_stats.nii.gz
3dinfo -max posmask_times_stats.nii.gz
3dcalc -a ses-01_stats_ACC_dlPFC_mask.test1.ETACmask.global.1neg.5perc.nii.gz -b stats_dlPFC_MDD_minus_HC.nii.gz -expr 'a*b' -prefix negmask_times_stats.nii.gz
3dinfo -min negmask_times_stats.nii.gz
3dinfo -max negmask_times_stats.nii.gz

3dinfo -min stats_dlPFC_MDD_minus_HC.nii.gz
3dcalc -a stats_dlPFC_MDD_minus_HC.nii.gz -b ses-01_stats_ACC_dlPFC_mask.test1.ETACmask.global.1neg.5perc.nii.gz  -exp 'a*b' -prefix TEST_SUB.nii.gz
3dcalc -a ses-01_stats_ACC_dlPFC_mask.test1.ETACmask.global.1neg.5perc.nii.gz -b stats_dlPFC_MDD_minus_HC.nii.gz  -exp 'a*b' -prefix TEST_SUB2.nii.gz
3dinfo -min TEST_SUB2.nii.gz


# fslmaths stats_dlPFC_MDD_minus_HC.nii.gz -thr 0 -bin positive_stats_dlPFC_MDD_minus_HC.nii.gz
# fslmaths stats_dlPFC_MDD_minus_HC.nii.gz -uthr 0 -bin negative_stats_dlPFC_MDD_minus_HC.nii.gz

# # now look to see if all voxels for positive ETAC were in the positive mask
# 3dcalc -a ses-01_stats_ACC_dlPFC_mask.test1.ETACmask.global.1pos.5perc.nii.gz -b positive_stats_dlPFC_MDD_minus_HC.nii.gz -expr 'a+b' -prefix posmask_posStat.nii.gz
# 3dinfo -max posmask_posStat.nii.gz # could also threshold
# 3dcalc -a ses-01_stats_ACC_dlPFC_mask.test1.ETACmask.global.1pos.5perc.nii.gz -b negative_stats_dlPFC_MDD_minus_HC.nii.gz -expr 'a+b' -prefix posmask_negStat.nii.gz
# 3dinfo -max posmask_negStat.nii.gz # okay max is 1!

# 3dcalc -a ses-01_stats_ACC_dlPFC_mask.test1.ETACmask.global.1neg.5perc.nii.gz -b positive_stats_dlPFC_MDD_minus_HC.nii.gz -expr 'a+b' -prefix negmask_posStat.nii.gz
# 3dinfo -max negmask_posStat.nii.gz # overlap
# 3dcalc -a ses-01_stats_ACC_dlPFC_mask.test1.ETACmask.global.1neg.5perc.nii.gz -b negative_stats_dlPFC_MDD_minus_HC.nii.gz -expr 'a+b' -prefix negmask_negStat.nii.gz
# 3dinfo -max negmask_negStat.nii.gz # no overlap between negative and negative

# # overlap in 1 pos and 1 neg?
# 3dcalc -a ses-01_stats_ACC_dlPFC_mask.test1.ETACmask.global.1neg.5perc.nii.gz -b ses-01_stats_ACC_dlPFC_mask.test1.ETACmask.global.1pos.5perc.nii.gz -expr 'a+b' -prefix posmask_negmask.nii.gz
# 3dinfo -max posmask_negmask.nii.gz



# now do the same thing with the faces data to test: /data/jux/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/afni/group_level/ses-01

3dbucket -prefix stats_dlPFC_MDD_minus_HC.nii.gz ses-01_stats_fearfulminusneut_ACC_dlPFC_mask.ttest.nii.gz[0]
fslmaths stats_dlPFC_MDD_minus_HC.nii.gz -thr 0 -bin positive_stats_dlPFC_MDD_minus_HC.nii.gz
fslmaths stats_dlPFC_MDD_minus_HC.nii.gz -uthr 0 -bin negative_stats_dlPFC_MDD_minus_HC.nii.gz


3dcalc -a ses-01_stats_fearfulminusneut_ACC_dlPFC_mask_BLUR04.nii.gz[0] -b ses-01_stats_fearfulminusneut_ACC_dlPFC_mask_BLUR04.BLUR04.ETACmask.global.1neg.5perc.nii.gz -expr 'a*b' -prefix negmask_times_stats.nii.gz
3dinfo -min negmask_times_stats.nii.gz
3dinfo -max negmask_times_stats.nii.gz
3dcalc -a ses-01_stats_fearfulminusneut_ACC_dlPFC_mask_BLUR04.B4.0.nii.gz[0] -b ses-01_stats_fearfulminusneut_ACC_dlPFC_mask_BLUR04.BLUR04.ETACmask.global.1pos.5perc.nii.gz -expr 'a*b' -prefix posmask_times_stats.nii.gz



# 3dcalc -a ses-01_stats_fearfulminusneut_ACC_dlPFC_mask.test1.ETACmask.global.1pos.5perc.nii.gz -b positive_stats_dlPFC_MDD_minus_HC.nii.gz -expr 'a+b' -prefix posmask_posStat.nii.gz
# 3dinfo -max posmask_posStat.nii.gz # could also threshold
# 3dcalc -a ses-01_stats_fearfulminusneut_ACC_dlPFC_mask.test1.ETACmask.global.1pos.5perc.nii.gz -b negative_stats_dlPFC_MDD_minus_HC.nii.gz -expr 'a+b' -prefix posmask_negStat.nii.gz
# 3dinfo -max posmask_negStat.nii.gz # okay max is 1!

# 3dcalc -a ses-01_stats_fearfulminusneut_ACC_dlPFC_mask.test1.ETACmask.global.1neg.5perc.nii.gz -b positive_stats_dlPFC_MDD_minus_HC.nii.gz -expr 'a+b' -prefix negmask_posStat.nii.gz
# 3dinfo -max negmask_posStat.nii.gz # overlap
# 3dcalc -a ses-01_stats_fearfulminusneut_ACC_dlPFC_mask.test1.ETACmask.global.1neg.5perc.nii.gz -b negative_stats_dlPFC_MDD_minus_HC.nii.gz -expr 'a+b' -prefix negmask_negStat.nii.gz
# 3dinfo -max negmask_negStat.nii.gz # no overlap between negative and negative

# do the same thing w/ subtracted data: /data/jux/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/afni/group_level/ses-03_minus_ses-01

3dbucket -prefix stats_dlPFC_MDD_minus_HC.nii.gz ses-03_minus_ses-01_stats_fearfulminusneut_ACC_dlPFC_mask.ttest.nii.gz[0]
fslmaths stats_dlPFC_MDD_minus_HC.nii.gz -thr 0 -bin positive_stats_dlPFC_MDD_minus_HC.nii.gz
fslmaths stats_dlPFC_MDD_minus_HC.nii.gz -uthr 0 -bin negative_stats_dlPFC_MDD_minus_HC.nii.gz
3dcalc -a ses-03_minus_ses-01_stats_fearfulminusneut_ACC_dlPFC_mask.test1.ETACmask.global.1pos.5perc.nii.gz -b positive_stats_dlPFC_MDD_minus_HC.nii.gz -expr 'a+b' -prefix posmask_posStat.nii.gz
3dinfo -max posmask_posStat.nii.gz # could also threshold
3dcalc -a ses-03_minus_ses-01_stats_fearfulminusneut_ACC_dlPFC_mask.test1.ETACmask.global.1pos.5perc.nii.gz -b negative_stats_dlPFC_MDD_minus_HC.nii.gz -expr 'a+b' -prefix posmask_negStat.nii.gz
3dinfo -max posmask_negStat.nii.gz # okay max is 1!

3dcalc -a ses-03_minus_ses-01_stats_fearfulminusneut_ACC_dlPFC_mask.test1.ETACmask.global.1neg.5perc.nii.gz -b positive_stats_dlPFC_MDD_minus_HC.nii.gz -expr 'a+b' -prefix negmask_posStat.nii.gz
3dinfo -max negmask_posStat.nii.gz # overlap
3dcalc -a ses-03_minus_ses-01_stats_fearfulminusneut_ACC_dlPFC_mask.test1.ETACmask.global.1neg.5perc.nii.gz -b negative_stats_dlPFC_MDD_minus_HC.nii.gz -expr 'a+b' -prefix negmask_negStat.nii.gz
3dinfo -max negmask_negStat.nii.gz # no overlap between negative and negative


** FATAL ERROR: number of input volumes=2119 not evenly divisible by ncase=4
** Program compile date = Aug  5 2019

# check with given data: /data/jux/cnds/amennen/rtAttenPenn/fmridata/Nifti/derivatives/afni/AFNI_data6/group_results
3dbucket -prefix stats_group_ACM.nii.gz stat.6.covary_ACM+tlrc.BRIK[0]
fslmaths stats_group_ACM.nii.gz -thr 0 -bin positive_stats_ACM.nii.gz
fslmaths stats_group_ACM.nii.gz -uthr 0 -bin negative_stats_ACM.nii.gz
3dcalc -a stat.6.covary_ACM.test1.ETACmask.global.1pos.9perc.nii.gz -b positive_stats_ACM.nii.gz -expr 'a+b' -prefix posmask_posStat.nii.gz
3dinfo -max posmask_posStat.nii.gz # could also threshold
3dcalc -a stat.6.covary_ACM.test1.ETACmask.global.1pos.9perc.nii.gz -b negative_stats_ACM.nii.gz -expr 'a+b' -prefix posmask_negStat.nii.gz
3dinfo -max posmask_negStat.nii.gz # okay max is 1!

3dcalc -a stat.6.covary_ACM.test1.ETACmask.global.1neg.9perc.nii.gz -b positive_stats_ACM.nii.gz -expr 'a+b' -prefix negmask_posStat.nii.gz
3dinfo -max negmask_posStat.nii.gz # overlap

3dcalc -a stat.6.covary_ACM.test1.ETACmask.global.1neg.9perc.nii.gz -b negative_stats_ACM.nii.gz -expr 'a+b' -prefix negmask_negStat.nii.gz
3dinfo -max negmask_negStat.nii.gz # no overlap between negative and negative

3dcalc -a stat.6.covary_ACM.test1.ETACmask.global.1neg.9perc.nii.gz -b stats_group_ACM.nii.gz -expr 'a*b' -prefix negmask_times_stats.nii.gz
3dinfo -min negmask_times_stats.nii.gz
3dinfo -max negmask_times_stats.nii.gz
3dcalc -a stat.6.covary_ACM.test1.ETACmask.global.1pos.9perc.nii.gz -b stats_group_ACM.nii.gz -expr 'a*b' -prefix posmask_times_stats.nii.gz
3dinfo -min posmask_times_stats.nii.gz
3dinfo -max posmask_times_stats.nii.gz

3dcalc -a stat.6.covary_ACM.test1.ETACmask.global.1neg.9perc.nii.gz -b stat.6.covary_ACM+tlrc.BRIK[0] -expr 'a*b' -prefix negmask_times_stats2.nii.gz
3dinfo -min negmask_times_stats2.nii.gz
3dinfo -max negmask_times_stats2.nii.gz

3dcalc -a stats_group_ACM.nii.gz -b stat.6.covary_ACM.test1.ETACmask.global.1neg.9perc.nii.gz -expr 'a*b' -prefix negmask_times_stats2.nii.gz
3dinfo -max negmask_times_stats2.nii.gz
3dinfo -min negmask_times_stats2.nii.gz

3dcalc -a stats_group_ACM.nii.gz -b stat.6.covary_ACM.test1.ETACmask.global.1pos.9perc.nii.gz -expr 'a*b' -prefix posmask_times_stats2.nii.gz
3dinfo -max posmask_times_stats2.nii.gz
3dinfo -min posmask_times_stats2.nii.gz