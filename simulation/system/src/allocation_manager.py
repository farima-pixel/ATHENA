#!/usr/bin/env python
# title: allocation_manager.py
# author: Joahannes Costa <joahannes@lrc.ic.unicamp.br>
# date: 30.03.2021

import log_manager
import random
import time

# schedulers
import scheduler.marina as marina

import src.utils.GWO as GWO

# PARA BIN PACKING
from binpacker import Binpacker
from binpacker import Item

# GUROBI
# import binpacking_gurobi
# HEURISTICA
import firstfit

from AnalyticHierarchyProcess import AHP
ahp = AHP(log=True)

# fila_alocacao = {nuvem0:[0,1,3], nuvem1:[2,4]}
# global fila_alocacao
escalonamento = {}
tarefas_agora = []

nuvens_alloc = 0
recursos_alloc = 0
tempo_alloc = 0

local_vc = 'total'
local_rsu = 'total'

import cluster_manager

# variar tamanho da fila no futuro

def scheduling(step, vclouds, tasks, algorithm):

	print("[DEBUG] >> ESCALONANDO TAREFAS...",step)
	# LIMPAR CONTROLE DE ESCALONAMENTO
	escalonamento.clear()
	tarefas_agora.clear()

	# print("Nuvens:",vclouds)
	print("Tarefas:",tasks)

	for i in tasks:
		tarefas_agora.append(i)

	if algorithm == "CRATOS":
		CRATOS_Alloc(step, vclouds, tasks)

	elif algorithm == "PSO":
		PSO_Alloc(step, vclouds, tasks)

	elif algorithm == "AHP":
		AHP_Alloc(step, vclouds, tasks)

	elif algorithm == "FIFO":
		FIFO_Alloc(step, vclouds, tasks)

	elif algorithm == "UNC":
		UNC_Alloc(step, vclouds, tasks)

	elif algorithm == "MARINA":
		MARINA_Alloc(step, vclouds, tasks)

	else:
		print("ALGORITMO NAO CONHECIDO!")

def get_results(allocated_tasks):
	
	# print("RESULTADOS")
	# print(allocated_tasks)

	a = 0 #reward
	b = 0 #task allocated number
	c = 0 #task size sum

	b = len(allocated_tasks)

	for i in allocated_tasks:
		a += i[2]
		c += i[1]

	return a, b, c

def CRATOS_Alloc(step, vclouds, tasks):

	tasks = tasks.copy()

	total_recursos = 0
	for i,j in vclouds.items():
		total_recursos += j

	numero_de_tarefas = len(tasks)
	numero_de_nuvens = len(vclouds)

	tempo_inicio = time.time()
	MY_SYSTEM(vclouds, tasks)
	tempo_final = time.time()
	tempo_total = tempo_final - tempo_inicio

	# new
	global nuvens_alloc
	global recursos_alloc
	global tempo_alloc
	nuvens_alloc = numero_de_nuvens
	recursos_alloc = total_recursos
	tempo_alloc += tempo_total
	
def PSO_Alloc(step, vclouds, tasks):
	
	tasks = tasks.copy()

	total_recursos = 0
	for i,j in vclouds.items():
		total_recursos += j

	numero_de_tarefas = len(tasks)
	numero_de_nuvens = len(vclouds)

	tempo_inicio = time.time()
	PSO(vclouds, tasks)
	tempo_final = time.time()
	tempo_total = tempo_final - tempo_inicio

	# print("Lista alocadas GWO:",local_alocadas)

	# new
	global nuvens_alloc
	global recursos_alloc
	global tempo_alloc
	nuvens_alloc = numero_de_nuvens
	recursos_alloc = total_recursos
	tempo_alloc += tempo_total

def AHP_Alloc(step, vclouds, tasks):
	
	tasks = tasks.copy()

	total_recursos = 0
	for i,j in vclouds.items():
		total_recursos += j

	numero_de_tarefas = len(tasks)
	numero_de_nuvens = len(vclouds)

	tempo_inicio = time.time()
	ahp_allocation(vclouds, tasks)
	tempo_final = time.time()
	tempo_total = tempo_final - tempo_inicio

	# new
	global nuvens_alloc
	global recursos_alloc
	global tempo_alloc
	nuvens_alloc = numero_de_nuvens
	recursos_alloc = total_recursos
	tempo_alloc += tempo_total

def FIFO_Alloc(step, vclouds, tasks):

	tasks = tasks.copy()

	total_recursos = 0
	for i,j in vclouds.items():
		total_recursos += j

	numero_de_tarefas = len(tasks)
	numero_de_nuvens = len(vclouds)

	tempo_inicio = time.time()
	FIFO(vclouds, tasks)
	tempo_final = time.time()
	tempo_total = tempo_final - tempo_inicio

	# new
	global nuvens_alloc
	global recursos_alloc
	global tempo_alloc
	nuvens_alloc = numero_de_nuvens
	recursos_alloc = total_recursos
	tempo_alloc += tempo_total

def UNC_Alloc(step, vclouds, tasks):
	
	tasks = tasks.copy()

	total_recursos = 0
	for i,j in vclouds.items():
		total_recursos += j

	numero_de_tarefas = len(tasks)
	numero_de_nuvens = len(vclouds)

	tempo_inicio = time.time()
	UNC(vclouds, tasks)
	tempo_final = time.time()
	tempo_total = tempo_final - tempo_inicio

	# new
	global nuvens_alloc
	global recursos_alloc
	global tempo_alloc
	nuvens_alloc = numero_de_nuvens
	recursos_alloc = total_recursos
	tempo_alloc += tempo_total

def MARINA_Alloc(step, vclouds, tasks):
	
	tasks = tasks.copy()

	total_recursos = 0
	for i,j in vclouds.items():
		total_recursos += j

	numero_de_tarefas = len(tasks)
	numero_de_nuvens = len(vclouds)

	tempo_inicio = time.time()
	# MARINA(vclouds, tasks)
	marina.run(vclouds, tasks)
	tempo_final = time.time()
	tempo_total = tempo_final - tempo_inicio

	# new
	global nuvens_alloc
	global recursos_alloc
	global tempo_alloc
	nuvens_alloc = numero_de_nuvens
	recursos_alloc = total_recursos
	tempo_alloc += tempo_total

def weight(tasks):
	tasks = tasks.copy()
	return tasks[1]

def value(tasks):
	tasks = tasks.copy()
	return tasks[2]

def dp_solution_mors(W, wt, val):
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
	return result

