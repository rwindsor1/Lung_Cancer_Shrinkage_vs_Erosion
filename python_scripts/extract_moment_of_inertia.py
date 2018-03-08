import os 
import nibabel as nib
import matplotlib.pyplot as plt
import numpy as np
import scipy.ndimage

filepath = "D:/fullTumourNiftys"
def get_moment_of_inertia(nib_obj):
	intensity_data = nib_obj.get_data()
	CoM = scipy.ndimage.measurements.center_of_mass(intensity_data)
	indices = np.indices(intensity_data.shape)
	indices = np.moveaxis(indices,0,3)
	sqdist_from_CoM = np.zeros(intensity_data.shape)
	sqdist_from_CoM[:,:,:] = (indices[:,:,:,0]-CoM[0])**2+(indices[:,:,:,1]-CoM[1])**2+(indices[:,:,:,2]-CoM[2])**2
	return np.sum(intensity_data*sqdist_from_CoM)

patients = os.listdir(filepath)

fig,ax = plt.subplots()
for patient in patients:
	I_arr = []
	scans = os.listdir(os.path.join(filepath,patient))
	for scan in scans:
		nibfile = nib.load(os.path.join(filepath,patient,scan))
		I_arr.append(get_moment_of_inertia(nibfile))
	I_arr = I_arr/I_arr[0]
	ax.plot(I_arr,label = patient)

ax.set_xlabel("Scan Number")
ax.set_ylabel("Moment of Inertia (HU/px^2)")
ax.legend()

plt.show()