import json
from shapely.geometry import Point, Polygon
import matplotlib.pyplot as plt

f = open('cells.json')
cells = json.load(f)
f.close()

for i in cells:
	cont = 0
	for j in cells[i]:
		if int(i) == 2:
			x = j[0]
			y = j[1]
			plt.scatter(x, y, c='k',zorder=2)
		else:
			x = j[0]
			y = j[1]
			plt.scatter(x, y,c='k',zorder=2)
		
		if cont == 0:
			plt.annotate(i, (x+(x*0.06), y+(y*0.05)))

		cont += 1

plt.show()