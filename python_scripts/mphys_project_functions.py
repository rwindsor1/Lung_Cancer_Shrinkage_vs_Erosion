import numpy as np
import os
import nibabel as nib
import matplotlib.pyplot as plt
import scipy.ndimage
from skimage import feature
import skimage

# generates a mask array from a numpy array
def create_mask(gtv_arr, threshold = 500,sigma = 0.5, radius_of_mask = 2,small_obj_size = 20):
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
	return [gtv_arr[(gtv_arr<threshold) & (gtv_arr>0)].mean(),gtv_arr[(gtv_arr<threshold) & (gtv_arr>0)].std()]
	


def show_slice(slice_obj):
    fig,axes = plt.subplots(1)
    axes.imshow(slice_obj, cmap='gray',origin='lower')
    