#!/usr/bin/env python
# title: firstfit.py
# author: Joahannes Costa <joahannes@lrc.ic.unicamp.br>
# date: 15.04.2021

def heuristica_FFD(valor_bin, itens):

	n = len(itens)

	order = sorted([i for i in range(n)], key=lambda i: itens[i], reverse=True)

	bin_for_item = [-1 for i in range(n)]
	bin_space = []

	for i in order:
		for j in range(len(bin_space)):

			if itens[i] <= bin_space[j]:

				bin_for_item[i] = j
				bin_space[j] -= itens[i]
				break

		if bin_for_item[i] < 0:

			j = len(bin_space)
			bin_for_item[i] = j
			bin_space.append(valor_bin -  itens[i])

	n_bins = len(bin_space)

	return bin_for_item

def get_items_bpp(lista_tarefas, resultado):

	controle = {controle : [] for controle in range(len(lista_tarefas))}

	for i in range(len(resultado)):
		for j in controle:
			if i in controle:
				controle[resultado[i]].append(i)
				break

	contem = []
	remocao = []
	for i in controle:
		if len(controle[i]) > 0:
			contem.append(i)
		else:
			remocao.append(i)

	for i in remocao:
		if i in controle:
			controle.pop(i)

	return controle

def get_best_allocation(valor_bin, lista, resultado):

	resultado = resultado.copy()
	lista = lista.copy()

	best = {}

	for i in resultado:
		best[i] = {}
		soma = 0
		num_itens = 0
		num_itens = len(resultado[i])
		for j in resultado[i]:
			soma = soma + lista[j]
		best[i]['soma'] = soma
		best[i]['itens'] = num_itens
		# print(i, soma, num_itens)

	maximo = 0
	id_maximo = -1
	for i in best:
		if best[i]['itens'] > maximo:
			maximo = best[i]['itens']
			id_maximo = i

	return id_maximo