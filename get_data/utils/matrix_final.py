import sumolib
import matplotlib.pyplot as plt

# parse the net
#net = sumolib.net.readNet('../scenario/porto.net.xml')

X = [-8.65, -8.61857143, -8.58714286, -8.55571429, -8.52428571, -8.49285714, -8.46142857, -8.43]
Y = [41.14, 41.14428571, 41.14857143, 41.15285714, 41.15714286, 41.16142857, 41.16571429, 41.17]

cells = 7

points = {}

for linha in range(len(X)):
	points[linha] = {}
	lines = []
	for coluna in range(len(Y)):
		lines.append((Y[coluna], X[linha]))

	points[linha] = lines


final = {}

for ponto in points:
	final[ponto] = {}
	lista = []
	# print(points[ponto])
	for i in range(cells + 1):
		for j in range(1,i+2):
			if i != j and j > i:
				# print(points[ponto][i],points[ponto][j])
				lista.append(points[ponto][i])
				lista.append(points[ponto][j])
			if j == cells:
				break
	final[ponto] = lista

for i in range(len(final)):
	if i > 0 and i < 7:
		print(final[i])
		print(final[i])
	else:
		print(final[i])