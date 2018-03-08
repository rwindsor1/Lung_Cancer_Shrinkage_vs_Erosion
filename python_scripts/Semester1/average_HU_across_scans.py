import numpy as np
import matplotlib.pyplot as plt
import nibabel as nib
import os

inputFile = "D:/combinedNiftis"
outputFile = "D:/TumourMeanCSVs"
pictureFile = "D:/annulusMeanHUchange"
patientNames = os.listdir(inputFile)
for patientName in patientNames:
	scanNames = os.listdir(os.path.join(inputFile,patientName))
	outputfile = open(os.path.join(outputFile,patientName)+".csv","w")
	mean_list = []
	for scanName in scanNames:
		arr = nib.load(os.path.join(inputFile,patientName,scanName)).get_data()
		mean = arr[np.where(arr != 0)].mean()
		print(mean)
		mean_list.append(mean)
		outputfile.write(str(mean))
		outputfile.write("\n")
	outputfile.close()
	print(mean_list)
	plt.plot(range(1,len(mean_list)+1),mean_list)
	plt.xlabel("ScanNumber")
	plt.ylabel("MeanHU")
	plt.title(patientName+" Mean HU of Annulus versus scan number")
	plt.savefig(os.path.join(pictureFile,patientName)+".PNG")
