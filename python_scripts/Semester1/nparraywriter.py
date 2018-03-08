
# coding: utf-8

# In[25]:


import nibabel as nib # used to read in nifti files
import os
import numpy as np
from skimage.viewer import CollectionViewer
#from matplotlib.backends.qt_compat import QtWidgets, QtCore, QtGui
import matplotlib.pyplot as plt
# In[31]:
# load in data

masktype = "insidemasksnew" # name of folder containing masks
file_address = "C:/Users/Rhydian/Documents/Work/MPhysProject/nifty folder/" # directory containing both nifti files
output_file = "C:/Users/Rhydian/Documents/Work/MPhysProject/nparrays/inside/"
mask_names = os.listdir(file_address + masktype) # name of mask nifti
true_img_names = os.listdir(file_address + "fullscans") # name of reference scan nifti
for mask_name in mask_names:
    if mask_name[:7] ==  "NSCLC6_" or mask_name[:7] == "NSCLC10":
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
            print(mask_name)
            print(mask_data.shape)
            print(true_data.shape)
            errcount = 0
            if mask_data.shape == true_data.shape:
                print(np.amax(mask_data))
                print(np.amax(true_data))
                arr = np.swapaxes(true_data*(mask_data/255),2,0)
                print(np.amax(arr))
                print("Merge Completed")
            else:
                errcount += 1
           
            if errcount == 0:
                arr[arr==0] = np.nan
                np.save(output_file+true_img_name[0:7]+"scan" +true_img_name[-5]+mask_name[0:8],arr)
            """plt.hist(arr[~np.isnan(arr)],bins=50)
            plt.xlabel("HU")
            plt.ylabel("Frequency")
            plt.title(true_img_name[0:7]+" scan" +true_img_name[-5]+ " " +mask_name[0:11])
            plt.show()"""
            
    


"""            output_file = open("C:/Users/Rhydian/Documents/Work/MPhysProject/project_fulldata_csv/"+true_img_name + "outside.csv" ,'w')
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

"""


