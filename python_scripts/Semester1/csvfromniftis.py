
# coding: utf-8

# In[25]:


import nibabel as nib # used to read in nifti files
import os

# In[31]:
# load in data

masktype = "insidemasksnew" # name of folder containing masks
file_address = "C:/Users/Rhydian/Documents/Work/MPhysProject/nifty folder/" # directory containing both nifti files
mask_names = os.listdir(file_address + masktype) # name of mask nifti
true_img_names = os.listdir(file_address + "fullscans") # name of reference scan nifti
for mask_name in mask_names:
    if mask_name[:7] = "NSCLC6_"|| mask_name[:7] = "NSCLC10":
        print("Looking for scans in " + mask_name)
        relevant_scans = []
        for name in true_img_names: 
            if name[:7] == mask_name[:7]:
                relevant_scans.append(name)
        print(relevant_scans)
        for true_img_name in relevant_scans:
            print("Loading mask:" + mask_name)
            print("Loading full scan:" + true_img_name)
            
                    
            mask_img = nib.load(file_address+masktype+"/"+mask_name)
            mask_data = mask_img.get_data()
            true_img = nib.load(file_address+"fullscans/"+true_img_name)
            true_data = true_img.get_data()
            print(mask_data.shape)
            print(true_data.shape)
            if mask_data.shape == true_data.shape:
                for i in range(mask_data.shape[0]):
                    for j in range(mask_data.shape[1]):
                        for k in range(mask_data.shape[2]):
                            if mask_data[i,j,k] != 0:
                                mask_data[i,j,k] = mask_data[i,j,k]*true_data[i,j,k]/255
                    if i % 40 == 0:
                        print(str(int(100*i/410)) + " percentage merged")
                
                print("Merge Completed")


                output_file = open("C:/Users/Rhydian/Documents/Work/MPhysProject/project_fulldata_csv/"+true_img_name + "inside.csv" ,'w')
                print("Writing to" + mask_name + ".csv")
                # find mean pixel value
                import numpy as np
                for i in range(mask_data.shape[0]):
                    for j in range(mask_data.shape[1]):
                        for k in range(mask_data.shape[2]):
                            if mask_data[i,j,k] != 0:
                                output_file.write(str(i) +","+str(j)+","+str(k)+","+str(mask_data[i,j,k])+"\n")
                    if i % 40 == 0:
                        print(str(int(100*i/410)) + " percentage written")
                output_file.close()
                print(" Completed writing file")

    # In[ ]:




