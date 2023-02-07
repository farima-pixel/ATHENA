#!/usr/bin/python3
# title: tovec.py
# author: Joahannes Costa <joahannes@lrc.ic.unicamp.br>
# date: 21.06.2022

import utils.PARETO as PARETOSET

def request_prediction(initial_time, timewindow, tasks):
	expected_tasks = 0
	for timestep in tasks.tasks_number[:timewindow]:
		expected_tasks += timestep[1]
	return expected_tasks

def run(queue, clouds, tasks):
	
	print("executando PARETO....")
	result = {}
	resource_splited = {}
	
	local_tasks = {}
	tasks_pareto = {}
	local_tasks_deadline = {}
	for i in queue.get_queue():
		if queue.task_queue_control[i[1]]['status'] == 'PENDING':
			local_tasks[i[1]] = queue.task_queue_control[i[1]]['size']
			# PARA PARETO
			local_tasks_deadline[i[1]] = i[0]
			tasks_pareto[i[1]] = [queue.task_queue_control[i[1]]['cpu'], queue.task_queue_control[i[1]]['size'], queue.task_queue_control[i[1]]['deadline']]

	'''
	# BEGIN: REQUEST PREDICTION
	'''
	if len(local_tasks) > 10:
		result_remotecloud = {}
		result_masterfog   = {}
		candidate = request_prediction(100, 5, tasks)
		result_masterfog, result_remotecloud = send_to_up_tier(candidate, clouds, local_tasks, local_tasks_deadline, tasks)
		result['masterfog'] = result_masterfog
		result['remotecloud'] = result_remotecloud

		resource_splited['masterfog'] = split_resource_up_tier('masterfog', result_masterfog, clouds.masterfognodes[0], local_tasks)
		resource_splited['remotecloud'] = split_resource_up_tier('remotecloud', result_remotecloud, clouds.remotecloud[0], local_tasks)

		if len(result_masterfog) > 0:
			for i in result_masterfog:
				del local_tasks[i]
				del tasks_pareto[i]
				del local_tasks_deadline[i]

		if len(result_remotecloud) > 0:
			for i in result_remotecloud:
				del local_tasks[i]
				del tasks_pareto[i]
				del local_tasks_deadline[i]
	'''
	# END: REQUEST PREDICTION
	'''

	# print("Tarefas:")
	# for i in queue.task_queue_control:
	# 	print(i, queue.task_queue_control[i])
	# sorted_clouds = []
	local_clouds = {}
	for i in clouds.clouds:
		local_clouds[i] = clouds.clouds[i]['mips']
		# sorted_clouds.append(i)
	
	# sorted_clouds = sorted(local_clouds, key=lambda x: local_clouds[x], reverse=False)
	sorted_clouds = sorted(local_clouds, key=lambda x: local_clouds[x], reverse=True)

	for cloud in range(len(sorted_clouds)):
		
		if len(local_tasks) > 0:

			id_nuvem = sorted_clouds[cloud]
			result[id_nuvem] = {}

			# print("Nuvem:",id_nuvem)

			cloud_capacity = sorted_clouds[cloud]
			local_result = {}

			min_task_size = min(local_tasks, key=local_tasks.get)
			if local_tasks[min_task_size] > local_clouds[id_nuvem]:
				# print("NUVEM SEM RECURSOS!")
				break
			
			# EXECUTA ABORDAGEM DE ESCALONAMENTO AQUI
			# PARETO
			# while cloud_capacity > 0:

			temporary_result = PARETOSET.run_pareto_set(tasks_pareto, cloud_capacity)

			local_pareto_deadline = {}
			for item_pareto in temporary_result:
				local_pareto_deadline[item_pareto] = local_tasks_deadline[item_pareto]

			# organiza estrututa de dados de resultado temporario
			if len(temporary_result) > 0:
				for task_i in temporary_result:
					id_task_now = task_i
					if local_tasks[id_task_now] <= cloud_capacity:
						local_result[id_task_now] = -1
						cloud_capacity -= local_tasks[id_task_now]
						if len(local_tasks) == 0:
							break
					else:
						break

			# print("Local result:",local_result)
				
			if len(local_result) > 0:

				# ADICIONAR VERIFICACAO DE RECURSOS FUTUROS AQUI
				'''
				INICIO: USO DE DADOS PREDITOS
				'''
				# GUARDA DEADLINE DAS CANDIDATAS
				deadlines = {}
				for task in local_result:
					deadlines[task] = local_pareto_deadline[task]
				sorted_deadlines = sorted(list(deadlines.keys()), key=lambda x: deadlines[x], reverse=True)

				# APENAS PARA TESTE DO MECANISMO
				# FIXME:
				# clouds.clouds[180] = {'members': 17, 'vehicle_cpu': 7, 'bs_cpu': 10, 'mips': 17, 'prediction': [17, 17, 17, 16, 16]}
				# clouds.clouds[id_nuvem]['prediction'] = [17, 17, 17, 16, 16]

				to_remove_based_on_deadline = {}
				list_remove_based_deadline = []
				# VERIFICA RECURSOS PARA CADA t \in T DA JANELA DE PREDICAO
				# print("MINHA CLOUD:",clouds.clouds[id_nuvem]['prediction'])
				for cloud_t in clouds.clouds[id_nuvem]['prediction']:
					items = [local_tasks[x] if x in local_tasks else 0 for x in local_result]
					sum_tasks = sum(items)
					value = abs(cloud_t - sum_tasks)
					# SE DIFERENCA DE RECURSOS FOR MAIOR QUE ZERO
					if value > 0:
						# SE SOMA DE TAREFAS FOR MAIOR QUE CAPACIDADE ATUAL
						# REMOVE A TAREFA COM MAIOR DEADLINE, OU SEJA, PODE ESPERAR MAIS
						#print(sum_tasks, cloud_t)
						if sum_tasks > cloud_t:
							maximo = sorted_deadlines[0]
							# print("MAXIMO ATUAL:",maximo)
							del local_result[maximo]
							sorted_deadlines.remove(maximo)
							list_remove_based_deadline.append(maximo)
				'''
				FINAL: USO DE DADOS PREDITOS
				'''

				'''
				modificacao paper farima, send_to_up_tier()
				'''
				if len(list_remove_based_deadline) > 0:
					result_remotecloud = {}
					result_masterfog   = {}
					result_masterfog, result_remotecloud = send_to_up_tier(clouds, list_remove_based_deadline, tasks)
					result['masterfog'] = result_masterfog
					result['remotecloud'] = result_remotecloud

					resource_splited['masterfog'] = split_resource_up_tier('masterfog', result_masterfog, clouds.masterfognodes[0], local_tasks)
					resource_splited['remotecloud'] = split_resource_up_tier('remotecloud', result_remotecloud, clouds.remotecloud[0], local_tasks)

					if len(result_masterfog) > 0:
						for i in result_masterfog:
							del local_tasks[i]
							del tasks_pareto[i]
							del local_tasks_deadline[i]

					if len(result_remotecloud) > 0:
						for i in result_remotecloud:
							del local_tasks[i]
							del tasks_pareto[i]
							del local_tasks_deadline[i]
				'''
				modificacao paper farima, send_to_up_tier()
				'''

				# VERIFICA PROCESSAMENTO E ADICIONA ESTIMATIVA NA TAREFA
				processing = get_processing_time(local_clouds[id_nuvem], tasks, local_result)
				for task in processing:
					local_result[task] = processing[task]

				# MAPEAMENTO DE USO DOS RECURSOS
				resource_splited[id_nuvem] = split_resource(local_result, clouds.clouds[id_nuvem], local_tasks)

				# REMOVE TAREFAS ESCALONADAS E VERIFICADAS
				for i in local_result:
					del local_tasks[i]
					del tasks_pareto[i]
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


