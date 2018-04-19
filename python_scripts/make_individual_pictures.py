import sys
sys.path.insert(0, 'C:/Users/Rhydian/Documents/GitHub/Lung_Cancer_Shrinkage_vs_Erosion/python_scripts/')
import numpy as np 
import matplotlib.pyplot as plt
import nibabel as nib
import scipy.misc

import os
from mphys_project_functions import show_slice

mode = 2 # 0 for real data, 1 for fragmenting sims, 2 for elastic sims

if mode == 0:
	input_folder = "D:" + os.sep + "tumourNiftis"
	for patient in os.listdir(input_folder):
		current_path = os.path.join(input_folder,patient) # path to patient file
		print("new patient")
		for scan in os.listdir(current_path):
			path_to_scan = os.path.join(current_path,scan) # path to scan file
			tumour_nifti = nib.load(path_to_scan)
			tumour_data = tumour_nifti.get_data()
			for slice_num in range(tumour_data.shape[2]):
				slice_data = tumour_data[:,:,slice_num]
				scan_num = scan[scan.find("_")+1:scan.rfind("_")]
				scan_name = patient + "_" + str(scan_num) + "_" + str(slice_num) + ".png"
				scipy.misc.imsave(os.path.join("D:/all-pics2",scan_name), tumour_data[:,:,slice_num])
				


if mode == 1:
	input_folder = "D:" + os.sep + "simulated_niftis"+os.sep+"fragmenting"
	for patient in os.listdir(input_folder):
		current_path = os.path.join(input_folder,patient) # path to patient file
		print("new patient")
		for scan in os.listdir(current_path):
			path_to_scan = os.path.join(current_path,scan) # path to scan file
			tumour_nifti = nib.load(path_to_scan)
			tumour_data = tumour_nifti.get_data()
			for slice_num in range(tumour_data.shape[2]):
				slice_data = tumour_data[:,:,slice_num]
				scan_num = scan[scan.rfind("_")+1:scan.rfind(".")]
				scan_name = patient + "_" + str(scan_num) + "_" + str(slice_num) + ".png"
				scipy.misc.imsave(os.path.join("D:/all-pics-fragmenting-sim",scan_name), tumour_data[:,:,slice_num])


if mode == 2:
	input_folder = "D:" + os.sep + "simulated_niftis"+os.sep+"non-fragmenting"
	for patient in os.listdir(input_folder):
		current_path = os.path.join(input_folder,patient) # path to patient file
		print("new patient")
		for scan in os.listdir(current_path):
			path_to_scan = os.path.join(current_path,scan) # path to scan file
			tumour_nifti = nib.load(path_to_scan)
			tumour_data = tumour_nifti.get_data()
			for slice_num in range(tumour_data.shape[2]):
				slice_data = tumour_data[:,:,slice_num]
				scan_num = scan[scan.rfind("_")+1:scan.rfind(".")]
				scan_name = patient + "_" + str(scan_num) + "_" + str(slice_num) + ".png"
				scipy.misc.imsave(os.path.join("D:/all-pics-elastic-sim",scan_name), tumour_data[:,:,slice_num])