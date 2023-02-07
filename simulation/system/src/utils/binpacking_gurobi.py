#!/usr/bin/env python
# title: binpacking_gurobi.py
# author: Joahannes Costa <joahannes@lrc.ic.unicamp.br>
# date: 12.04.2021

from gurobipy import *

def model_bpp(c, w, UB=None, bin_for_item=None, LogToConsole=True, TimeLimit=30):
	n = len(w)
	if UB == None:
		UB = n
	model = Model()
	model.params.LogToConsole = LogToConsole
	model.params.TimeLimit = TimeLimit # seconds
	x = model.addVars(n, UB, vtype=GRB.BINARY)
	y = model.addVars(UB, vtype=GRB.BINARY)
	model.setObjective(quicksum(y[j] for j in range(UB)), GRB.MINIMIZE) # minimize the number of bins used
	model.addConstrs(quicksum(x[i,j] for j in range(UB)) == 1 for i in range(n)) # each item in exactly one bin
	model.addConstrs(quicksum(w[i] * x[i,j] for i in range(n)) <= c * y[j] for j in range(UB))

	if bin_for_item != None:
		for i in range(n):
			x[i, bin_for_item[i]].start = 1
	
	model.optimize()

	bin_for_item = [-1 for i in range(n)]
	for i in range(n):
		for j in range(UB):
			if x[i,j].X > 0.5:
				bin_for_item[i] = j

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