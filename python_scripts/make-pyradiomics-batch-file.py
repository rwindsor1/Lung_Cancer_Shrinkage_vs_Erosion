import os

outputfile = open("D:/simulation-batch-file.csv","w")
outputfile.write( "Image,Mask,ID \n" )
pathtoniftis = "D:\simulated_niftis"

for mode_of_recession in os.listdir(pathtoniftis):
	patients = os.listdir(os.path.join(pathtoniftis,mode_of_recession))
	for patient in patients:
		niftis = os.listdir(os.path.join(pathtoniftis,mode_of_recession,patient))
		for nifti in niftis:
			pathtowrite = os.path.join(pathtoniftis,mode_of_recession,patient,nifti)
			outputfile.write(pathtowrite +"," + "D:" +os.sep+ "niftyfolder" +os.sep+ "masks" +os.sep + patient +"mask.nii" +"," + nifti + "\n")

outputfile.close()