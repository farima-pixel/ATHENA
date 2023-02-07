
# -*- coding: UTF-8 -*-

# File name: plot_results.py
# Author: Joahannes Costa
# Data create: 14/12/2017
# Data last modified: 14/12/2017
# Python version: 2.7
# Description: plota graficos de linha para algoritmos de disseminacao

from __future__ import division

from matplotlib.ticker import FormatStrFormatter

import math
import matplotlib.pyplot as plt
import numpy as np
from numpy import *

import matplotlib as mpl

# identificacao dos algoritmos
ALGORITHM = (1,2,)

# print(min(ALGORITHM))

# configuracoes de estilo
LABEL = {
	1 : r"$\lambda$ = 1",
	2 : r"$\lambda$ = 2",
	3 : r"$\lambda$ = 3",
	4 : r"$\lambda$ = 4",
	5 : r"$\lambda$ = 5",
}

MARKS = {
	1 : "s", #GREEDY-1
	2 : "s", #DP-1
	3 : "o", #CRATOS
	4 : "v", #GREEDY-VALUE
	5 : "o", #GREEDY-N
}

style = "-"

LINES = {
	1 : style,
	2 : style,
	3 : style,
	4 : style,
	5 : style,
}

norm = mpl.colors.Normalize(vmin=min(ALGORITHM), vmax=max(ALGORITHM)+2)
cmap = mpl.cm.ScalarMappable(norm=norm, cmap=mpl.cm.Greys)
cmap.set_array([])

#VARIABLES PLOT
X_LEGEND = u'Time (s)'

x_fig = 7 #6.8
y_fig = 6 #5.5

markersize = 0
linewidth = 3

formato = '.eps'
legenda_size = 16

cenario_raio = '100'
recursos = '1'

# 24h 		= 0, 87480
# 6h-9h 	= 21600, 32400
# 14h-16h	= 50400, 57600
inicio = 0
final = 500

def plot_time():

	
	for algorithm in ALGORITHM:

		file_input_name = 'task_seed_1_rate_' + str(algorithm) + '.txt'

		x = []
		y = []

		cont = 0
		valor = 0
		for line in open(file_input_name):

			if int(line.split()[0]) > inicio and int(line.split()[0]) < final:

				x.append(cont)
				# x.append(int(line.split()[0]))
				valor += int(line.split()[0])
				y.append(valor)

				cont += 1

		# x = np.divide(x, 1000)
		y = np.divide(y, 1000)

		plt.plot(x, y, color=cmap.to_rgba(algorithm+2), linestyle=LINES[algorithm], linewidth=linewidth, markersize=markersize, marker=MARKS[algorithm], label=LABEL[algorithm])		


	# plt.axvline(x=50400, linewidth=0.8, linestyle='--', color='k')
	# plt.axvline(x=57600, linewidth=0.8, linestyle='--', color='k')

	# xticks = np.arange(x_min, x_max, 7200)
	# xname = np.arange(0,9000,1000)
	plt.xlabel('Time (s)', fontsize=legenda_size)
	plt.xticks(fontsize=legenda_size)

	# yticks = np.arange(0, 20, 3)
	plt.yticks(fontsize=legenda_size)
	plt.ylabel('Number of tasks queued (# x 1000)', fontsize=legenda_size)
	
	plt.grid(color='0.9', linestyle='--', linewidth=0.4, axis='both', alpha=0.1)
	# # plt.grid(True, which="both", ls="-", linewidth=0.1, color='0.90', zorder=0)
	plt.legend(
		numpoints 	= 1,
		loc 		= 'best',
		ncol		= 1,
		fancybox 	= False,
		# frameon 	= True,
		shadow		= False,
		# borderpad	= 0.5,
		edgecolor	= 'k',
		fontsize 	= legenda_size
		)

	# plt.axvspan(50400, 57600, facecolor='0.9', alpha=0.9)

	fig = plt.gcf()

	# plt.yscale('log')

	# plt.ylim(-1, 20, 4)


	# # plt.gca().spines['right'].set_color('none')
	# plt.gca().spines['top'].set_color('none')

	# fig.set_size_inches(6.8, 5.5)
	fig.set_size_inches(x_fig, y_fig)
	fig.savefig('fila_tarefas' + formato, dpi=200, bbox_inches = 'tight', pad_inches = 0.05)
	# plt.show()
	plt.close()


if __name__ == "__main__":

	plot_time()