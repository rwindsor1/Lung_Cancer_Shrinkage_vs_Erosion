import os
file_loc = "C:/Users/Rhydian/Documents/Work/MPhysProject/project_data_csv"
for i in os.listdir(file_loc):
    file = open(file_loc + "/" +i,'r')
    for line in file:
        entry = line.split(",")
        entry[-1] = entry[-1][:-2]
        entry = [i[:-4]] + entry
        print(entry)
    