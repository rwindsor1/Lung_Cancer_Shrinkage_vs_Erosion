import os
import nibabel as nib

inFolder = "D:/i20o20masksNew3"
fileName = "N01i20o20maskNew3.nii"

filePath = os.path.join(inFolder,fileName)

img = nib.load(filePath)
nib.viewers.OrthoSlicer3D(img.get_data()).show()