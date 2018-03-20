import sys
sys.path.insert(0, 'C:/Users/Rhydian/Documents/GitHub/Lung_Cancer_Shrinkage_vs_Erosion/python_scripts/')
from mphys_project_functions import fragmenting_sim, show_slice
import nibabel as nib
import matplotlib.pyplot as plt
img = nib.load("D:/fullTumourNiftys/NSCLC1_/NSCLC1__registered_OARsfullscan2.nii").get_data()
for i in range(1):
	img = fragmenting_sim(img)
	print("Loop " + str(i+1) + " of 10")
	show_slice(img[100:200,150:300,60])
plt.show()