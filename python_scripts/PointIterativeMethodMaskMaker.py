
# coding: utf-8

# Import modules to deal with data and load up test file.

# In[1]:


import numpy as np
import os
import nibabel as nib
import matplotlib.pyplot as plt

datafile = "F:/fullGTV"
filenames = os.listdir(datafile)
file = os.path.join(datafile, filenames[0])
img = nib.load(file)
img_data = img.get_data() # puts data into format plt can use


# Show slices of raw data as an image

# In[2]:


# function to show slices as an object
def show_slice(slice_obj):
    # Function to display row of image slices
    fig, axes = plt.subplots(1)
    axes.imshow(slice_obj, cmap="gray", origin="lower")
    
scan_slice = img_data[:,:,80]
show_slice(img_data[:,:,80]) # use 80 as default slide number for testing
plt.show()


# Get pixels around the tumour in scan slice

# In[3]:


from skimage import feature

edges = feature.canny(scan_slice,sigma=2)
show_slice(edges) # show edges of image
print(edges.max())
plt.show()


# In[8]:


import skimage.filters
import skimage.morphology
mask = skimage.filters.rank.maximum(edges,skimage.morphology.disk(2))
show_slice(edges_new[200:250,150:220])
plt.show()


# In[ ]:




