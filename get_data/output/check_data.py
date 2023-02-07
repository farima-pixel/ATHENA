
import glob

files = glob.glob("data/*.txt")
files = sorted(files)

time = 1003110

for file in files:
	# print(file)
	filename = open(file, "r")
	for step in filename:
		if int(step.split()[0]) == time:
			print(file.split("/")[1].split("_")[1].split(".")[0], step.split()[1])