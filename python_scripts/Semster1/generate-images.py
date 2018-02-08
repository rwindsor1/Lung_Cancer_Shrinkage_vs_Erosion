import os
import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt
import scipy.misc
from PIL import Image
path_to_niftis = "D:/fullTumourNiftys"
output_path = "D:/fullTumourPictures/"
for patient_name in os.listdir(path_to_niftis):

	try:
		os.mkdir(os.path.join(output_path,patient_name))
	except:
		for scan_name in os.listdir(os.path.join(path_to_niftis,patient_name)):
			try:
				os.mkdir(os.path.join(output_path,patient_name,scan_name[:-4]))
			except:
				scan = nib.load(os.path.join(path_to_niftis,patient_name,scan_name))
				scan_data = scan.get_data()
				for slice_num in range(scan_data.shape[2]):
					scipy.misc.imsave(output_path + patient_name + "/" + scan_name[:-4] + "/" + scan_name.replace(".nii","--") + str(slice_num) + ".png", scan_data[:,:,slice_num])
				