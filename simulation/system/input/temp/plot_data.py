import matplotlib.pyplot as plt
import glob

files = glob.glob("*.txt")
files = sorted(files)

for file in files:
	x = []
	y = []
	now = open(file, "r")
	for i in now:
		x.append(int(i.split()[0]))
		y.append(int(i.split()[1]))

	plt.plot(x,y)
	plt.title(file)
	plt.savefig('img/' + file.split(".")[0] + '.png', dpi=200, bbox_inches = 'tight', pad_inches = 0.05)
	plt.close()