def MARINA(vclouds, tasks):

	print("\n -> MARINA")

	tasks = tasks.copy()
	vclouds = vclouds.copy()

	tasks_rsu = tasks.copy()
	# print("RECURSOS:",cluster_manager.recursos)
	
	# CRIA DICIONARIO DE VCS
	recursos_vcs = {}
	for i in cluster_manager.controle_recursos:
		time = {}
		for j in cluster_manager.controle_recursos[i]:
			time[j] = cluster_manager.controle_recursos[i][j]['vc']
		recursos_vcs[i] = time
	
	# CRIA DICIONARIO DE RSUS
	recursos_rsus = {}
	for i in cluster_manager.controle_recursos:
		time = {}
		for j in cluster_manager.controle_recursos[i]:
			time[j] = cluster_manager.controle_recursos[i][j]['rsu']
		recursos_rsus[i] = time

	# print("RECURSOS_VCS:",recursos_vcs[1])

	deadline_temp = {}
	ciclos_temp = {}
	peso_temp = {}
	tarefas_local = {}
	tarefas_sinteticas = {}
	cont = 0
	for i in tasks:
		tarefas_local[cont] = i[1]
		tarefas_sinteticas[cont] = i[0]
		peso_temp[i[0]] = i[1]
		ciclos_temp[i[0]] = i[3]
		deadline_temp[i[0]] = i[4]
		cont += 1
	
	controle_marina = {}

	tarefas = []
	for i in tarefas_local:
		tarefas.append(tarefas_local[i])

	# tasks = sorted(tasks, reverse=False, key=weight)

	# ALOCA NAS VCS
	nuvens = {}
	while len(tasks) > 0:

		if len(recursos_vcs) > 0:

			# print("Restaram:",tasks)

			# --------------------------
			# BIN-PACKING NEXTFIT
			# --------------------------
			# maximo = max_value(vclouds)
			tempo = 0
			maximo = max_value_per_time(recursos_vcs, tempo)
			valor_bin = recursos_vcs[maximo][tempo]
			recursos_vcs.pop(maximo)
		
			controle_valor_bin = 0
			controle_valor_bin = valor_bin

			print("\nNuvem atual:",maximo)
			print("Valor:",valor_bin)

			# maior nuvem menor que a menor tarefa
			min_local = min_value(tasks)
			if valor_bin < min_local:
				print("SEM ESPAÇO NAS VCS!")
				break
		
			# --------------------------
			# BIN-PACKING PLI - GUROBI
			# --------------------------
			# transforma dicionario em lista
			sintetica_controle = tarefas_sinteticas.copy()

			tarefas = []
			for i in tarefas_local:
				tarefas.append(tarefas_local[i])
			
			# BIN PACKING PLI
			alocadas_agora = []

			# reorganiza tarefas_d
			tarefas_sinteticas.clear()
			cont = 0
			for i in range(len(tarefas)):
				if tarefas[i] > valor_bin:
					# print("Removendo:",i,"->",tarefas[i])
					tarefas_local.pop(i)
					# tarefas_sinteticas.pop(i)
				else:
					tarefas_sinteticas[cont] = sintetica_controle[i]
					# print("Atualizando:",i)
					cont += 1

			# cont = 0
			# for i in teste:
			# 	tarefas_sinteticas[cont] = i
			# 	cont += 1
			if len(tarefas_local) == 0:
				break

			tarefas = []
			for i in tarefas_local:
				tarefas.append(tarefas_local[i])

			tarefas_local = {}
			for i in range(len(tarefas)):
				tarefas_local[i] = tarefas[i]

			# print("Sintetica ID >",tarefas_sinteticas)
			# print("Local PESO >",tarefas_local)
			# print("Tarefas >",tarefas)
			
			bin_for_item = firstfit.heuristica_FFD(valor_bin, tarefas)
			controle_local = firstfit.get_items_bpp(tarefas, bin_for_item)
			
			# print("Controle local:",controle_local)
			id_nuvem = -1
			id_nuvem = firstfit.get_best_allocation(valor_bin, tarefas, controle_local)

			alocadas_local = []
			for i in controle_local[id_nuvem]:
				# print(i)
				if i in tarefas_local:
					# print(i)
					alocadas_local.append(i)

			# transformar para ID em tasks
			for i in alocadas_local:
				alocadas_agora.append(tarefas_sinteticas[i])

			print("Tarefas candidatas:",alocadas_agora)

			# transforma alocadas_local em alocadas_agora
			
			'''
			# BIN PACKING COM NEXT FIT
			
			alocadas_agora = []
			for i in tasks:
				size = i[1]
				if size <= valor_bin:
					alocadas_agora.append(i[0])
					valor_bin = valor_bin - size
			
			print("Tarefas candidatas:",alocadas_agora)
			'''

			# nenhuma
			if len(alocadas_agora) == 0:
				print("MIOU")
				break

			# -----------------------
			# VERIFICA DEADLINE
			# -----------------------
			print("VERIFICANDO DEADLINE")
			controle_local = []
			for now in alocadas_agora:
				# print(" - tarefa:",now)
				deadline = deadline_temp[now]
				peso = peso_temp[now]
				pontuacao = 0
				for tempo_k in range(deadline):
					# print("Tempo:",tempo)
					# print(">>>",cluster_manager.recursos[maximo][tempo])
					vc_time = cluster_manager.controle_recursos[maximo][tempo_k]['vc']
					# print("vc_time",vc_time)
					if vc_time >= peso:
						pontuacao += 1
				if pontuacao < deadline:
					controle_local.append(now)

			if len(controle_local) > 0:
				for vec in controle_local:
					# remove das alocadas
					if vec in alocadas_agora:
						# print(" * Removeu tarefa:",vec)
						alocadas_agora.remove(vec)

			# -----------------------
			# VERIFICA PROCESSAMENTO
			# -----------------------
			print("VERIFICANDO PROCESSAMENTO")
			# CONSERTAR PARA DIVIDIR ENTRE VEICULOS
			# print("cluster_manager.recursos[maximo][0]:",cluster_manager.recursos[maximo][0])
			# print("len(alocadas_agora)",len(alocadas_agora))
			# frequencia_vc = round(cluster_manager.recursos[maximo][0] / len(alocadas_agora), 2)
			if len(alocadas_agora) > 0:
				frequencia_vc = cluster_manager.controle_recursos[maximo][tempo][local_vc]
				# print("FREQ:",frequencia_vc)
				
				tempo_processamento_tarefas = {}

				controle_local_2 = []
				for now in alocadas_agora:
					# print("Tarefa:",now)
					tempo_processamento = 0
					# print("Ciclos:",ciclos_temp[now])
					tempo_processamento = round(ciclos_temp[now] / frequencia_vc, 2)
					# print(" * proc:",tempo_processamento)
					if tempo_processamento > deadline_temp[now]:
						controle_local_2.append(now)
					else:
						tempo_processamento_tarefas[now] = tempo_processamento

				if len(controle_local_2) > 0:
					for vec in controle_local_2:
						# remove das alocadas
						if vec in alocadas_agora:
							# print("> Removeu tarefa:",vec)
							alocadas_agora.remove(vec)

				# -----------------------
				# ESCALONA EM DEFINITIVO
				# -----------------------
				escalonamento_controle = {}
				for tarefa_i in alocadas_agora:
					escalonamento_controle[tarefa_i] = {}
					escalonamento_controle[tarefa_i]['processamento'] = tempo_processamento_tarefas[tarefa_i]
					escalonamento_controle[tarefa_i]['local'] = 'vc'
					nuvens[maximo] = tarefa_i
					for tarefa_j in tasks:
						if tarefa_i == tarefa_j[0]:
							tasks.remove(tarefa_j)
						if tarefa_j[1] > controle_valor_bin:
							tasks.remove(tarefa_j)

				if len(escalonamento_controle) > 0:
					escalonamento[maximo] = escalonamento_controle
					# print("Esc:",escalonamento)

				for i in alocadas_local:
					if i in tarefas_local:
						# print("Removendo",i)
						tarefas_local.pop(i)
						tarefas_sinteticas.pop(i)
				
				cont = 0
				teste = {}
				for i in tarefas_sinteticas:
					teste[cont] = tarefas_sinteticas[i]
					cont += 1
				
				tarefas_sinteticas.clear()
				tarefas_sinteticas = teste
				
				tarefas = []
				for i in tarefas_local:
					tarefas.append(tarefas_local[i])
				
				tarefas_local.clear()
				for i in range(len(tarefas)):
					tarefas_local[i] = tarefas[i]
				
				if len(tarefas_local) == 0:
					print("alocou tudo!")
					break
				
				# # reorganiza tarefas_d
				# if len(tarefas_local) == 0:
				# 	print("alocou tudo!")
				# 	break
				# else:
				# 	tarefas_local = {}
				# 	for i in range(len(tarefas)):
				# 		tarefas_local[i] = tarefas[i]

				# tarefas_sinteticas = {}
				# cont = 0
				# for i in tasks:
				# 	tarefas_sinteticas[cont] = i[0]
				# 	cont += 1

		else:
			break
	
	for i in escalonamento:
		for j in escalonamento[i]:
			for k in tasks_rsu:
				if j == k[0]:
					tasks_rsu.remove(k)
	
	# print("Atualizado:",tasks_rsu)

	# atualizando tarefas
	tarefas_local = {}
	tarefas_sinteticas = {}
	cont = 0
	for i in tasks_rsu:
		tarefas_local[cont] = i[1]
		tarefas_sinteticas[cont] = i[0]
		cont += 1
	
	tarefas = []
	for i in tarefas_local:
		tarefas.append(tarefas_local[i])

	# print("Tarefas LOCAL RSUS",tarefas_local)
	# print("Tarefas SINTETICA RSUS",tarefas_sinteticas)

	# ALOCA NAS RSUS
	while len(tasks_rsu) > 0:
		if len(recursos_rsus) > 0:

			# print("Restaram:",tasks)

			# --------------------------
			# BIN-PACKING NEXTFIT
			# --------------------------
			# maximo = max_value(vclouds)
			tempo = 0
			maximo = max_value_per_time(recursos_rsus, tempo)
			valor_bin = recursos_rsus[maximo][tempo]
			recursos_rsus.pop(maximo)
		
			controle_valor_bin = 0
			controle_valor_bin = valor_bin

			print("\nNuvem atual:",maximo)
			print("Valor:",valor_bin)

			# maior nuvem menor que a menor tarefa
			min_local = min_value(tasks)
			if valor_bin < min_local:
				print("SEM ESPAÇO NAS RSUS!")
				break

			# --------------------------
			# BIN-PACKING PLI - GUROBI
			# --------------------------
			# transforma dicionario em lista
			sintetica_controle = tarefas_sinteticas.copy()

			tarefas = []
			for i in tarefas_local:
				tarefas.append(tarefas_local[i])
			
			# BIN PACKING PLI
			alocadas_agora = []

			# reorganiza tarefas_d
			tarefas_sinteticas.clear()
			cont = 0
			for i in range(len(tarefas)):
				if tarefas[i] > valor_bin:
					print("Removendo:",i,"->",tarefas[i])
					tarefas_local.pop(i)
					# tarefas_sinteticas.pop(i)
				else:
					tarefas_sinteticas[cont] = sintetica_controle[i]
					print("Atualizando:",i)
					cont += 1

			if len(tarefas_local) == 0:
				break
			# cont = 0
			# for i in teste:
			# 	tarefas_sinteticas[cont] = i
			# 	cont += 1

			tarefas = []
			for i in tarefas_local:
				tarefas.append(tarefas_local[i])

			tarefas_local = {}
			for i in range(len(tarefas)):
				tarefas_local[i] = tarefas[i]

			# print("Sintetica ID >",tarefas_sinteticas)
			# print("Local PESO >",tarefas_local)
			print("Tarefas >",tarefas)

			bin_for_item = firstfit.heuristica_FFD(valor_bin, tarefas)
			controle_local = firstfit.get_items_bpp(tarefas, bin_for_item)
			
			# print("Controle local:",controle_local)

			id_nuvem = firstfit.get_best_allocation(valor_bin, tarefas, controle_local)

			# print("TESTEEEEEEEEEE:",controle_local[id_nuvem])

			# seleciona melhor alocacao
			# print("nuvem:",id_nuvem)

			# print("locais:",tarefas_local)

			alocadas_local = []
			for i in controle_local[id_nuvem]:
				# print(i)
				if i in tarefas_local:
					# print(i)
					alocadas_local.append(i)

			# transformar para ID em tasks
			for i in alocadas_local:
				alocadas_agora.append(tarefas_sinteticas[i])

			print("Tarefas candidatas:",alocadas_agora)
			
			'''
			# BIN PACKING COM NEXT FIT
			alocadas_agora = []
			for i in tasks:
				size = i[1]
				if size <= valor_bin:
					alocadas_agora.append(i[0])
					valor_bin = valor_bin - size

			print("Tarefas candidatas:",alocadas_agora)
			'''

			# nenhuma
			if len(alocadas_agora) == 0:
				break

			# -----------------------
			# VERIFICA DEADLINE
			# -----------------------
			print("VERIFICANDO DEADLINE")
			controle_local = []
			for now in alocadas_agora:
				# print(" - tarefa:",now)
				deadline = deadline_temp[now]
				peso = peso_temp[now]
				pontuacao = 0
				for tempo_k in range(deadline):
					# print("Tempo:",tempo)
					# print(">>>",cluster_manager.recursos[maximo][tempo])
					vc_time = cluster_manager.controle_recursos[maximo][tempo_k]['vc']
					# print("vc_time",vc_time)
					if vc_time >= peso:
						pontuacao += 1
				if pontuacao < deadline:
					controle_local.append(now)

			if len(controle_local) > 0:
				for vec in controle_local:
					# remove das alocadas
					if vec in alocadas_agora:
						# print(" * Removeu tarefa:",vec)
						alocadas_agora.remove(vec)

			# -----------------------
			# VERIFICA PROCESSAMENTO
			# -----------------------
			print("VERIFICANDO PROCESSAMENTO")
			# CONSERTAR PARA DIVIDIR ENTRE VEICULOS
			# print("cluster_manager.recursos[maximo][0]:",cluster_manager.recursos[maximo][0])
			# print("len(alocadas_agora)",len(alocadas_agora))
			# frequencia_vc = round(cluster_manager.recursos[maximo][0] / len(alocadas_agora), 2)
			if len(alocadas_agora) > 0:
				frequencia_vc = cluster_manager.controle_recursos[maximo][tempo][local_rsu]
				# print("FREQ:",frequencia_vc)
				
				tempo_processamento_tarefas = {}

				controle_local_2 = []
				for now in alocadas_agora:
					# print("Tarefa:",now)
					tempo_processamento = 0
					# print("Ciclos:",ciclos_temp[now])
					tempo_processamento = round(ciclos_temp[now] / frequencia_vc, 2)
					# print(" * proc:",tempo_processamento)
					if tempo_processamento > deadline_temp[now]:
						controle_local_2.append(now)
					else:
						tempo_processamento_tarefas[now] = tempo_processamento

				if len(controle_local_2) > 0:
					for vec in controle_local_2:
						# remove das alocadas
						if vec in alocadas_agora:
							# print("> Removeu tarefa:",vec)
							alocadas_agora.remove(vec)

				# -----------------------
				# ESCALONA EM DEFINITIVO
				# -----------------------
				escalonamento_controle = {}
				for tarefa_i in alocadas_agora:
					escalonamento_controle[tarefa_i] = {}
					escalonamento_controle[tarefa_i]['processamento'] = tempo_processamento_tarefas[tarefa_i]
					escalonamento_controle[tarefa_i]['local'] = 'rsu'
					for tarefa_j in tasks_rsu:
						if tarefa_i == tarefa_j[0]:
							tasks_rsu.remove(tarefa_j)
						if tarefa_j[1] > controle_valor_bin:
							tasks_rsu.remove(tarefa_j)
				
				if len(escalonamento_controle) > 0:
					if maximo in nuvens:
						escalonamento[maximo].update(escalonamento_controle)
					else:
						escalonamento[maximo] = escalonamento_controle

				for i in alocadas_local:
					if i in tarefas_local:
						# print("Removendo",i)
						tarefas_local.pop(i)
						tarefas_sinteticas.pop(i)
				
				cont = 0
				teste = {}
				for i in tarefas_sinteticas:
					teste[cont] = tarefas_sinteticas[i]
					cont += 1
				
				tarefas_sinteticas.clear()
				tarefas_sinteticas = teste
				
				tarefas = []
				for i in tarefas_local:
					tarefas.append(tarefas_local[i])
				
				tarefas_local.clear()
				for i in range(len(tarefas)):
					tarefas_local[i] = tarefas[i]
				
				if len(tarefas_local) == 0:
					print("alocou tudo RSU!")
					break

		else:
			break

	return escalonamento

