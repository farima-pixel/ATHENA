#!/usr/bin/env python
# title: log_manager.py
# author: Joahannes Costa <joahannes@lrc.ic.unicamp.br>
# date: 25.03.2021

# LOG
#===============================================================#
# [0] step														#
# [1] recurso das vccs											#
# [2] numero de tarefas geradas									#
# [3] algoritmo utilizado										#
# [4] ganho por alocar as n tarefas								#
# [5] tarefas que foram alocadas								#
# [6] numero de vccs criadas									#
# [7] peso das tarefas											#
# [8] cpu_time													#
# [9] delay														#
#===============================================================#

import os
import numpy as np

def get_information(radius, resources, weight, rate, megacycles, algorithm, seed, deadline):
	
	# cria diretorio para cada algoritmo em output
	dirName = 'output/' + algorithm
	if not os.path.isdir(dirName):
		os.makedirs(dirName)
	
	# # cria diretorio para cada algoritmo em log
	# dirNameLog = 'log/' + algorithm
	# if not os.path.isdir(dirNameLog):
	# 	os.makedirs(dirNameLog)

	global name_alloc
	global name_time
	global name_queue
	global name_cluster
	global name_fila
	radius_log = int(radius)
	global resource_log 
	resource_log = resources
	weight_log = weight

	name_alloc = dirName + '/SEED_'+str(seed)+'_RESULTS_radius_'+str(radius_log)+'_resource_'+str(resource_log)+'_weight_'+str(weight_log)+'_rate_'+str(rate)+'_megacycles_'+str(megacycles)+'_deadline_'+str(deadline)+'.txt'
	name_time = dirName + '/SEED_'+str(seed)+'_TIME_radius_'+str(radius_log)+'_resource_'+str(resource_log)+'_weight_'+str(weight_log)+'_rate_'+str(rate)+'_megacycles_'+str(megacycles)+'_deadline_'+str(deadline)+'.txt'
	name_queue = dirName + '/SEED_'+str(seed)+'_COST_radius_'+str(radius_log)+'_resource_'+str(resource_log)+'_weight_'+str(weight_log)+'_rate_'+str(rate)+'_megacycles_'+str(megacycles)+'_deadline_'+str(deadline)+'.txt'

	if os.path.exists(name_alloc):
		os.system('rm ' + name_alloc)
	if os.path.exists(name_time):
		os.system('rm ' + name_time)
	if os.path.exists(name_queue):
		os.system('rm ' + name_queue)

	name_cluster = dirName + '/CLUSTER_SEED_1_' + str(rate) + '.txt'
	name_fila = dirName + '/FILA_SEED_1_' + str(rate) + '.txt'

def log_resources(step, number, resource_per_cluster, resource, weight, radius):
	resources_file = open('output/resources_'+str(radius)+'_'+str(resource)+'_'+str(weight)+'.txt','a')
	resources_file.write(str(step) + "," + str(number) + "," + str(resource_per_cluster) + "\n")
	resources_file.close()

	return resources_file

def log_tasks(step, number, tasks, resource, weight, radius):
	tasks_file = open('output/tasks_'+str(radius)+'_'+str(resource)+'_'+str(weight)+'.txt','a')
	tasks_file.write(str(step) + "," + str(number) + "," + str(tasks) + "\n")
	tasks_file.close()

	return tasks_file

def log_allocation(step, n_tasks, total_cpu_time):

	total_cpu_time = round(total_cpu_time, 5)

	allocation_file = open(name_alloc,'a')
	allocation_file.write(
		str(step) + "\t" +
		str(n_tasks) + "\t" +
		str(total_cpu_time) + "\n"
		)
	allocation_file.close()

def log_time(resultado):

	time_file = open(name_time,'a')
	time_file.write(str(resultado) + "\n")
	time_file.close()

def log_cost(resultado_price):

	queue_file = open(name_queue,'a')
	queue_file.write(str(resultado_price) + "\n")
	queue_file.close()

def log_cluster(step, nuvens):
	nuvem_escolhida = 4
	cluster_file = open(name_cluster, 'a')
	cluster_file.write(str(step) + '\t' + str(nuvens[nuvem_escolhida][0]) + '\n')
	cluster_file.close()

