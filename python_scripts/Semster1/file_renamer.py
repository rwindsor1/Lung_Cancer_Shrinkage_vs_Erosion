import os

file = "D:/fullscans"

filenames = os.listdir(file)
for filename in filenames:
	prefix = filename[0:7]
	print(prefix)
	if prefix[0] == "N":
		