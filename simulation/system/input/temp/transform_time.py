import matplotlib.pyplot as plt
import glob

files = glob.glob("*.txt")
files = sorted(files)

print(files)

PATH = 'new/'

for file in files:
	name = file.split("_")[1].split(".")[0]
	now = open(file, "r")
	new = open(PATH + name + '.txt','w')
	cont = 0
	for i in now:
		new.write(str(cont) + '\t' + str(i.split()[1]) + '\n')
		cont += 1
	new.close()