def log_fila(step, fila):
	fila_file = open(name_fila, 'a')
	fila_file.write(str(step) + '\t' + str(len(fila)) + '\n')
	fila_file.close()

def log_results(resultados):
	
	total_tasks = len(resultados)
	escalonadas = 0
	delay = []
	queue_time = []

	status_aceitos = ['PENDING', 'SUBMITTED', 'EXPIRED']

	for i in resultados:

		insert_time = float(resultados[i]['insert_time'])
		remove_time = float(resultados[i]['remove_time'])
		queue_time.append(remove_time - insert_time)

		if resultados[i]['status'] not in status_aceitos:
			start_time = float(resultados[i]['start_time'])
			finish_time = float(resultados[i]['finish_time'])
			delay.append(finish_time - start_time)

		if resultados[i]['status'] == 'COMPLETED':
			escalonadas += 1
			
	porcentagem 			= round((escalonadas * 100 / total_tasks),2)
	total_delay 			= round(np.mean(delay), 2)
	total_delay_std 		= round(np.std(delay), 2)
	total_queue_time 		= round(np.mean(queue_time), 2)
	total_queue_time_std 	= round(np.std(queue_time), 2)

	print(" * Total:",total_tasks)
	print(" * Escalonadas:",escalonadas)
	print(" * Porcentagem:",porcentagem)
	print(" * Delay:", total_delay)
	print(" * Queue:", total_queue_time)

	allocation_file = open(name_alloc,'a')
	allocation_file.write(
		str(total_tasks) + "\t" +
		str(escalonadas) + "\t" +
		str(porcentagem) + "\t" +
		str(total_delay) + "\t" +
		str(total_delay_std) + "\t" +
		str(total_queue_time) + "\t" +
		str(total_queue_time_std) + "\n"
		)
	allocation_file.close()

def log_results_final(resultados):
	
	total_tasks = len(resultados)

	allocation_file = open(name_alloc,'a')

	for i in resultados:
		allocation_file.write(
			str(total_tasks) + "\t" +
			str(i) + "\t" +
			str(resultados[i]['size']) + "\t" +
			str(resultados[i]['value']) + "\t" +
			str(resultados[i]['cpu']) + "\t" +
			str(resultados[i]['deadline']) + "\t" +
			str(resultados[i]['insert_time']) + "\t" +
			str(resultados[i]['start_time']) + "\t" +
			str(resultados[i]['finish_time']) + "\t" +
			str(resultados[i]['remove_time']) + "\t" +
			str(resultados[i]['waiting_time']) + "\t" +
			str(resultados[i]['cost']) + "\t" +
			str(resultados[i]['status']) + "\n"
		)

	allocation_file.close()

	escalonadas = 0
	delay = []
	queue_time = []
	cost = []

	status_aceitos = ['PENDING', 'SUBMITTED', 'EXPIRED']

	for i in resultados:

		insert_time = float(resultados[i]['insert_time'])
		remove_time = float(resultados[i]['remove_time'])
		queue_time.append(remove_time - insert_time)

		if resultados[i]['cost'] != None:
			cost.append(float(resultados[i]['cost']))

		if resultados[i]['status'] not in status_aceitos:
			start_time = float(resultados[i]['start_time'])
			finish_time = float(resultados[i]['finish_time'])
			delay.append(finish_time - start_time)

		if resultados[i]['status'] == 'COMPLETED':
			escalonadas += 1
			
	porcentagem 			= round((escalonadas * 100 / total_tasks),2)
	total_delay 			= round(np.mean(delay), 2)
	total_delay_std 		= round(np.std(delay), 2)
	total_queue_time 		= round(np.mean(queue_time), 2)
	total_queue_time_std 	= round(np.std(queue_time), 2)
	total_cost				= round(np.mean(cost), 2)		

	print(" * Total:",total_tasks)
	print(" * Escalonadas:",escalonadas)
	print(" * Porcentagem:",porcentagem)
	print(" * Delay:", total_delay)
	print(" * Queue:", total_queue_time)
	print(" * Costs:", total_cost)