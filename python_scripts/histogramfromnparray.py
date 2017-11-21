import numpy as np
import os
import matplotlib.pyplot as plt
input_file= "C:/Users/Rhydian/Documents/Work/MPhysProject/nparrays/inside"
# arrays to specify area of graphs. each dictionary entry has form [xlim,ylim,bins]
dict = {"NSCLC1_":[1200,900,100],
        "NSCLC2_":[1200,300,80],
        "NSCLC5_":[1200,1400,100],
        "NSCLC6_":[1200,400,100],
        "NSCLC7_":[1200,2200,100],
        "NSCLC10":[1200,500,100],
        "NSCLC11":[1200,1600,200],
        "NSCLC16":[1200,500, 100]}
for file_name in os.listdir(input_file):
    if file_name[0:7] == "NSCLC10":
        
        info_array = dict[file_name[0:7]]
        print(file_name)
        arr = np.load(os.path.join(input_file,file_name))
        print(len(arr[~np.isnan(arr)]))
        fig,ax = plt.subplots(1)
        values, bins, _ = ax.hist(arr[~np.isnan(arr)], bins = info_array[2])
        area = sum(np.diff(bins)*values)
        print("Area: " +str(area))
        plt.title(file_name)
        plt.xlabel("HU")
        plt.ylabel("Frequency")
        ax.set_xlim(0,info_array[0])
        ax.set_ylim(0,info_array[1])
        plt.savefig(os.path.join("C:/Users/Rhydian/Documents/Work/MPhysProject/inside_histograms/31102017",file_name.replace("npy","png")))
        plt.close()
        plt.clf()
        