def MY_SYSTEM(vclouds, tasks):

	tasks = tasks.copy()
	vclouds = vclouds.copy()

	# para controle interno do algoritmo
	lista_local_sintetica = {}
	cont = 0
	for i in tasks:
		lista_local_sintetica[i[0]] = cont
		cont += 1

	# CRIA DICIONARIO DE VCS
	recursos_vcs = {}
	for i in cluster_manager.controle_recursos:
		time = {}
		for j in cluster_manager.controle_recursos[i]:
			time[j] = cluster_manager.controle_recursos[i][j]['vc']
		recursos_vcs[i] = time
	
	# CRIA DICIONARIO DE RSUS
	recursos_rsus = {}
	for i in cluster_manager.controle_recursos:
		time = {}
		for j in cluster_manager.controle_recursos[i]:
			time[j] = cluster_manager.controle_recursos[i][j]['rsu']
		recursos_rsus[i] = time

	ciclos_temp = {}
	for i in tasks:
		ciclos_temp[i[0]] = i[3]

	# ALOCA NAS VCS
	nuvens = {}
	while len(tasks) > 0:

		if len(recursos_vcs) > 0:

			tempo = 0
			maximo = max_value_per_time(recursos_vcs, tempo)
			if maximo == -1:
				break
			maior_vc = recursos_vcs[maximo][tempo]

			# for DP solution
			wt = []
			va = []
			for i in tasks:
				wt.append(i[1])
				va.append(i[2])

			# maior nuvem menor que a menor tarefa
			if maior_vc < min(wt):
				print("SEM RECURSOS NAS VCS!")
				break

			alocadas_agora = dp_solution_mors(maior_vc, wt, va)

			print("Tarefas candidatas:",alocadas_agora)

			recursos_vcs.pop(maximo)

			temp_list = []
			for i in alocadas_agora:
				# print(i[0])
				for j in lista_local_sintetica:
					# print(lista_local_sintetica[j])
					if i[0] == lista_local_sintetica[j]:
						# print("Alocada:",i,j)
						temp_list.append(j)

			print("temp:",temp_list)

			# -----------------------
			# VERIFICA PROCESSAMENTO
			# -----------------------
			if len(alocadas_agora) > 0:
				frequencia_total = cluster_manager.controle_recursos[maximo][tempo][local_vc]
				frequencia_vc = frequencia_total / len(alocadas_agora)
				tempo_processamento_tarefas = {}
				controle_local_2 = []
				for now in temp_list:
					# print("Tarefa:",now)
					# print("Ciclo:",ciclos_temp[now])
					tempo_processamento = 0
					tempo_processamento = round(ciclos_temp[now] / frequencia_vc, 2)
					tempo_processamento_tarefas[now] = tempo_processamento
				
				# -----------------------
				# ESCALONA EM DEFINITIVO
				# -----------------------
				escalonamento_controle = {}
				for tarefa_i in temp_list:
					escalonamento_controle[tarefa_i] = {}
					escalonamento_controle[tarefa_i]['processamento'] = tempo_processamento_tarefas[tarefa_i]
					escalonamento_controle[tarefa_i]['local'] = 'vc'
					nuvens[maximo] = tarefa_i
					for tarefa_j in tasks:
						if tarefa_i == tarefa_j[0]:
							tasks.remove(tarefa_j)
				
				for i in temp_list:
					if i in lista_local_sintetica:
						lista_local_sintetica.pop(i)

				# reorganiza lista de controle
				cont = 0
				for i in tasks:
					lista_local_sintetica[i[0]] = cont
					cont += 1
				
				if len(escalonamento_controle) > 0:
					escalonamento[maximo] = escalonamento_controle
			
		else:
			break
	
	# para controle interno do algoritmo
	lista_local_sintetica = {}
	cont = 0
	for i in tasks:
		lista_local_sintetica[i[0]] = cont
		cont += 1

	# ALOCA NAS RSUS
	while len(tasks) > 0:

		if len(recursos_rsus) > 0:

			tempo = 0
			maximo = max_value_per_time(recursos_rsus, tempo)
			if maximo == -1:
				break
			maior_vc = recursos_rsus[maximo][tempo]

			# for DP solution
			wt = []
			va = []
			for i in tasks:
				wt.append(i[1])
				va.append(i[2])

			# maior nuvem menor que a menor tarefa
			if maior_vc < min(wt):
				print("SEM RECURSOS NAS RSUS!")
				break

			alocadas_agora = dp_solution_mors(maior_vc, wt, va)

			recursos_rsus.pop(maximo)

			temp_list = []
			for i in alocadas_agora:
				# print(i[0])
				for j in lista_local_sintetica:
					# print(lista_local_sintetica[j])
					if i[0] == lista_local_sintetica[j]:
						# print("Alocada:",i,j)
						temp_list.append(j)

			# -----------------------
			# VERIFICA PROCESSAMENTO
			# -----------------------
			if len(alocadas_agora) > 0:
				frequencia_total = cluster_manager.controle_recursos[maximo][tempo][local_rsu]
				frequencia_vc = frequencia_total / len(alocadas_agora)
				tempo_processamento_tarefas = {}
				controle_local_2 = []
				for now in temp_list:
					tempo_processamento = 0
					tempo_processamento = round(ciclos_temp[now] / frequencia_vc, 2)
					tempo_processamento_tarefas[now] = tempo_processamento
				
				# -----------------------
				# ESCALONA EM DEFINITIVO
				# -----------------------
				escalonamento_controle = {}
				for tarefa_i in temp_list:
					escalonamento_controle[tarefa_i] = {}
					escalonamento_controle[tarefa_i]['processamento'] = tempo_processamento_tarefas[tarefa_i]
					escalonamento_controle[tarefa_i]['local'] = 'rsu'
					for tarefa_j in tasks:
						if tarefa_i == tarefa_j[0]:
							tasks.remove(tarefa_j)
				
				for i in temp_list:
					if i in lista_local_sintetica:
						lista_local_sintetica.pop(i)

				# reorganiza lista de controle
				cont = 0
				for i in tasks:
					lista_local_sintetica[i[0]] = cont
					cont += 1
				
				if len(escalonamento_controle) > 0:
					if maximo in nuvens:
						escalonamento[maximo].update(escalonamento_controle)
					else:
						escalonamento[maximo] = escalonamento_controle
			
		else:
			break

	return escalonamento

