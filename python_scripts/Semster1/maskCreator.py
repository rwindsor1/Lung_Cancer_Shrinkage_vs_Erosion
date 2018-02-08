import numpy as np
import os
import nibabel as nib
import matplotlib.pyplot as plt
import scipy.ndimage
from skimage import feature
import skimage
from PIL import Image
from skimage.viewer import ImageViewer	


# function to show slices
def show_slice(slice_obj):
    # Function to display row of image slices
    fig, axes = plt.subplots(1)
    axes.imshow(slice_obj, cmap="gray", origin="lower")

# set HU value to threshold tumours at
THRESHOLD = 500
# set radius of mask in mm
radius_of_mask = 2
# paths to files containing GTVs and progScansFile
GTVFile = "D:/GTVdelins"
progScansFile = "D:/ProgNii"


GTVnames = os.listdir(GTVFile)
progScanNames = os.listdir(progScansFile)
outputFile = "D:/i20o20masksNew3"
for GTVname in GTVnames:
	flag = 0
	# get name of relevant full scan for given GTV
	for progScanNameIterate in progScanNames:
		if progScanNameIterate[0:3] == GTVname[0:3]:
			progScanName = progScanNameIterate
			print(progScanName)
			flag = 1
			break

	if flag == 0:
		continue
	# load up .nii files
	GTVVolData= nib.load(os.path.join(GTVFile,GTVname)).get_data()
	FullScanData = nib.load(os.path.join(progScansFile,progScanName)).get_data()

	# use GTV mask to get relevant area of FullScanData
	combinedData = np.zeros(GTVVolData.shape)
	combinedData[np.where(GTVVolData > 0)] = FullScanData[np.where(GTVVolData > 0)]
	pixels_before_threshold = int(combinedData[np.where(combinedData>0)].shape[0])

	# remove all areas of tumour below threshold
	combinedData[np.where(combinedData < THRESHOLD)] = 0
	pixels_after_threshold = int(combinedData[np.where(combinedData>0)].shape[0])

	# print out user message telling them name of scan and how many pixels have been
	# thresholded away
	print(" Name of Patient: %s \n Pixels before thresholding: %i \n Pixels after thresholding: %i" %(GTVname,pixels_before_threshold,pixels_after_threshold))


	# fill volume for each sllice using binary_fill_holes.get edges of filled volume using canny edge detector. Then create mask of rad
	output_array = np.zeros(combinedData.shape)
	for i in range(np.shape(combinedData)[2]):
		scan_slice = combinedData[:,:,i]
		# Get pixels around the tumour in scan slice
		scan_slice = scipy.ndimage.binary_fill_holes(scan_slice)
		#scan_slice = skimage.morphology.remove_small_objects(scan_slice.astype(bool), min_size=20, connectivity=1, in_place=False)
		edges = feature.canny(scan_slice,sigma=2)

		# apply point iterative filer to get mask
		mask = skimage.filters.rank.maximum(edges,skimage.morphology.disk(radius_of_mask))
		output_array[:,:,i] = mask
	nifti_image = nib.Nifti1Image(output_array,np.eye(4))
	nib.save(nifti_image,os.path.join(outputFile,GTVname.replace("_GTVdelin.nii","i20o20maskNew3.nii")))