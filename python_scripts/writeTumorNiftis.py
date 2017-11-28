import numpy as np
import nibabel as nib # used to read in nifti files
import os

fileAddress = "C:/Users/Rhydian/Documents/Work/MPhysProject/nifty folder/" # directory containing both nifti files
maskSet = "insidemasksnew" # selects which masks to use
scanSet = "fullscans" # selects which set of scans to use
maskNames = os.listdir(os.path.join(fileAddress,maskSet)) # name of mask nifti
fullScanNames = os.listdir(os.path.join(fileAddress,scanSet)) # name of reference scan nifti
print(maskNames[-1])
for maskName in maskNames:
	if maskName[0:4] !="SABR":
		continue

	relevantScanNames = []
	for fullScanName in fullScanNames:
		if fullScanName[0:7] == maskName[0:7]:
			relevantScanNames.append(fullScanName)
	print(relevantScanNames)
	for relevantScanName in relevantScanNames:
		# load up nifti files
		scan = nib.load(os.path.join(fileAddress,scanSet,relevantScanName))
		mask = nib.load(os.path.join(fileAddress,maskSet,maskName))
		# put nifti files into np array and set all mask values to 1 or 0 and all
		# scanArr values which are 1 to zero
		scanArr = np.array(scan.get_data())
		maskArr = np.array(mask.get_data())
		scanArr[np.where(scanArr == 1)] = 0
		maskArr[np.where(maskArr == 255)] = 1
		# apply mask to scan by multiplying them together and put into outputArr
		outputArr = scanArr*maskArr
		# save outputArr as a nifti file
		outputNifti = nib.Nifti1Image(outputArr, np.eye(4))
		if not (os.path.exists(os.path.join("D:/niftyfolder",relevantScanName[0:7]))):
			os.makedirs	(os.path.join("D:/niftyfolder",relevantScanName[0:7]))
		nib.save(outputNifti,os.path.join("D:/niftyfolder",relevantScanName[0:7],relevantScanName))

print("done")
"""
mask_img = nib.load(file_address+mask_name)
mask_data = mask_img.get_data()
true_img = nib.load(file_address+true_img_name)
true_data = true_img.get_data()
print(mask_data.shape)
print(true_data.shape)
mask_data = np.array(mask_data)
true_data = np.array(true_data)
true_data[np.where(true_data == 1)] = 0 # set the minimum value of true data to zero
mask_data[np.where(mask_data == 255)] = 1 # set max values of the true data to 1 to make multiplication easier


px_count = [] # array to store each slice of CT scan in
for i in range(0,120,1):
    slice_i = mask_data[:, :, i]
    px_count.append(slice_i)
    
show_slice(true_data[:, :, 60]) # show slice from reference scan
plt.suptitle("Reference Scan Slice") # 
show_slice(mask_data[:, :, 60])

plt.show()


# In[258]:


# combine mask with full scan pixel values

mask_data_new = mask_data*true_data
print(mask_data_new.min())
show_slice(mask_data_new[:, :, 170])
plt.suptitle("Center slices for image")
plt.show(


"""