def FIFO(vclouds, tasks):

	tasks = tasks.copy()
	vclouds = vclouds.copy()

	# CRIA DICIONARIO DE VCS
	recursos_vcs = {}
	for i in cluster_manager.controle_recursos:
		time = {}
		for j in cluster_manager.controle_recursos[i]:
			time[j] = cluster_manager.controle_recursos[i][j]['vc']
		recursos_vcs[i] = time
	
	# CRIA DICIONARIO DE RSUS
	recursos_rsus = {}
	for i in cluster_manager.controle_recursos:
		time = {}
		for j in cluster_manager.controle_recursos[i]:
			time[j] = cluster_manager.controle_recursos[i][j]['rsu']
		recursos_rsus[i] = time

	# tasks = sorted(tasks, reverse=True, key=weight)

	ciclos_temp = {}
	for i in tasks:
		ciclos_temp[i[0]] = i[3]

	# ALOCA NAS VCS
	nuvens = {}
	while len(tasks) > 0:

		# alocadas_agora = []
		if len(recursos_vcs) > 0:
			
			tempo = 0
			maximo = max_value_per_time(recursos_vcs, tempo)
			if maximo == -1:
				break
			maior_vc = recursos_vcs[maximo][tempo]

			controle_valor_vc = 0
			controle_valor_vc = maior_vc

			# maior nuvem menor que a menor tarefa
			min_local = min_value(tasks)
			if maior_vc < min_local:
				print("SEM RECURSOS NAS VCS!")
				break
			
			alocadas_agora = []
			# codigo fifo
			for i in tasks:
				size = i[1]
				if size <= maior_vc:
					alocadas_agora.append(i[0])
					maior_vc = maior_vc - size
					# print("Tarefa %d " % i[0])
					# print(" * alocada na nuvem %d " % maior_vc_indice)

			print("Tarefas candidatas:",alocadas_agora)
			recursos_vcs.pop(maximo)

			# -----------------------
			# VERIFICA PROCESSAMENTO
			# -----------------------
			frequencia_vc = cluster_manager.controle_recursos[maximo][tempo][local_vc]
			tempo_processamento_tarefas = {}
			controle_local_2 = []
			for now in alocadas_agora:
				tempo_processamento = 0
				tempo_processamento = round(ciclos_temp[now] / frequencia_vc, 2)
				tempo_processamento_tarefas[now] = tempo_processamento
			
			# -----------------------
			# ESCALONA EM DEFINITIVO
			# -----------------------
			escalonamento_controle = {}
			for tarefa_i in alocadas_agora:
				escalonamento_controle[tarefa_i] = {}
				escalonamento_controle[tarefa_i]['processamento'] = tempo_processamento_tarefas[tarefa_i]
				escalonamento_controle[tarefa_i]['local'] = 'vc'
				nuvens[maximo] = tarefa_i
				for tarefa_j in tasks:
					if tarefa_i == tarefa_j[0]:
						tasks.remove(tarefa_j)
					if tarefa_j[1] > controle_valor_vc:
						tasks.remove(tarefa_j)

			if len(escalonamento_controle) > 0:
				escalonamento[maximo] = escalonamento_controle

		else:
			break

	# ALOCA NAS RSUS	
	while len(tasks) > 0:

		# alocadas_agora = []
		if len(recursos_rsus) > 0:
			
			tempo = 0
			maximo = max_value_per_time(recursos_rsus, tempo)
			if maximo == -1:
				break
			maior_vc = recursos_rsus[maximo][tempo]

			controle_valor_vc = 0
			controle_valor_vc = maior_vc

			# maior nuvem menor que a menor tarefa
			min_local = min_value(tasks)
			if maior_vc < min_local:
				print("SEM RECURSOS NAS RSUS!")
				break
			
			alocadas_agora = []
			# codigo fifo
			for i in tasks:
				size = i[1]
				if size <= maior_vc:
					alocadas_agora.append(i[0])
					maior_vc = maior_vc - size
					# print("Tarefa %d " % i[0])
					# print(" * alocada na nuvem %d " % maior_vc_indice)
		
			recursos_rsus.pop(maximo)

			# -----------------------
			# VERIFICA PROCESSAMENTO
			# -----------------------
			frequencia_vc = cluster_manager.controle_recursos[maximo][tempo][local_rsu]
			tempo_processamento_tarefas = {}
			controle_local_2 = []
			for now in alocadas_agora:
				tempo_processamento = 0
				tempo_processamento = round(ciclos_temp[now] / frequencia_vc, 2)
				tempo_processamento_tarefas[now] = tempo_processamento
			
			# -----------------------
			# ESCALONA EM DEFINITIVO
			# -----------------------
			escalonamento_controle = {}
			for tarefa_i in alocadas_agora:
				escalonamento_controle[tarefa_i] = {}
				escalonamento_controle[tarefa_i]['processamento'] = tempo_processamento_tarefas[tarefa_i]
				escalonamento_controle[tarefa_i]['local'] = 'rsu'
				for tarefa_j in tasks:
					if tarefa_i == tarefa_j[0]:
						tasks.remove(tarefa_j)
					if tarefa_j[1] > controle_valor_vc:
						tasks.remove(tarefa_j)

			if len(escalonamento_controle) > 0:
				if maximo in nuvens:
					escalonamento[maximo].update(escalonamento_controle)
				else:
					escalonamento[maximo] = escalonamento_controle

		else:
			break
	
	return escalonamento

