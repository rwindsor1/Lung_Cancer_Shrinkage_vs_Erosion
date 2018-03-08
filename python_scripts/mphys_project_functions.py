import numpy as np
import os
import nibabel as nib
import matplotlib.pyplot as plt
import scipy.ndimage
from skimage import feature
import skimage
from PIL import Image
from skimage.viewer import ImageViewer	

# generates a mask array from a numpy array
def create_mask(gtv_arr, threshold = 500, radius_of_mask = 2):
	mask_arr = gtv_arr
	mask_arr[np.where(mask_arr<threshold)] = 0
	output_arr = np.zeros(mask_arr)
	for i in range(np.shape(mask_arr)[2]):
		scan_slice = scipy.ndimage.binary_fill_holes(mask_arr[:,:,i])
		scan_slice = skimage.morphology.remove_small_objects(scan_slice.astype(bool), min_size=20, connectivity=1, in_place=False)
		edges = feature.canny(scan_slice,sigma=2)
		mask = skimage.filters.rank.maximum(edges,skimage.morphology.disk(radius_of_mask))
		output_arr[:,:,i] = mask
		
	return mask_arr
	
def show_slice(slice_obj):
    fig,axes = plt.subplots(1)
    axes.imshow(slice_obj, cmap='gray',origin='lower')
    