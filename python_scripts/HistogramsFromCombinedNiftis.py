# Takes combined Niftis and creates histograms based on them

import numpy as np
import matplotlib.pyplot as plt
import nibabel as nib
import os

inputFile = "D:/fullTumourNiftys"
outputFile = "D:/fullTumourHistograms"
patientNames = os.listdir(inputFile)


for patientName in patientNames:
    scanNames = os.listdir(os.path.join(inputFile,patientName))
    for scanName in scanNames:
        scanPath = os.path.join(inputFile,patientName,scanName)
        scan = nib.load(scanPath)
        scanData = scan.get_data()
        pixelVals = scanData[np.where(scanData>0)]
        values, bins, _ = plt.hist(pixelVals, bins = 200)
        plt.savefig(os.path.join(outputFile,scanName.replace(".nii",".png")))
        plt.clf()