def UNC(vclouds, tasks):

	print("UNC!")
	tasks = tasks.copy()
	vclouds = vclouds.copy()

	# CRIA DICIONARIO DE VCS
	recursos_vcs = {}
	for i in cluster_manager.controle_recursos:
		time = {}
		for j in cluster_manager.controle_recursos[i]:
			time[j] = cluster_manager.controle_recursos[i][j]['vc']
		recursos_vcs[i] = time
	
	# CRIA DICIONARIO DE RSUS
	recursos_rsus = {}
	for i in cluster_manager.controle_recursos:
		time = {}
		for j in cluster_manager.controle_recursos[i]:
			time[j] = cluster_manager.controle_recursos[i][j]['rsu']
		recursos_rsus[i] = time

	ciclos_temp = {}
	for i in tasks:
		ciclos_temp[i[0]] = i[3]

	tasks = sorted(tasks, reverse=False, key=weight)

	# ALOCA NAS VCS
	nuvens = {}
	while len(tasks) > 0:

		# alocadas_agora = []
		if len(recursos_vcs) > 0:
			
			tempo = 0
			maximo = max_value_per_time(recursos_vcs, tempo)
			if maximo == -1:
				break
			maior_vc = recursos_vcs[maximo][tempo]

			controle_valor_vc = 0
			controle_valor_vc = maior_vc

			# maior nuvem menor que a menor tarefa
			min_local = min_value(tasks)
			if maior_vc < min_local:
				print("SEM RECURSOS NAS VCS!")
				break
			
			alocadas_agora = []

			# codigo fifo
			for i in tasks:
				size = i[1]
				if size <= maior_vc:
					alocadas_agora.append(i[0])
					maior_vc = maior_vc - size
					# print("Tarefa %d " % i[0])
					# print(" * alocada na nuvem %d " % maior_vc_indice)
		
			recursos_vcs.pop(maximo)

			# -----------------------
			# VERIFICA PROCESSAMENTO
			# -----------------------
			if len(alocadas_agora) > 0:
				frequencia_total = cluster_manager.controle_recursos[maximo][tempo][local_vc]
				frequencia_vc = frequencia_total / len(alocadas_agora)
				tempo_processamento_tarefas = {}
				controle_local_2 = []
				for now in alocadas_agora:
					tempo_processamento = 0
					tempo_processamento = round(ciclos_temp[now] / frequencia_vc, 2)
					tempo_processamento_tarefas[now] = tempo_processamento
				
				# -----------------------
				# ESCALONA EM DEFINITIVO
				# -----------------------
				escalonamento_controle = {}
				for tarefa_i in alocadas_agora:
					escalonamento_controle[tarefa_i] = {}
					escalonamento_controle[tarefa_i]['processamento'] = tempo_processamento_tarefas[tarefa_i]
					escalonamento_controle[tarefa_i]['local'] = 'vc'
					nuvens[maximo] = tarefa_i
					for tarefa_j in tasks:
						if tarefa_i == tarefa_j[0]:
							tasks.remove(tarefa_j)
						if tarefa_j[1] > controle_valor_vc:
							tasks.remove(tarefa_j)

				if len(escalonamento_controle) > 0:
					escalonamento[maximo] = escalonamento_controle

		else:
			break

	# ALOCA NAS RSUS	
	while len(tasks) > 0:

		# alocadas_agora = []
		if len(recursos_rsus) > 0:
			
			tempo = 0
			maximo = max_value_per_time(recursos_rsus, tempo)
			if maximo == -1:
				break
			maior_vc = recursos_rsus[maximo][tempo]

			controle_valor_vc = 0
			controle_valor_vc = maior_vc

			# maior nuvem menor que a menor tarefa
			min_local = min_value(tasks)
			if maior_vc < min_local:
				print("SEM RECURSOS NAS RSUS!")
				break
			
			alocadas_agora = []

			# codigo fifo
			for i in tasks:
				size = i[1]
				if size <= maior_vc:
					alocadas_agora.append(i[0])
					maior_vc = maior_vc - size
					# print("Tarefa %d " % i[0])
					# print(" * alocada na nuvem %d " % maior_vc_indice)
		
			recursos_rsus.pop(maximo)

			# -----------------------
			# VERIFICA PROCESSAMENTO
			# -----------------------
			if len(alocadas_agora) > 0:
				frequencia_total = cluster_manager.controle_recursos[maximo][tempo][local_rsu]
				frequencia_vc = frequencia_total / len(alocadas_agora)
				tempo_processamento_tarefas = {}
				controle_local_2 = []
				for now in alocadas_agora:
					tempo_processamento = 0
					tempo_processamento = round(ciclos_temp[now] / frequencia_vc, 2)
					tempo_processamento_tarefas[now] = tempo_processamento
				
				# -----------------------
				# ESCALONA EM DEFINITIVO
				# -----------------------
				escalonamento_controle = {}
				for tarefa_i in alocadas_agora:
					escalonamento_controle[tarefa_i] = {}
					escalonamento_controle[tarefa_i]['processamento'] = tempo_processamento_tarefas[tarefa_i]
					escalonamento_controle[tarefa_i]['local'] = 'rsu'
					for tarefa_j in tasks:
						if tarefa_i == tarefa_j[0]:
							tasks.remove(tarefa_j)
						if tarefa_j[1] > controle_valor_vc:
							tasks.remove(tarefa_j)

				if len(escalonamento_controle) > 0:
					if maximo in nuvens:
						escalonamento[maximo].update(escalonamento_controle)
					else:
						escalonamento[maximo] = escalonamento_controle

		else:
			break

	return escalonamento

def ahp_allocation(vclouds, tasks):
	
	tasks = tasks.copy()
	vclouds = vclouds.copy()

	# CRIA DICIONARIO DE VCS
	recursos_vcs = {}
	for i in cluster_manager.controle_recursos:
		time = {}
		for j in cluster_manager.controle_recursos[i]:
			time[j] = cluster_manager.controle_recursos[i][j]['vc']
		recursos_vcs[i] = time
	
	# CRIA DICIONARIO DE RSUS
	recursos_rsus = {}
	for i in cluster_manager.controle_recursos:
		time = {}
		for j in cluster_manager.controle_recursos[i]:
			time[j] = cluster_manager.controle_recursos[i][j]['rsu']
		recursos_rsus[i] = time

	# tasks = sorted(tasks, reverse=False, key=weight)

	# print("Ordenadas:",tasks)

	ciclos_temp = {}
	tarefas = {}
	tasks_padrao = {}
	for i in tasks:
		# peso, valor, ciclos, deadline
		# tarefas[i[0]] = [i[1], i[2], i[3], i[4]]
		tarefas[i[0]] = [i[4], i[1], i[3], i[2]]
		tasks_padrao[i[0]] = [i[1], i[2], i[3], i[4]]
		ciclos_temp[i[0]] = i[3]

	# ALOCA NAS VCS
	nuvens = {}
	while len(tarefas) > 0:

		if len(recursos_vcs) > 0:

			# print("Nuvens:",recursos_vcs)
			
			tempo = 0
			maximo = max_value_per_time(recursos_vcs, tempo)
			if maximo == -1:
				break
			maior_vc = recursos_vcs[maximo][tempo]

			controle_valor_vc = 0
			controle_valor_vc = maior_vc

			# maior nuvem menor que a menor tarefa
			min_local = min_value(tasks)
			if maior_vc < min_local:
				print("SEM RECURSOS NAS VCS!")
				break
			
			alocadas_agora = []

			# print("Nuvem atual:",maximo)

			while maior_vc > 0:

				allocated = ahp.Politica(tarefas)
				# print("Task selecionada:",allocated[0])

				# print("Peso:",tasks_padrao[allocated[0]][0])

				if tasks_padrao[allocated[0]][0] <= maior_vc:
					maior_vc = maior_vc - tasks_padrao[allocated[0]][0]
					alocadas_agora.append(allocated[0])
					tarefas.pop(allocated[0])
					
					if len(tarefas) == 0:
						break
				else:
					tarefas.pop(allocated[0])
					break
			
			# print("Tarefas candidatas VC:",alocadas_agora)
			
			recursos_vcs.pop(maximo)

			# -----------------------
			# VERIFICA PROCESSAMENTO
			# -----------------------
			if len(alocadas_agora) > 0:
				frequencia_total = cluster_manager.controle_recursos[maximo][tempo][local_vc]
				frequencia_vc = frequencia_total / len(alocadas_agora)
				tempo_processamento_tarefas = {}
				controle_local_2 = []
				for now in alocadas_agora:
					tempo_processamento = 0
					tempo_processamento = round(ciclos_temp[now] / frequencia_vc, 2)
					tempo_processamento_tarefas[now] = tempo_processamento
				
				# -----------------------
				# ESCALONA EM DEFINITIVO
				# -----------------------
				escalonamento_controle = {}
				for tarefa_i in alocadas_agora:
					escalonamento_controle[tarefa_i] = {}
					escalonamento_controle[tarefa_i]['processamento'] = tempo_processamento_tarefas[tarefa_i]
					escalonamento_controle[tarefa_i]['local'] = 'vc'
					nuvens[maximo] = tarefa_i
					for tarefa_j in tasks:
						if tarefa_i == tarefa_j[0]:
							tasks.remove(tarefa_j)
						if tarefa_j[1] > controle_valor_vc:
							tasks.remove(tarefa_j)

				if len(escalonamento_controle) > 0:
					escalonamento[maximo] = escalonamento_controle

		else:
			break

	# ALOCA NAS RSUS	
	while len(tarefas) > 0:
		
		if len(recursos_rsus) > 0:

			# print("Nuvens:",recursos_vcs)
			
			tempo = 0
			maximo = max_value_per_time(recursos_rsus, tempo)
			if maximo == -1:
				break
			maior_vc = recursos_rsus[maximo][tempo]

			controle_valor_vc = 0
			controle_valor_vc = maior_vc

			# maior nuvem menor que a menor tarefa
			min_local = min_value(tasks)
			if maior_vc < min_local:
				print("SEM RECURSOS NAS RSUS!")
				break
			
			alocadas_agora = []

			print("Nuvem atual:",maximo)
			print("Valor:",maior_vc)

			while maior_vc > 0:

				allocated = ahp.Politica(tarefas)
				print("Task selecionada:",allocated[0])

				print("Peso:",tasks_padrao[allocated[0]][0])

				if tasks_padrao[allocated[0]][0] <= maior_vc:
					maior_vc = maior_vc - tasks_padrao[allocated[0]][0]
					alocadas_agora.append(allocated[0])
					tarefas.pop(allocated[0])

					if len(tarefas) == 0:
						break

				else:
					tarefas.pop(allocated[0])
					break
			
			print("Tarefas candidatas RSU:",alocadas_agora)

			recursos_rsus.pop(maximo)

			# -----------------------
			# VERIFICA PROCESSAMENTO
			# -----------------------
			if len(alocadas_agora) > 0:
				frequencia_total = cluster_manager.controle_recursos[maximo][tempo][local_rsu]
				frequencia_vc = frequencia_total / len(alocadas_agora)
				tempo_processamento_tarefas = {}
				controle_local_2 = []
				for now in alocadas_agora:
					tempo_processamento = 0
					tempo_processamento = round(ciclos_temp[now] / frequencia_vc, 2)
					tempo_processamento_tarefas[now] = tempo_processamento
				
				# -----------------------
				# ESCALONA EM DEFINITIVO
				# -----------------------
				escalonamento_controle = {}
				for tarefa_i in alocadas_agora:
					escalonamento_controle[tarefa_i] = {}
					escalonamento_controle[tarefa_i]['processamento'] = tempo_processamento_tarefas[tarefa_i]
					escalonamento_controle[tarefa_i]['local'] = 'rsu'
					for tarefa_j in tasks:
						if tarefa_i == tarefa_j[0]:
							tasks.remove(tarefa_j)
						if tarefa_j[1] > controle_valor_vc:
							tasks.remove(tarefa_j)
				
				if len(escalonamento_controle) > 0:
					if maximo in nuvens:
						escalonamento[maximo].update(escalonamento_controle)
					else:
						escalonamento[maximo] = escalonamento_controle
		else:
			break
	
	return escalonamento

