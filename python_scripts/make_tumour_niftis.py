import os
import nibabel as nib
import numpy as np

mask_path = "D:/GTVdelins"
scan_path = "D:/fullscans"

for patient in os.listdir(scan_path):
	mask_arr = nib.load(os.path.join(mask_path,patient + "_GTVdelin.nii")).get_data().astype(bool)
	for scan in os.listdir(os.path.join(scan_path,patient)):
		if scan.rfind("a.nii") != -1:
			scan_arr = nib.load(os.path.join(scan_path,patient,scan)).get_data()
			tumour_arr = scan_arr*mask_arr
			outputNifti = nib.Nifti1Image(tumour_arr, np.eye(4))
			if not (os.path.exists(os.path.join("D:/tumourNiftis",patient))):
				os.makedirs	(os.path.join("D:/tumourNiftis",patient))
			nib.save(outputNifti,os.path.join("D:/tumourNiftis",patient,scan.replace("a.nii","_tum.nii")))
