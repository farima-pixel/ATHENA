#!/usr/bin/env python
# title: monitor.py
# author: Joahannes Costa <joahannes@lrc.ic.unicamp.br>
# date: 04.11.2021

import random
import log_manager

class SchedulingMonitor():

	def get_status(self, step, schedule, task, cloud, queue):

		self.actual_time = step
		print("MONITOR ESCALONAMENTO...", self.actual_time)

		'''
		ATUALIZA FILA DE TAREFAS
		'''
		queue.update(step, schedule)

		print(schedule.escalonamento)

		'''
		ATUALIZA STATUS DAS TAREFAS
		# 1. verifica se a tarefa completou seu processamento [OK]
		# 2. remove tarefa completa da fila de execução e de espera [OK]
		# 3. atualiza informacao da nuvem veicular com base na tarefa que saiu [PENDENTE]
		# ABORDAGENS DIFERENTES DO MARINA:
		#  ---> # 4. se nuvem.recurso < tarefas, então cancela o processamento de todas.
		'''
		# print("CLOUDS")
		# for i in cloud.clouds:
		# 	print(i, cloud.clouds[i])

		self.for_removing_now = []
			
		for cloud_i, tasks_j in schedule.escalonamento.items():
			
			for item in tasks_j:

				if float(self.actual_time) >= float(queue.task_queue_control[item]['finish_time']):
					
					if queue.task_queue_control[item]['status'] == 'SUBMITTED':
						print(item + " concluiu seu processamento!")
						# TODO: MODELAR DELAY PARA ADICIONAR NESSA MÉTRICA
						# task_remove_time = float(self.actual_time) + round(random.random(), 4)
						task_remove_time = round(queue.task_queue_control[item]['finish_time'] + random.uniform(0.1, 0.5), 4)
						queue.task_queue_control[item]['remove_time'] = task_remove_time
						queue.task_queue_control[item]['status'] = 'COMPLETED'
						queue.final_queue[item]['remove_time'] = task_remove_time
						queue.final_queue[item]['status'] = 'COMPLETED'
						# REMOVE TAREFA DA HEAP
						position = -1
						for q_item in queue.task_queue:
							position += 1
							if item == q_item[1]:
								del queue.task_queue[position]
						
						# print("ESTRUTURA DE DADOS DE RECURSOS")
						# print(schedule.resource_usage)

						# READICIONA RECURSO NA VC CORRESPONDENTE
						task_info_resource = schedule.resource_usage[cloud_i][item]
						print(task_info_resource)

						if cloud_i == 'masterfog':
							cloud.update(cloud_i, task_info_resource, 'complete', 'masterfog')
							local_cost = self.resource_price(task_info_resource, 'masterfog')
							queue.final_queue[item]['cost'] = local_cost

						elif cloud_i == 'remotecloud':
							cloud.update(cloud_i, task_info_resource, 'complete', 'remotecloud')
							local_cost = self.resource_price(task_info_resource, 'remotecloud')
							queue.final_queue[item]['cost'] = local_cost

						else:
							cloud.update(cloud_i, task_info_resource, 'complete', 'vcs')
							local_cost = self.resource_price(task_info_resource, 'vcs')
							queue.final_queue[item]['cost'] = local_cost

						del schedule.resource_usage[cloud_i][item]
						self.for_removing_now.append([cloud_i, item])
				
					elif queue.task_queue_control[item]['status'] == 'EXPIRED':

						task_info_resource = schedule.resource_usage[cloud_i][item]
						
						if cloud_i == 'masterfog':
							cloud.update(cloud_i, task_info_resource, 'complete', 'masterfog')
							local_cost = self.resource_price(task_info_resource, 'masterfog')
							queue.final_queue[item]['cost'] = local_cost
						elif cloud_i == 'remotecloud':
							cloud.update(cloud_i, task_info_resource, 'complete', 'remotecloud')
							local_cost = self.resource_price(task_info_resource, 'remotecloud')
							queue.final_queue[item]['cost'] = local_cost
						else:
							cloud.update(cloud_i, task_info_resource, 'complete', 'vcs')
							local_cost = self.resource_price(task_info_resource, 'vcs')
							queue.final_queue[item]['cost'] = local_cost

						del schedule.resource_usage[cloud_i][item]
						self.for_removing_now.append([cloud_i, item])

		# print("PARA REMOVER AGORA")
		# print(self.for_removing_now)

		# REMOVE TAREFAS CONCLUIDAS DA ESTRUTURA DE ESCALONAMENTO
		for remove_id in self.for_removing_now:
			del schedule.escalonamento[remove_id[0]][remove_id[1]]

		# for remove_id in testes:
		# 	del 


	def check_vehicular_cloud(self, cloud, queue):
		"Check resources in each vehicular clouds."
		return 0

	def resource_price(self, uso_recursos, resource_type):
		"Define monetary cost based on resource used."
		total_price = 0
		time_using = uso_recursos['processing_time']
		
		vehicle_price = 6.016
		bs_price = 15.444
		mfn_price = 24.480
		cloud_price = 32.772

		if resource_type == 'vcs':
			vehicle_total_cost = (vehicle_price * uso_recursos['vehicle']) * time_using
			bs_total_cost = (bs_price * uso_recursos['bs']) * time_using
			total_price = round(vehicle_total_cost + bs_total_cost, 3)

		elif resource_type == 'masterfog':
			mfn_total_cost = (mfn_price * uso_recursos['mfn']) * time_using
			total_price = round(mfn_total_cost, 3)

		elif resource_type == 'remotecloud':
			rc_total_cost = (rc_price * uso_recursos['rc']) * time_using
			total_price = round(rc_total_cost, 3)

		# print("PRECIFICANDO USO RECURSOS")
		print("Total: $",total_price)

		return total_price
