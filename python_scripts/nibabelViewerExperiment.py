import os
import nibabel as nib

inFolder = "D:/mphysproject/nifty folder/insideMasks"
fileName = "brokenScanNifty.nii"

filePath = os.path.join(inFolder,fileName)

img = nib.load(filePath)
nib.viewers.OrthoSlicer3D(img.get_data()).show()