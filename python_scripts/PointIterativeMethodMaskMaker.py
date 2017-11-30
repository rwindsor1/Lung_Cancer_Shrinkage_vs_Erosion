
# coding: utf-8

# Import modules to deal with data and load up test file.

# In[1]:


import numpy as np
import os
import nibabel as nib
import matplotlib.pyplot as plt
import skimage.filters
import skimage.morphology
from skimage import feature

inputFile = "D:/fullGTVfixed" #  file containing full GTV niftis
outputFile = "D:/i20o20masksNew"
radius_of_mask =  2 # radius of mask in pixels (1 px is equivalent to 1 mm)

def show_slice(slice_obj):
	    # Function to display row of image slices
	    fig, axes = plt.subplots(1)
	    axes.imshow(slice_obj, cmap="gray", origin="lower")

filenames = os.listdir(inputFile)
for filename in filenames:
	file = os.path.join(inputFile, filename)
	img = nib.load(file)
	img_data = img.get_data() # puts data into format plt can use

	# Show slices of raw data as an image

	# In[2]:


	# function to show slices as an object
	
	output_array = np.zeros(np.shape(img_data))    
	#scan_slice = img_data[:,:,80]
	for i in range(np.shape(img_data)[2]):
		scan_slice = img_data[:,:,i]
		scan_slice[np.where(scan_slice > 0)] = 255 # gets rid of grey regions (see lab book 28/11/2017)
		# Get pixels around the tumour in scan slice
		edges = feature.canny(scan_slice,sigma=2)

		# apply point iterative filer to get mask
		mask = skimage.filters.rank.maximum(edges,skimage.morphology.disk(radius_of_mask))
		output_array[:,:,i] = mask

	output_array = np.array(output_array)
	nifti_image = nib.Nifti1Image(output_array,np.eye(4)) # create mask nifti to be saved
	nib.save(nifti_image,os.path.join(outputFile,filename.replace("registered_OARsGTV.nii","i20o20maskNew.nii")))





