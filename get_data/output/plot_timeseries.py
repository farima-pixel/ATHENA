

import matplotlib.pyplot as plt

filename = open("data/cell_41.txt", "r")

x = []
y = []

for i in filename:

	x.append(int(i.split()[0]))
	y.append(int(i.split()[1]))

plt.plot(x, y)
plt.show()