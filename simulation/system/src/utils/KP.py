
def KP(size, local_tasks, local_values):

	# CRIA ESTRUTURA DE CONTROLE DE ID
	controle = {}
	escalonadas = {}

	cont = 0
	for task in local_tasks:
		controle[cont] = task
		cont += 1

	W = size
	wt = []
	val = []
	for i in range(len(local_tasks)):
		id_tarefa = controle[i]
		wt.append(local_tasks[id_tarefa])
		val.append(local_values[id_tarefa])

	result = []
	result1 = 0
	n = len(val)
	K = [[0 for x in range(W + 1)] for x in range(n + 1)]

	# Build table K[][] in bottom up manner
	for i in range(n + 1):
		for w in range(W + 1):
			# base case
			if i == 0 or w == 0:
				K[i][w] = 0
			elif wt[i-1] <= w:
				K[i][w] = max(val[i-1] + K[i-1][w-wt[i-1]], K[i-1][w])
			else:
				K[i][w] = K[i-1][w]

	# stores the result of Knapsack
	res = K[n][W]
	# print res

	w = W
	for i in range(n, 0, -1): 
		if res <= 0:
			break

		if res == K[i - 1][w]:
			continue
		else:
			# This item is included. 
			# print i-1, wt[i-1], val[i-1]
			result.append([i-1, wt[i-1], val[i-1]])
			result1 += wt[i-1]

			# Since this weight is included 
			# its value is deducted 
			res = res - val[i - 1] 
			w = w - wt[i - 1]

	# return K[n][W], len(result), result

	for i in result:
		id_task = i[0]
		# print(controle[id_task])
		escalonadas[controle[id_task]] = -1

	return escalonadas

def get_real_task(resultado):
	
	best_scheduling = {}

	return best_scheduling