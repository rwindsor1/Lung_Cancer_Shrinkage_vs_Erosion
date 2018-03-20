import numpy as np
import os
import nibabel as nib
import matplotlib.pyplot as plt
import scipy.ndimage
from skimage import feature
import skimage
import math

# generates a mask array from a numpy array
def create_mask(gtv_arr, threshold = 500,sigma = 0.05, radius_of_mask = 2,small_obj_size = 20):
	mask_arr = np.copy(gtv_arr)
	mask_arr[np.where(mask_arr<threshold)] = 0
	for i in range(np.shape(mask_arr)[2]):
		scan_slice = scipy.ndimage.binary_fill_holes(mask_arr[:,:,i])
		scan_slice = skimage.morphology.remove_small_objects(scan_slice.astype(bool), min_size=small_obj_size, connectivity=1, in_place=False)
		edges = feature.canny(scan_slice,sigma=sigma)
		mask = skimage.filters.rank.maximum(edges,skimage.morphology.disk(radius_of_mask))
		mask_arr[:,:,i] = mask
		
	return mask_arr

# gets the values of healthy tissue mean and standard devation around the tumour
def get_healthy_tissue_vals(gtv_arr,threshold = 500):
	return gtv_arr[np.where(mask_arr<threshold and mask_arr>0)].mean(),gtv_arr[np.where(mask_arr<threshold and mask_arr>0)].var()
	


def show_slice(slice_obj):
    fig,axes = plt.subplots(1)
    axes.imshow(slice_obj, cmap='gray',origin='lower')
	
def get_noise_info(inArr,threshold =500):
    img = np.copy(inArr)
    binary = np.copy(img)
    binary[np.where(binary < threshold)] = 0
    binary[np.where(binary >= threshold)] = 1
    noise = img*(1-binary).astype(float)
    noise[np.where(noise == 0)] = np.nan
    noise_mean = np.nanmean(noise)
    noise_var = np.nanvar(noise)
    return [noise_mean, noise_var]
	
def elastic_sim(inArr, threshold=500, depth = 1):
	gtv_arr = np.copy(inArr)
	old_mask = create_mask(inArr, radius_of_mask = depth)
	gtv_arr[gtv_arr < threshold] = 0
	gtv_arr[gtv_arr >= threshold] = 1
	removal_pix = old_mask*gtv_arr
	noise_mean = get_noise_info(inArr)[0]
	noise_var = get_noise_info(inArr)[1]
	inv_removal_pix=1-removal_pix/255
	outArr = inv_removal_pix*inArr
	rand_array = np.random.normal(noise_mean, sqrt(noise_var), size=inArr.shape)
	add_mask = (1-inv_removal_pix)*rand_array
	outArr = outArr + add_mask
	return outArr
    