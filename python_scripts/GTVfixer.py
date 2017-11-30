import numpy as np
import os
import nibabel as nib
import matplotlib.pyplot as plt
import skimage.filters
import skimage.morphology
from skimage import feature

inputFile = "D:/fullGTV" #  file containing full GTV niftis
outputFile = "D:/fullGTVfixed"

filenames = os.listdir(inputFile)
for filename in filenames:
	file = os.path.join(inputFile, filename)
	img = nib.load(file)
	img_data = img.get_data() # puts data into format plt can use
	img_data[np.where(img_data>0)] = img_data.max()
	output_array = img_data
	output_array = np.array(output_array)
	nifti_image = nib.Nifti1Image(output_array,np.eye(4)) # create mask nifti to be saved
	nib.save(nifti_image,os.path.join(outputFile,filename))