import os
import shutil

in_path = "D:"+os.sep +"fullTumourPictures"

patients = os.listdir(in_path)


for patient in patients:
	patient_path = os.path.join(in_path,patient)

	scans = os.listdir(patient_path)
	for scan in scans:
		scan_path = os.path.join(patient_path,scan)
		if scan == "all_pictures":
			print("flag")
			continue

		scan_no = scans.index(scan) + 2
		for pic in os.listdir(scan_path):
			slice_num = pic[pic.rfind("-")+1:pic.rfind(".")]
			patient_name = patient[:patient.find("_")]
			pic_out_name = str(patient_name) + "_scan" + str(scan[scan.rfind("n")+1:]) + "_slice" + str(slice_num) +".png"
			pic_out_path = os.path.join("D:" + os.sep , "all-pics",pic_out_name)
			#print(pic_out_path)
			src = os.path.join(in_path,patient,scan,pic)
			print(src)
			shutil.copyfile(src, pic_out_path)