def send_to_up_tier(number_tasks, clouds, candidate_tasks, candidate_tasks_deadline, tasks):
	print("SEND TO UP TIER")
	local_result = {}
	master_fogs  = {}
	remote_cloud = {}

	sorted_tasks = sorted(candidate_tasks_deadline, key=lambda x: candidate_tasks_deadline[x], reverse=True)
	
	# print(candidate_tasks)
	# print("Deadline:",sorted_tasks)
	# print("Consider:",number_tasks)
	# print(">",sorted_tasks[:number_tasks])

	for tasks_i in sorted_tasks[:number_tasks]:
		print(tasks_i) # id-00001]

		if clouds.masterfognodes[0]["size"] > 0:
			master_fogs[tasks_i] = -1
			
		elif clouds.masterfognodes[0]["size"] <= 0 and clouds.remotecloud[0]["size"] > 0:
			remote_cloud[tasks_i] = -1

		else:
			print("System without resources!")
	
	if len(master_fogs) > 0:
		processing_mfn = get_processing_time(clouds.masterfognodes[0]["mips"], tasks, master_fogs)
		for task in processing_mfn:
			master_fogs[task] = processing_mfn[task]

	if len(remote_cloud) > 0:
		processing_rc = get_processing_time(clouds.remotecloud[0]["mips"], tasks, remote_cloud)
		for task in processing_rc:
			remote_cloud[task] = processing_rc[task]
	

	print(master_fogs)
	print(remote_cloud)
	return master_fogs, remote_cloud

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

def split_resource_up_tier(entity, local_schedule, current_cloud, local_tasks):
	"Return the resources usage."
	resources = {}

	if entity == 'remotecloud':
		remotecloud  = current_cloud['cpu']
		for task in local_schedule:
			resource_used = 0
			resources[task] = {}
			size_task = local_tasks[task]
			for i in range(1, size_task + 1):
				resource_used += 1
				remotecloud -= 1
				resources[task]['rc']				= resource_used
				resources[task]['processing_time'] 	= local_schedule[task]
				resources[task]['size'] 			= local_tasks[task]

	elif entity == 'masterfog':
		masterfog  = current_cloud['cpu']
		for task in local_schedule:
			resource_used = 0
			resources[task] = {}
			size_task = local_tasks[task]
			for i in range(1, size_task + 1):
				resource_used += 1
				masterfog -= 1
				resources[task]['mfn']				= resource_used
				resources[task]['processing_time'] 	= local_schedule[task]
				resources[task]['size'] 			= local_tasks[task]

	# print("Resouces Usage:",resources)
	return resources