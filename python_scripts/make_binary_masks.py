import os
import nibabel as nib
import numpy as np


path_to_masks = "D:/tumourNiftis"
patients = os.listdir(path_to_masks)
for patient in patients:
	patient_path = os.path.join(path_to_masks,patient)
	scan = os.listdir(patient_path)[0]
	patient_data = nib.load(os.path.join(patient_path,scan)).get_data()
	patient_data[patient_data>0] = 1
	patient_data = patient_data.astype(int)
	img = nib.Nifti1Image(patient_data, np.eye(4))
	nib.save(img,"D:/niftyfolder/masks/"+patient+"mask.nii")
