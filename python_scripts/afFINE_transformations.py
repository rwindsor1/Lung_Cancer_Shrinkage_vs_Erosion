import os
import nibabel as nib
import numpy as np

path = "D:/fullscans"
pathlets = os.listdir(path)
for pathlet in pathlets:
	scans = os.listdir(os.path.join(path,pathlet))
	for scan in scans:
		scan_data = nib.load(os.path.join(path,pathlet,scan)).get_data()
		print(scan_data.shape)
		out_nib = nib.Nifti1Image(scan_data.astype(int),np.identity(4))
		nib.save(out_nib, os.path.join(path,pathlet,scan).replace(".nii","a.nii"))