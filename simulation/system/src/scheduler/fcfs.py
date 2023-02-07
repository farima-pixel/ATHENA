#!/usr/bin/python3
# title: fcfs.py
# author: Joahannes Costa <joahannes@lrc.ic.unicamp.br>
# date: 21.06.2022

def run(queue, clouds, tasks):
	
	print("executando FCFS....")
	result = {}
	
	local_tasks = {}
	local_tasks_deadline = {}
	for i in queue.get_queue():
		if queue.task_queue_control[i[1]]['status'] == 'PENDING':
			local_tasks[i[1]] = queue.task_queue_control[i[1]]['size']
			local_tasks_deadline[i[1]] = i[0]

	# print("Tarefas:")
	# for i in queue.task_queue_control:
	# 	print(i, queue.task_queue_control[i])
	sorted_clouds = []
	local_clouds = {}
	for i in clouds.clouds:
		local_clouds[i] = clouds.clouds[i]['mips']
		sorted_clouds.append(i)

	# sorted_clouds = sorted(local_clouds, key=lambda x: local_clouds[x], reverse=False)
	# sorted_clouds = sorted(local_clouds, key=lambda x: local_clouds[x], reverse=False)
	resource_splited = {}

	for cloud in range(len(sorted_clouds)):
		
		if len(local_tasks) > 0:

			id_nuvem = sorted_clouds[cloud]
			result[id_nuvem] = {}

			cloud_capacity = sorted_clouds[cloud]
			local_result = {}

			min_task_size = min(local_tasks, key=local_tasks.get)
			if local_tasks[min_task_size] > local_clouds[id_nuvem]:
				# print("NUVEM SEM RECURSOS!")
				break

			# FIFO GREEDY CLASSICO
			for task in local_tasks:
				if local_tasks[task] <= cloud_capacity:
					local_result[task] = -1
					cloud_capacity -= local_tasks[task]
				else:
					break
			
			if len(local_result) > 0:

				# VERIFICA PROCESSAMENTO E ADICIONA ESTIMATIVA NA TAREFA
				processing = get_processing_time(local_clouds[id_nuvem], tasks, local_result)
				for task in processing:
					local_result[task] = processing[task]

				# MAPEAMENTO DE USO DOS RECURSOS
				resource_splited[id_nuvem] = split_resource(local_result, clouds.clouds[id_nuvem], local_tasks)

				# REMOVE TAREFAS ESCALONADAS E VERIFICADAS
				for i in local_result:
					del local_tasks[i]
					del local_tasks_deadline[i]

				result[id_nuvem] = local_result

			else:
				# SEM RESULTADO
				pass
		else:
			# TODAS TAREFAS ESCALONADAS
			break
	
	print(" ** ",result)
	return result, resource_splited

def get_processing_time(cloud_frequency, tasks, local_schedule):
	tasks_frequency = {}
	total_frequency = cloud_frequency
	scheduled_tasks = len(local_schedule)
	shared_frequency = total_frequency / scheduled_tasks

	for task in local_schedule:
		# TODO: SUBSTITUIR POR SIZE?
		medida_tarefa = tasks.task_set_control[task]['cpu']
		task_time = round((medida_tarefa / shared_frequency), 2)
		tasks_frequency[task] = task_time

	return tasks_frequency

def split_resource(local_schedule, current_cloud, local_tasks):
	"Return the resources usage."
	resources = {}
	vehicle  = current_cloud['vehicle_cpu']
	bs 		 = current_cloud['bs_cpu']

	for task in local_schedule:
		used_vehicle = 0
		used_bs = 0
		resources[task] = {}
		size_task = local_tasks[task]
		for i in range(1, size_task + 1):

			if vehicle > 0:
				vehicle -= 1
				used_vehicle += 1
			elif vehicle == 0:
				size_task = size_task - used_vehicle
				if bs > 0:
					bs -= 1
					used_bs += 1
			
			resources[task]['vehicle']			= used_vehicle
			resources[task]['bs'] 				= used_bs
			resources[task]['processing_time'] 	= local_schedule[task]
			resources[task]['size'] 			= local_tasks[task]

	# print("Resouces Usage:",resources)
	return resources