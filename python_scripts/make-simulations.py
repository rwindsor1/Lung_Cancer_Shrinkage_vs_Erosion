import sys
sys.path.insert(0, 'C:/Users/Rhydian/Documents/GitHub/Lung_Cancer_Shrinkage_vs_Erosion/python_scripts/')
import os
import nibabel as nib
import numpy as np
from mphys_project_functions import fragmenting_sim, elastic_sim


# parameters to change
no_of_interations = 5
simulation_type = "non-fragmenting" # should be "non-fragmenting" or "fragmenting"
input_path = "D:/tumourNiftis"
output_path = "D:/simulated_niftis"
patients = os.listdir(input_path)

# error message if invalid answer for simulation_type
if (simulation_type != "non-fragmenting") & (simulation_type != "fragmenting"):
	print("Error : simulation_type must equal either \" fragmenting \" or \" non-fragmenting \" !")
	exit()



# get first nifti for each patient
for patient in patients:
	arr = nib.load(os.path.join(input_path,patient,os.listdir(os.path.join(input_path,patient))[0])).get_data()
	for i in range(no_of_interations):
		if simulation_type == "fragmenting":
			arr = fragmenting_sim(arr)
		else:
			arr = elastic_sim(arr)

		out_nib = nib.Nifti1Image(arr,np.identity(4))
		if os.path.exists(os.path.join(output_path,simulation_type,patient)) == False:
			os.mkdir(os.path.join(output_path,simulation_type,patient))

		nib.save(out_nib,os.path.join(output_path,simulation_type,patient)+"/"+patient+ "_"+ simulation_type + "_"+ str(i) + ".nii")