def PSO(vclouds, tasks):
	
	tasks = tasks.copy()
	vclouds = vclouds.copy()
	
	# CRIA DICIONARIO DE VCS
	recursos_vcs = {}
	for i in cluster_manager.controle_recursos:
		time = {}
		for j in cluster_manager.controle_recursos[i]:
			time[j] = cluster_manager.controle_recursos[i][j]['vc']
		recursos_vcs[i] = time
	
	# CRIA DICIONARIO DE RSUS
	recursos_rsus = {}
	for i in cluster_manager.controle_recursos:
		time = {}
		for j in cluster_manager.controle_recursos[i]:
			time[j] = cluster_manager.controle_recursos[i][j]['rsu']
		recursos_rsus[i] = time

	# tasks = sorted(tasks, reverse=True, key=weight)
	
	ciclos_temp = {}
	for i in tasks:
		ciclos_temp[i[0]] = i[3]

	tarefas = tasks.copy()

	# ALOCA NAS VCS
	nuvens = {}
	while len(tasks) > 0:

		if len(recursos_vcs) > 0:
			
			tempo = 0
			maximo = max_value_per_time(recursos_vcs, tempo)
			if maximo == -1:
				break
			maior_vc = recursos_vcs[maximo][tempo]

			controle_valor_vc = 0
			controle_valor_vc = maior_vc

			# maior nuvem menor que a menor tarefa
			min_local = min_value(tasks)
			if maior_vc < min_local:
				print("SEM RECURSOS NAS VCS!")
				break
			
			alocadas_agora = []

			# print("\nNuvem atual:",maximo)

			while maior_vc > 0:

				allocated = GWO.gwo_solution(maior_vc, tarefas)
				if type(allocated) is int:

					if tarefas[allocated][1] <= maior_vc:
						maior_vc = maior_vc - tarefas[allocated][1]
						alocadas_agora.append(tarefas[allocated][0])
						tarefas.pop(allocated)

						if len(tarefas) == 0:
							break
					else:
						break
				else:
					break
						
			# print("Tarefas candidatas:",alocadas_agora)
			# print("Tarefas restantes:",tarefas)
			recursos_vcs.pop(maximo)

			# -----------------------
			# VERIFICA PROCESSAMENTO
			# -----------------------
			if len(alocadas_agora) > 0:
				frequencia_total = cluster_manager.controle_recursos[maximo][tempo][local_vc]
				frequencia_vc = frequencia_total / len(alocadas_agora)
				tempo_processamento_tarefas = {}
				controle_local_2 = []
				for now in alocadas_agora:
					tempo_processamento = 0
					tempo_processamento = round(ciclos_temp[now] / frequencia_vc, 2)
					tempo_processamento_tarefas[now] = tempo_processamento
				
				# -----------------------
				# ESCALONA EM DEFINITIVO
				# -----------------------
				escalonamento_controle = {}
				for tarefa_i in alocadas_agora:
					escalonamento_controle[tarefa_i] = {}
					escalonamento_controle[tarefa_i]['processamento'] = tempo_processamento_tarefas[tarefa_i]
					escalonamento_controle[tarefa_i]['local'] = 'vc'
					nuvens[maximo] = tarefa_i
					for tarefa_j in tasks:
						if tarefa_i == tarefa_j[0]:
							tasks.remove(tarefa_j)				
						if tarefa_j[1] > controle_valor_vc:
							tasks.remove(tarefa_j)
							if tarefa_j in tarefas:
								tarefas.remove(tarefa_j)
				
				if len(escalonamento_controle) > 0:
					escalonamento[maximo] = escalonamento_controle

				if len(tarefas) == 0:
					break

		else:
			break
	
	# ALOCA NAS RSUS	
	while len(tasks) > 0:

		if len(recursos_rsus) > 0:
			
			tempo = 0
			maximo = max_value_per_time(recursos_rsus, tempo)
			if maximo == -1:
				break
			maior_vc = recursos_rsus[maximo][tempo]

			controle_valor_vc = 0
			controle_valor_vc = maior_vc

			# maior nuvem menor que a menor tarefa
			min_local = min_value(tasks)
			if maior_vc < min_local:
				print("SEM RECURSOS NAS RSUS!")
				break
			
			alocadas_agora = []

			while maior_vc > 0:
				# print("Capacidade atual:",maior_vc)
				# print(tarefas)

				allocated = GWO.gwo_solution(maior_vc, tarefas)
				if type(allocated) is int:

					if tarefas[allocated][1] <= maior_vc:
						maior_vc = maior_vc - tarefas[allocated][1]
						alocadas_agora.append(tarefas[allocated][0])
						tarefas.pop(allocated)

						if len(tarefas) == 0:
							break
					else:
						break
				else:
					break
			
			recursos_rsus.pop(maximo)

			# -----------------------
			# VERIFICA PROCESSAMENTO
			# -----------------------
			if len(alocadas_agora) > 0:
				frequencia_total = cluster_manager.controle_recursos[maximo][tempo][local_rsu]
				frequencia_vc = frequencia_total / len(alocadas_agora)
				tempo_processamento_tarefas = {}
				controle_local_2 = []
				for now in alocadas_agora:
					tempo_processamento = 0
					tempo_processamento = round(ciclos_temp[now] / frequencia_vc, 2)
					tempo_processamento_tarefas[now] = tempo_processamento
				
				# -----------------------
				# ESCALONA EM DEFINITIVO
				# -----------------------
				escalonamento_controle = {}
				for tarefa_i in alocadas_agora:
					escalonamento_controle[tarefa_i] = {}
					escalonamento_controle[tarefa_i]['processamento'] = tempo_processamento_tarefas[tarefa_i]
					escalonamento_controle[tarefa_i]['local'] = 'rsu'
					for tarefa_j in tasks:
						if tarefa_i == tarefa_j[0]:
							tasks.remove(tarefa_j)				
						if tarefa_j[1] > controle_valor_vc:
							tasks.remove(tarefa_j)
							if tarefa_j in tarefas:
								tarefas.remove(tarefa_j)

				if len(escalonamento_controle) > 0:
					if maximo in nuvens:
						escalonamento[maximo].update(escalonamento_controle)
					else:
						escalonamento[maximo] = escalonamento_controle
				
				if len(tarefas) == 0:
					break

		else:
			break
	
	return escalonamento

def max_value(vcloudDict):
	max_key = max(vcloudDict, key=vcloudDict.get)
	return max_key

def max_value_per_time(vehicular, time):
	
	max_value = 0
	max_key = -1
	for i in vehicular:
		atual = vehicular[i][time]
		if atual > max_value:
			max_value = atual
			max_key = i
	
	return max_key

def min_value(lista):
	minimo = 9999
	for i in lista:
		if i[1] < minimo:
			minimo = i[1]
	return minimo


# # BACKUP MARINA
# def MARINA(vclouds, tasks):

# 	print("\n -> MARINA")

# 	tasks = tasks.copy()
# 	vclouds = vclouds.copy()

# 	tasks_rsu = tasks.copy()
# 	# print("RECURSOS:",cluster_manager.recursos)
	
# 	# CRIA DICIONARIO DE VCS
# 	recursos_vcs = {}
# 	for i in cluster_manager.controle_recursos:
# 		time = {}
# 		for j in cluster_manager.controle_recursos[i]:
# 			time[j] = cluster_manager.controle_recursos[i][j]['vc']
# 		recursos_vcs[i] = time
	
# 	# CRIA DICIONARIO DE RSUS
# 	recursos_rsus = {}
# 	for i in cluster_manager.controle_recursos:
# 		time = {}
# 		for j in cluster_manager.controle_recursos[i]:
# 			time[j] = cluster_manager.controle_recursos[i][j]['rsu']
# 		recursos_rsus[i] = time

# 	# print("RECURSOS_VCS:",recursos_vcs[1])

# 	deadline_temp = {}
# 	ciclos_temp = {}
# 	peso_temp = {}
# 	tarefas_local = {}
# 	tarefas_sinteticas = {}
# 	cont = 0
# 	for i in tasks:
# 		tarefas_local[cont] = i[1]
# 		tarefas_sinteticas[cont] = i[0]
# 		peso_temp[i[0]] = i[1]
# 		ciclos_temp[i[0]] = i[3]
# 		deadline_temp[i[0]] = i[4]
# 		cont += 1
	
# 	controle_marina = {}

# 	tarefas = []
# 	for i in tarefas_local:
# 		tarefas.append(tarefas_local[i])

