"""
Active Contour Calculator


Finds the circumference of an active contour around a tumour volume from
loaded .nii files. Should load all of them from set file and create .csv
file with all contour lengths from all slices for each patient. 

N.B. - takes a while...

"""

# Import dependencies
import numpy as np
import math
import nibabel as nib
import os
from skimage.filters import gaussian
from skimage.segmentation import active_contour
import csv
import progressbar

# Function that loads the .nii file as a numpy array
def get_img(filename):
	gtv = nib.load(filename).get_data()
	return gtv

# Function that returns the indices of the array where the slices
# contain GTV delineations
def get_tumour_indices(img):
	indexcounter = []
	i=0
	while i < 120:
		if np.sum(gtv[:,:,i]) != 0:
			indexcounter.append(i)
			j=i
			i=119
			while j<120:
				if np.sum(gtv[:,:,j]) == 0:
					indexcounter.append(j)
					j=119
				j+=1
		i+=1
	return indexcounter

# Function that calculates circumference of contour
def get_contour_length(img):
    if np.sum(img) == 0:
        return 0 # returns 0 if there is no GTV delineation in slice
    else:
		# threshold image above 600 HU
        img[img<600] = 0
		
		# initialise the contour as a circle around the maximum value in GTV
        s = np.linspace(0, 2*np.pi, 400)

        init_point = [np.where(img[:,:]==np.amax(img))[0][0], 
                      np.where(img[:,:]==np.amax(img))[1][0]] 
        x = init_point[1] + 50*np.cos(s)
        y = init_point[0] + 50*np.sin(s)
        init = np.array([x, y]).T
		
		# Perform "snake" contour fit
        snake = active_contour(img, init, alpha=0.15, beta=0.13, 
                               gamma=0.001, w_line=0, w_edge=1, 
                               bc='periodic', max_px_move=1., 
                               max_iterations=5000, convergence=0.001)
							   
		# Find length by doing linear size between adjacent points 
		# (can approximate due to size of circumference and number of
		# points)
        r = [np.sqrt(math.pow(snake[i,0]-snake[i-1,0],2)
                     +math.pow(snake[i,1]-snake[i-1,1],2)) 
             for i in range(1,len(snake[:,0]))]
        return sum(r)
		
		
# Load .nii files containing burned GTV delineations
# (this would be for one patient, in my case NSCLC1)
# Folder should contain .nii images of scans


main = "D:/FullTumourNiftys"
patient = os.listdir(main)
patientpath = [os.path.join(main, i) for i in patient]
for folder in patientpath:
# Run through slices of each scan of each patient, append to an array

	img_file_names = os.listdir(folder)
	img_file_names = [os.path.join(folder, i) for i in img_file_names]
	contour_array = []
	for filename in img_file_names:
		print("Loading file: " + filename)
		img = get_img(filename)
		p,q,r = img.shape
		contour_lengths= []
		bar = progressbar.ProgressBar(redirect_stdout=True)
		for j in range(0,r-1):
			per_cent = np.rint(j/(r-1))
			contour_lengths.append(get_contour_length(img[:,:,j]))
			bar.update(per_cent)
		contour_array.append(contour_lengths)
		print("File done.")
		
	# Write to csv file
	print("Contours calculated. Writing to file...")
	subject = folder[-7:] + ".csv"
	with open(os.path.join(main,subject), "wb") as f:
		writer = csv.writer(f)
		writer.writerows(contour_array)
	
	print("File written.")