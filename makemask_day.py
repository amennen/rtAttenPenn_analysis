# Function to load in niftis and make a mask for those files

import numpy as np
import sys
import os
import os
import scipy
from scipy import io
import glob
import nibabel
import matplotlib.pyplot as plt
import argparse
import logging
import glob
# needs to:
# load the 2 nifti files
# rotate back to be in functional space - 90 degree counterclockwise rotation of the third dimension

subjectNum = np.int(sys.argv[1])
dayNum = np.int(sys.argv[2])
data_path = sys.argv[3]

def plot3Dbrain(nslices,mask):
    plt.subplots()
    for s in np.arange(nslices):
        plt.subplot(6,6,s+1)
        plt.imshow(mask[:,:,s])
    plt.show()
    return

def applyMask(volume, roiInds):
    # maskedVolume = np.zeros(volume.shape, dtype=float)
    # maskedVolume.flat[roiInds] = volume.flat[roiInds]
    maskedVolume = volume.flat[roiInds]
    return maskedVolume
#cfg.session.roiInds = utils.find(roi)
#TR.data = applyMask(trVolumeData, self.cfg.session.roiInds)
def find(A: np.ndarray) -> np.ndarray:
    '''Find nonzero elements of A in flat "C" row-major indexing order
       but sorted as in "F" column indexing order'''
    # find indices of non-zero elements in roi
    inds = np.nonzero(A)
    dims = A.shape
    # First convert to Matlab column-order raveled indicies in order to sort
    #   the indicies to match the order the data appears in the p.raw matrix
    indsMatRavel = np.ravel_multi_index(inds, dims, order='F')
    indsMatRavel.sort()
    # convert back to python raveled indices
    indsMat = np.unravel_index(indsMatRavel, dims, order='F')
    resInds = np.ravel_multi_index(indsMat, dims, order='C')
    return resInds

def makeMask(subjectNum,dayNum,data_path,ROI):



    if dayNum==1:
        functionalFN = 'exfunc'

        maskName = ROI + '_' + 'exfunc'
    else:
        functionalFN = 'exfunc2'
        maskName = ROI  + '2func2'

    subject_day_dir = "{0}/subject{1}/day{2}".format(data_path,subjectNum,dayNum)
    nifti_exfunc = glob.glob("{0}/reg/{1}_brain.nii*".format(subject_day_dir,functionalFN))[0]
    nifti_mask = "{0}/reg/{1}.nii.gz".format(subject_day_dir,maskName)
    matrix_mask_output = "{0}/{3}_{1}_{2}.mat".format(subject_day_dir,subjectNum,dayNum,ROI)
    original_mask_matrix = "{0}/mask_{1}_{2}.mat".format(subject_day_dir,subjectNum,dayNum)
    original_mask = scipy.io.loadmat(original_mask_matrix)['mask']
    # start with example case then check later
    # nifti_exfunc='/Volumes/norman/amennen/TEMP_MAKE_MASK/exfunc_brain.nii.gz'
    # nifti_mask='/Volumes/norman/amennen/TEMP_MAKE_MASK/wholebrain_mask_exfunc.nii.gz'

    exfunc_img = nibabel.load(nifti_exfunc).get_data()
    mask_img = nibabel.load(nifti_mask).get_data()
    
    # now rotate each
    anatMaskRot = np.zeros(np.shape(exfunc_img))
    brainExtRot = np.zeros((np.shape(exfunc_img)))
    for i in np.arange(np.shape(exfunc_img)[2]):
        anatMaskRot[:,:,i] = np.rot90(mask_img[:,:,i])
        brainExtRot[:,:,i] = np.rot90(exfunc_img[:,:,i])
    
    anatMaskRot = anatMaskRot.astype(bool)
    brainExtRot = brainExtRot.astype(bool)
    intersection = np.logical_and(anatMaskRot,brainExtRot)
    intersection2 = np.logical_and(intersection,original_mask)
    indices_original = np.argwhere(original_mask)
    indices_1d_original = find(original_mask)

    indices_1d_ROI = find(intersection2)
    n_new_ROI = len(indices_1d_ROI)

    ROI_ind_in_wholebrain = np.zeros((n_new_ROI,))
    for i in np.arange(n_new_ROI):
        this_index = np.argwhere(indices_1d_original == indices_1d_ROI[i])[0][0]
        ROI_ind_in_wholebrain[i] = this_index
    ROI_ind_in_wholebrain = ROI_ind_in_wholebrain.astype(int)

    # now let's check this - make random 64 x 64 x 36 x 3 time series
    # then load in masked with original index --> then remask with indices in whole brain
    # load in masked with ROI
    # check that they're the same
    # sample_data = np.random.rand(64,64,36)
    # orig = applyMask(sample_data,indices_1d_original)
    # roi = applyMask(sample_data,indices_1d_ROI)
    # roi_2 = orig[ROI_ind_in_wholebrain]
    # sum(roi!=roi_2)
    #np.unravel_index(indices_1d_original[ROI_ind_in_wholebrain],(64,64,36))
    mask_brain = np.zeros((np.shape(exfunc_img)))
    mask_brain[intersection2] = 1
    #mask_brain = mask_brain.astype(int)
    mask = {}
    mask['mask'] = mask_brain
    mask['indices'] = ROI_ind_in_wholebrain
    checkMask = 0
    if checkMask:
        plot3Dbrain(36,mask_brain)

    scipy.io.savemat(matrix_mask_output,mask)

    return 


def main():

    # MAKE FUNCTION HERE TO TAKE IN THE ARGUMENT OF SAVE PATH!
    makeMask(subjectNum,dayNum,data_path,'perception')
    makeMask(subjectNum,dayNum,data_path,'attention')

if __name__ == "__main__":
    # execute only if run as a script
    main()