# 	# tasks = sorted(tasks, reverse=False, key=weight)

# 	# ALOCA NAS VCS
# 	nuvens = {}
# 	while len(tasks) > 0:

# 		if len(recursos_vcs) > 0:

# 			# print("Restaram:",tasks)

# 			# --------------------------
# 			# BIN-PACKING NEXTFIT
# 			# --------------------------
# 			# maximo = max_value(vclouds)
# 			tempo = 0
# 			maximo = max_value_per_time(recursos_vcs, tempo)
# 			valor_bin = recursos_vcs[maximo][tempo]
# 			recursos_vcs.pop(maximo)
		
# 			controle_valor_bin = 0
# 			controle_valor_bin = valor_bin

# 			print("\nNuvem atual:",maximo)
# 			print("Valor:",valor_bin)

# 			# maior nuvem menor que a menor tarefa
# 			min_local = min_value(tasks)
# 			if valor_bin < min_local:
# 				print("SEM ESPAÇO NAS VCS!")
# 				break
		
# 			# --------------------------
# 			# BIN-PACKING PLI - GUROBI
# 			# --------------------------
# 			# transforma dicionario em lista
# 			sintetica_controle = tarefas_sinteticas.copy()

# 			tarefas = []
# 			for i in tarefas_local:
# 				tarefas.append(tarefas_local[i])
			
# 			# BIN PACKING PLI
# 			alocadas_agora = []

# 			# reorganiza tarefas_d
# 			tarefas_sinteticas.clear()
# 			cont = 0
# 			for i in range(len(tarefas)):
# 				if tarefas[i] > valor_bin:
# 					print("Removendo:",i,"->",tarefas[i])
# 					tarefas_local.pop(i)
# 					# tarefas_sinteticas.pop(i)
# 				else:
# 					tarefas_sinteticas[cont] = sintetica_controle[i]
# 					print("Atualizando:",i)
# 					cont += 1

# 			# cont = 0
# 			# for i in teste:
# 			# 	tarefas_sinteticas[cont] = i
# 			# 	cont += 1
# 			if len(tarefas_local) == 0:
# 				break

# 			tarefas = []
# 			for i in tarefas_local:
# 				tarefas.append(tarefas_local[i])

# 			tarefas_local = {}
# 			for i in range(len(tarefas)):
# 				tarefas_local[i] = tarefas[i]

# 			# print("Sintetica ID >",tarefas_sinteticas)
# 			# print("Local PESO >",tarefas_local)
# 			# print("Tarefas >",tarefas)

# 			bin_for_item = binpacking_gurobi.model_bpp(valor_bin, tarefas, LogToConsole=False, TimeLimit=5)
# 			controle_local = binpacking_gurobi.get_items_bpp(tarefas, bin_for_item)
			
# 			# print("Controle local:",controle_local)

# 			melhor_conjunto = 0
# 			id_nuvem = 0
# 			soma_controle = {}
# 			for key,value in controle_local.items():
# 				print(key, value)
# 				soma = 0
# 				soma_controle[key] = {}
# 				for i in value:
# 					soma = soma + tarefas[i]
# 				if soma > melhor_conjunto:
# 					melhor_conjunto = soma
# 					id_nuvem = key
# 				soma_controle[key]['soma'] = soma
# 				soma_controle[key]['quantidade'] = len(value)
				
# 			# seleciona melhor alocacao
# 			# print("nuvem:",id_nuvem)

# 			# print("locais:",tarefas_local)

# 			alocadas_local = []
# 			for i in controle_local[id_nuvem]:
# 				# print(i)
# 				if i in tarefas_local:
# 					# print(i)
# 					alocadas_local.append(i)

# 			# transformar para ID em tasks
# 			for i in alocadas_local:
# 				alocadas_agora.append(tarefas_sinteticas[i])

# 			print("Tarefas candidatas:",alocadas_agora)

# 			# transforma alocadas_local em alocadas_agora
			
# 			'''
# 			# BIN PACKING COM NEXT FIT
			
# 			alocadas_agora = []
# 			for i in tasks:
# 				size = i[1]
# 				if size <= valor_bin:
# 					alocadas_agora.append(i[0])
# 					valor_bin = valor_bin - size
			
# 			print("Tarefas candidatas:",alocadas_agora)
# 			'''

# 			# nenhuma
# 			if len(alocadas_agora) == 0:
# 				print("MIOU")
# 				break

# 			# -----------------------
# 			# VERIFICA DEADLINE
# 			# -----------------------
# 			print("VERIFICANDO DEADLINE")
# 			controle_local = []
# 			for now in alocadas_agora:
# 				# print(" - tarefa:",now)
# 				deadline = deadline_temp[now]
# 				peso = peso_temp[now]
# 				pontuacao = 0
# 				for tempo_k in range(deadline):
# 					# print("Tempo:",tempo)
# 					# print(">>>",cluster_manager.recursos[maximo][tempo])
# 					vc_time = cluster_manager.controle_recursos[maximo][tempo_k]['vc']
# 					# print("vc_time",vc_time)
# 					if vc_time >= peso:
# 						pontuacao += 1
# 				if pontuacao < deadline:
# 					controle_local.append(now)

# 			if len(controle_local) > 0:
# 				for vec in controle_local:
# 					# remove das alocadas
# 					if vec in alocadas_agora:
# 						# print(" * Removeu tarefa:",vec)
# 						alocadas_agora.remove(vec)

# 			# -----------------------
# 			# VERIFICA PROCESSAMENTO
# 			# -----------------------
# 			print("VERIFICANDO PROCESSAMENTO")
# 			# CONSERTAR PARA DIVIDIR ENTRE VEICULOS
# 			# print("cluster_manager.recursos[maximo][0]:",cluster_manager.recursos[maximo][0])
# 			# print("len(alocadas_agora)",len(alocadas_agora))
# 			# frequencia_vc = round(cluster_manager.recursos[maximo][0] / len(alocadas_agora), 2)
# 			if len(alocadas_agora) > 0:
# 				frequencia_vc = cluster_manager.controle_recursos[maximo][tempo][local_vc]
# 				# print("FREQ:",frequencia_vc)
				
# 				tempo_processamento_tarefas = {}

# 				controle_local_2 = []
# 				for now in alocadas_agora:
# 					# print("Tarefa:",now)
# 					tempo_processamento = 0
# 					# print("Ciclos:",ciclos_temp[now])
# 					tempo_processamento = round(ciclos_temp[now] / frequencia_vc, 2)
# 					# print(" * proc:",tempo_processamento)
# 					if tempo_processamento > deadline_temp[now]:
# 						controle_local_2.append(now)
# 					else:
# 						tempo_processamento_tarefas[now] = tempo_processamento

# 				if len(controle_local_2) > 0:
# 					for vec in controle_local_2:
# 						# remove das alocadas
# 						if vec in alocadas_agora:
# 							# print("> Removeu tarefa:",vec)
# 							alocadas_agora.remove(vec)

# 				# -----------------------
# 				# ESCALONA EM DEFINITIVO
# 				# -----------------------
# 				escalonamento_controle = {}
# 				for tarefa_i in alocadas_agora:
# 					escalonamento_controle[tarefa_i] = {}
# 					escalonamento_controle[tarefa_i]['processamento'] = tempo_processamento_tarefas[tarefa_i]
# 					escalonamento_controle[tarefa_i]['local'] = 'vc'
# 					nuvens[maximo] = tarefa_i
# 					for tarefa_j in tasks:
# 						if tarefa_i == tarefa_j[0]:
# 							tasks.remove(tarefa_j)
# 						if tarefa_j[1] > controle_valor_bin:
# 							tasks.remove(tarefa_j)

# 				if len(escalonamento_controle) > 0:
# 					escalonamento[maximo] = escalonamento_controle
# 					# print("Esc:",escalonamento)

# 				for i in alocadas_local:
# 					if i in tarefas_local:
# 						# print("Removendo",i)
# 						tarefas_local.pop(i)
# 						tarefas_sinteticas.pop(i)
				
# 				cont = 0
# 				teste = {}
# 				for i in tarefas_sinteticas:
# 					teste[cont] = tarefas_sinteticas[i]
# 					cont += 1
				
# 				tarefas_sinteticas.clear()
# 				tarefas_sinteticas = teste
				
# 				tarefas = []
# 				for i in tarefas_local:
# 					tarefas.append(tarefas_local[i])
				
# 				tarefas_local.clear()
# 				for i in range(len(tarefas)):
# 					tarefas_local[i] = tarefas[i]
				
# 				if len(tarefas_local) == 0:
# 					print("alocou tudo!")
# 					break

# 				# print("Tarefas apos escolanar:",tarefas)
# 				# print(" ** ",tarefas_local)
# 				# print(" * sintetica:",tarefas_sinteticas)
				
# 				# # reorganiza tarefas_d
# 				# if len(tarefas_local) == 0:
# 				# 	print("alocou tudo!")
# 				# 	break
# 				# else:
# 				# 	tarefas_local = {}
# 				# 	for i in range(len(tarefas)):
# 				# 		tarefas_local[i] = tarefas[i]

# 				# tarefas_sinteticas = {}
# 				# cont = 0
# 				# for i in tasks:
# 				# 	tarefas_sinteticas[cont] = i[0]
# 				# 	cont += 1

# 		else:
# 			break
	
