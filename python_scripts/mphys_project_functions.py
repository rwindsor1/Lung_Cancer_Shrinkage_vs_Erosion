import numpy as np
import os
import nibabel as nib
import matplotlib.pyplot as plt
import scipy.ndimage
from skimage import feature
import skimage
import math

# generates a mask array from a numpy array. Works as follows:

''' 1) thresholds (thresholding value specified by kwarg threshold, default is 500)
	2) fills holes
	3) removes small objects from tumour of size smaller than small_obj_size
	4) Use canny edge dector to get edges using specified sigma value
	5) Dilate edges to radius given by radius_of_mask
	'''
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
	rand_array = abs(np.random.normal(noise_mean, math.sqrt(noise_var), size=inArr.shape))
	add_mask = (1-inv_removal_pix)*rand_array
	outArr = outArr + add_mask
	return outArr


def fragmenting_sim(inArr, threshold = 500, iterations = 1):
	gtv = np.copy(inArr)
	noise_mean = get_noise_info(gtv)[0]
	noise_var = get_noise_info(gtv)[1]
	noise = abs(np.random.normal(loc=noise_mean, scale=np.sqrt(noise_var), size=gtv.shape))
	gtv[gtv == 0] = noise[gtv== 0]
	for i in range(iterations):
		# generate a mask for the given_gtv
		mask = create_mask(gtv,threshold = threshold, sigma = 0.5, small_obj_size = 20, radius_of_mask=4 )
		# fill in mask 

		filled_mask = scipy.ndimage.morphology.binary_fill_holes(mask)
		# get gradient
		gradient_of_tumour = get_3D_grad_matrix(gtv)
		# matrix containing gradients of the actual tumour
		normalised_gradients = gradient_of_tumour[filled_mask>0]/gradient_of_tumour[filled_mask>0].max()
		random_samples = np.random.triangular(0, 0.6, 1, size=normalised_gradients.shape)
		removed_pixels = np.ones(normalised_gradients.shape)
		removed_pixels[normalised_gradients > random_samples] = 0
		pixel_remover = np.ones(gtv.shape)
		pixel_remover[filled_mask > 0] = removed_pixels
		result = np.multiply(pixel_remover,gtv)
		result[result == 0] = abs(np.random.normal(loc=noise_mean, scale=np.sqrt(noise_var), size=result[result == 0].shape))
		gtv = result
	print(inArr.min())
	result[inArr == 0] = np.zeros(result[inArr == 0].shape)
	return result



def get_3D_grad_matrix(matrix):
	grad_list = np.gradient(matrix)
	grad = np.sqrt(np.multiply(grad_list[0], grad_list[0]) + np.multiply(grad_list[1], grad_list[1]) + np.multiply(grad_list[2], grad_list[2]))
	return grad
	