#!/usr/bin/env python

import numpy as np
import random
from scipy.stats import poisson
import matplotlib.pyplot as plt

def generate_number_of_tasks(seed, rate, plot):

	# compute poisson
	poisson_set = compute_poisson(rate)

	# requests_ID.txt
	if seed < 10:
		task_file = open('requests_0' + str(seed) + '.txt','w')
	else:
		task_file = open('requests_' + str(seed) + '.txt','w')

	# poisson_set.sort()
	for i in poisson_set:
		task_file.write(str(i) + "\n")
	task_file.close()
	
	if plot == True:
		# descomentar para visualizar o plot da poisson
		count, bins, ignored = plt.hist(
			poisson_set,
			# ,
			facecolor='red',
			edgecolor='black',
			density=True,
			align='mid',
			alpha=0.7)
		plt.xlabel('Number of tasks')
		plt.ylabel(r'$P(X = k) = \frac{e^{-k} . \lambda^k}{k!}$')
		plt.title('Seed: ' + str(seed) + ' - Rate: ' + str(rate))
		plt.savefig('tasks_arrival_seed_'+str(seed)+'_rate_'+str(rate)+'.eps', dpi=200, bbox_inches = 'tight', pad_inches = 0.05)
		plt.close()

	return max(poisson_set)

def compute_poisson(taxa):
	lamb = taxa # esperanca de ocorrencia
	size = 20000
	s = np.random.poisson(lamb,size)
	return s

def plot_poisson(limite):

	PROB = (1,2,3,4,5)

	# TESTE 1
	arr = []

	for i in PROB:
		rv = poisson(i)
		for num in range(0,limite):
	 		arr.append(rv.pmf(num))

		prob = rv.pmf(i)

		plt.xlabel('Number of tasks')
		plt.ylabel(r'$P(X = k) = \frac{e^{-k} . \lambda^k}{k!}$')

		# plt.grid(True)
		plt.plot(arr, linewidth=1.5, label=r'$\lambda = $'+str(i))
		plt.plot([i], [prob], marker='o', markersize=4, color="red")

		arr = []

	plt.legend()

	plt.savefig('tasks_arrival.eps', dpi=400, bbox_inches = 'tight', pad_inches = 0.05)

	plt.close()
	
if __name__ == "__main__":

	# plot_poisson()

	rates = []

	SEED = 50
	# RATE = [1,2,3,4,5]
	RATE = 2

	for seed in range(1,SEED):
		
		rates.append(generate_number_of_tasks(seed, RATE, False))

	plot_poisson(max(rates))