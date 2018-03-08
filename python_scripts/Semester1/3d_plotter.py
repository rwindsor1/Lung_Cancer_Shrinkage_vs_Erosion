import os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pickle
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
patient_name = "NSCLC1"
scan_number = 4
data_folder = "C:/Users/Rhydian/Dropbox/MPhys Lungs Shared Folder/datadump/fullguys/" + patient_name + "/"
save_folder = "C:/Users/Rhydian/Documents/Work/MPhysProject/tumour3dplots/"
file_name =  patient_name + "_registered_OARsfullscan"+str(scan_number)+".nii.csv"
the_file = open(data_folder + file_name,'r')
X, Y, Z,colors = [],[],[],[]
counter = 0
for line in the_file:
    if counter % 3 == False:
        temp_line= line.split(",")
        temp_line[-1].replace("\n","")
        X.append(int(temp_line[0]))
        Y.append(int(temp_line[1]))
        Z.append(int(temp_line[2]))
        colors.append((int(temp_line[3][:-1])/255,0,0))
    counter +=1
figure_title = file_name[:-8]
plt.title(figure_title)
ax.scatter(X,Y,Z,c=colors)
pickle.dump(fig, open(save_folder+file_name+".pickle", 'wb')) # 
plt.show()
