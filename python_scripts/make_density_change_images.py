import nibabel as nib
import os
import matplotlib.pyplot as plt
import os
import cv2
import numpy as np

# if mode is "init scan" then uses initial scan
# if mode is "s2s" then uses previous scan

mode = "s2s"
path = "D:/tumourNiftis"

for patient in os.listdir(path):
	print(patient)
	scans = os.listdir(os.path.join(path,patient))
	init_scan = nib.load(os.path.join(path,patient,scans[0]))
	init_scan_data = init_scan.get_data()
	ymin = np.where(init_scan_data != 0)[0].min()
	ymax = np.where(init_scan_data != 0)[0].max()+1
	xmin = np.where(init_scan_data != 0)[1].min()
	xmax = np.where(init_scan_data != 0)[1].max()+1
	for scan in scans:
		if scan == scans[0]:
			continue
		if(mode == "s2s"):
			init_scan_data = init_scan = nib.load(os.path.join(path,patient,scans[scans.index(scan)-1])).get_data()
		comparison_scan = nib.load(os.path.join(path,patient,scan)) 
		comparison_scan_data = comparison_scan.get_data().astype(float)
		comparison_scan_data[comparison_scan_data == 0] = np.nan
		diff = comparison_scan_data - init_scan_data
		for i in range(init_scan_data.shape[2]):
			fig,ax = plt.subplots(1)
			ax.set_facecolor('black')
			plot = ax.imshow(diff[ymin:ymax,xmin:xmax,i],cmap = "jet")
			fig.colorbar(plot)
			plt.title("Change in Density:"+patient+ " " +scan[scan.find("scan"):scan.rfind(".nii")]+ " slice: " + str(i))
			plt.tight_layout()
			try:
				plt.savefig("D:/s2s-change-in-density-pics/" + patient+"/" +scan[:scan.rfind("_")]+ "_slice" + str(i) + ".png")
			except:
				os.mkdir("D:/s2s-change-in-density-pics/"+patient)
				plt.savefig("D:/s2s-change-in-density-pics/" + patient+"/"+scan[:scan.rfind("_")]+ "_slice" + str(i) + ".png")
			plt.close()