# 	for i in escalonamento:
# 		for j in escalonamento[i]:
# 			for k in tasks_rsu:
# 				if j == k[0]:
# 					tasks_rsu.remove(k)
	
# 	# print("Atualizado:",tasks_rsu)

# 	# atualizando tarefas
# 	tarefas_local = {}
# 	tarefas_sinteticas = {}
# 	cont = 0
# 	for i in tasks_rsu:
# 		tarefas_local[cont] = i[1]
# 		tarefas_sinteticas[cont] = i[0]
# 		cont += 1
	
# 	tarefas = []
# 	for i in tarefas_local:
# 		tarefas.append(tarefas_local[i])

# 	# print("Tarefas LOCAL RSUS",tarefas_local)
# 	# print("Tarefas SINTETICA RSUS",tarefas_sinteticas)

# 	# ALOCA NAS RSUS
# 	while len(tasks_rsu) > 0:
# 		if len(recursos_rsus) > 0:

# 			# print("Restaram:",tasks)

# 			# --------------------------
# 			# BIN-PACKING NEXTFIT
# 			# --------------------------
# 			# maximo = max_value(vclouds)
# 			tempo = 0
# 			maximo = max_value_per_time(recursos_rsus, tempo)
# 			valor_bin = recursos_rsus[maximo][tempo]
# 			recursos_rsus.pop(maximo)
		
# 			controle_valor_bin = 0
# 			controle_valor_bin = valor_bin

# 			print("\nNuvem atual:",maximo)
# 			print("Valor:",valor_bin)

# 			# maior nuvem menor que a menor tarefa
# 			min_local = min_value(tasks)
# 			if valor_bin < min_local:
# 				print("SEM ESPAÇO NAS RSUS!")
# 				break

# 			# --------------------------
# 			# BIN-PACKING PLI - GUROBI
# 			# --------------------------
# 			# transforma dicionario em lista
# 			sintetica_controle = tarefas_sinteticas.copy()

# 			tarefas = []
# 			for i in tarefas_local:
# 				tarefas.append(tarefas_local[i])
			
# 			# BIN PACKING PLI
# 			alocadas_agora = []

# 			# reorganiza tarefas_d
# 			tarefas_sinteticas.clear()
# 			cont = 0
# 			for i in range(len(tarefas)):
# 				if tarefas[i] > valor_bin:
# 					print("Removendo:",i,"->",tarefas[i])
# 					tarefas_local.pop(i)
# 					# tarefas_sinteticas.pop(i)
# 				else:
# 					tarefas_sinteticas[cont] = sintetica_controle[i]
# 					print("Atualizando:",i)
# 					cont += 1

# 			if len(tarefas_local) == 0:
# 				break
# 			# cont = 0
# 			# for i in teste:
# 			# 	tarefas_sinteticas[cont] = i
# 			# 	cont += 1

# 			tarefas = []
# 			for i in tarefas_local:
# 				tarefas.append(tarefas_local[i])

# 			tarefas_local = {}
# 			for i in range(len(tarefas)):
# 				tarefas_local[i] = tarefas[i]

# 			# print("Sintetica ID >",tarefas_sinteticas)
# 			# print("Local PESO >",tarefas_local)
# 			print("Tarefas >",tarefas)

# 			bin_for_item = binpacking_gurobi.model_bpp(valor_bin, tarefas, LogToConsole=False, TimeLimit=5)
# 			controle_local = binpacking_gurobi.get_items_bpp(tarefas, bin_for_item)
			
# 			print("Controle local:",controle_local)

# 			melhor_conjunto = 0
# 			id_nuvem = 0
# 			soma_controle = {}
# 			for key,value in controle_local.items():
# 				print(key, value)
# 				soma = 0
# 				soma_controle[key] = {}
# 				for i in value:
# 					soma = soma + tarefas[i]
# 				if soma > melhor_conjunto:
# 					melhor_conjunto = soma
# 					id_nuvem = key
# 				soma_controle[key]['soma'] = soma
# 				soma_controle[key]['quantidade'] = len(value)
				
# 			# seleciona melhor alocacao
# 			# print("nuvem:",id_nuvem)

# 			# print("locais:",tarefas_local)

# 			alocadas_local = []
# 			for i in controle_local[id_nuvem]:
# 				# print(i)
# 				if i in tarefas_local:
# 					# print(i)
# 					alocadas_local.append(i)

# 			# transformar para ID em tasks
# 			for i in alocadas_local:
# 				alocadas_agora.append(tarefas_sinteticas[i])

# 			print("Tarefas candidatas:",alocadas_agora)
			
# 			'''
# 			# BIN PACKING COM NEXT FIT
# 			alocadas_agora = []
# 			for i in tasks:
# 				size = i[1]
# 				if size <= valor_bin:
# 					alocadas_agora.append(i[0])
# 					valor_bin = valor_bin - size

# 			print("Tarefas candidatas:",alocadas_agora)
# 			'''

# 			# nenhuma
# 			if len(alocadas_agora) == 0:
# 				break

# 			# -----------------------
# 			# VERIFICA DEADLINE
# 			# -----------------------
# 			print("VERIFICANDO DEADLINE")
# 			controle_local = []
# 			for now in alocadas_agora:
# 				# print(" - tarefa:",now)
# 				deadline = deadline_temp[now]
# 				peso = peso_temp[now]
# 				pontuacao = 0
# 				for tempo_k in range(deadline):
# 					# print("Tempo:",tempo)
# 					# print(">>>",cluster_manager.recursos[maximo][tempo])
# 					vc_time = cluster_manager.controle_recursos[maximo][tempo_k]['vc']
# 					# print("vc_time",vc_time)
# 					if vc_time >= peso:
# 						pontuacao += 1
# 				if pontuacao < deadline:
# 					controle_local.append(now)

# 			if len(controle_local) > 0:
# 				for vec in controle_local:
# 					# remove das alocadas
# 					if vec in alocadas_agora:
# 						# print(" * Removeu tarefa:",vec)
# 						alocadas_agora.remove(vec)

# 			# -----------------------
# 			# VERIFICA PROCESSAMENTO
# 			# -----------------------
# 			print("VERIFICANDO PROCESSAMENTO")
# 			# CONSERTAR PARA DIVIDIR ENTRE VEICULOS
# 			# print("cluster_manager.recursos[maximo][0]:",cluster_manager.recursos[maximo][0])
# 			# print("len(alocadas_agora)",len(alocadas_agora))
# 			# frequencia_vc = round(cluster_manager.recursos[maximo][0] / len(alocadas_agora), 2)
# 			if len(alocadas_agora) > 0:
# 				frequencia_vc = cluster_manager.controle_recursos[maximo][tempo][local_rsu]
# 				# print("FREQ:",frequencia_vc)
				
# 				tempo_processamento_tarefas = {}

# 				controle_local_2 = []
# 				for now in alocadas_agora:
# 					# print("Tarefa:",now)
# 					tempo_processamento = 0
# 					# print("Ciclos:",ciclos_temp[now])
# 					tempo_processamento = round(ciclos_temp[now] / frequencia_vc, 2)
# 					# print(" * proc:",tempo_processamento)
# 					if tempo_processamento > deadline_temp[now]:
# 						controle_local_2.append(now)
# 					else:
# 						tempo_processamento_tarefas[now] = tempo_processamento

# 				if len(controle_local_2) > 0:
# 					for vec in controle_local_2:
# 						# remove das alocadas
# 						if vec in alocadas_agora:
# 							# print("> Removeu tarefa:",vec)
# 							alocadas_agora.remove(vec)

# 				# -----------------------
# 				# ESCALONA EM DEFINITIVO
# 				# -----------------------
# 				escalonamento_controle = {}
# 				for tarefa_i in alocadas_agora:
# 					escalonamento_controle[tarefa_i] = {}
# 					escalonamento_controle[tarefa_i]['processamento'] = tempo_processamento_tarefas[tarefa_i]
# 					escalonamento_controle[tarefa_i]['local'] = 'rsu'
# 					for tarefa_j in tasks_rsu:
# 						if tarefa_i == tarefa_j[0]:
# 							tasks_rsu.remove(tarefa_j)
# 						if tarefa_j[1] > controle_valor_bin:
# 							tasks_rsu.remove(tarefa_j)
				
# 				if len(escalonamento_controle) > 0:
# 					if maximo in nuvens:
# 						escalonamento[maximo].update(escalonamento_controle)
# 					else:
# 						escalonamento[maximo] = escalonamento_controle

# 				for i in alocadas_local:
# 					if i in tarefas_local:
# 						# print("Removendo",i)
# 						tarefas_local.pop(i)
# 						tarefas_sinteticas.pop(i)
				
# 				cont = 0
# 				teste = {}
# 				for i in tarefas_sinteticas:
# 					teste[cont] = tarefas_sinteticas[i]
# 					cont += 1
				
# 				tarefas_sinteticas.clear()
# 				tarefas_sinteticas = teste
				
# 				tarefas = []
# 				for i in tarefas_local:
# 					tarefas.append(tarefas_local[i])
				
# 				tarefas_local.clear()
# 				for i in range(len(tarefas)):
# 					tarefas_local[i] = tarefas[i]
				
# 				if len(tarefas_local) == 0:
# 					print("alocou tudo RSU!")
# 					break

# 		else:
# 			break

# 	return escalonamento