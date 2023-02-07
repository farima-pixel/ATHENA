#!/usr/bin/python3
# title: scheduling_manager.py
# author: Joahannes Costa <joahannes@lrc.ic.unicamp.br
# date: 22.10.2021

# gerais
import log_manager as log
import cluster_manager
import random
import time

# algoritmos
import scheduler.fcfs as FCFS
import scheduler.marina as MARINA
import scheduler.cratos as CRATOS
import scheduler.tovec as TOVEC
import scheduler.nancy as NANCY
import scheduler.vtc2022 as PARETO
import scheduler.marina_new as TITS
import scheduler.farima as FARIMA
import scheduler.farima_rp as NEW

# FARIMA'S PAPER
RSU_LIST = [2, 8, 9, 15, 16, 17, 22, 23, 24, 29, 30, 31, 36, 37, 38, 43, 44, 45]

class SchedulingManager:

	def __init__(self):
		self.escalonamento = {}
		# POPULA ESSA ESTRUTURA COM TODAS AS BS

		# bs_list = {4:'', 5:'', 10:'', 22:'', 99:'', 105:'', 114:'', 122:'', 180:'', 188:'', 190:'', 200:'', 238:'', 240:''}
		bs_list = {
			2:'',
			8:'',
			9:'',
			15:'',
			16:'',
			17:'',
			22:'',
			23:'',
			24:'',
			29:'',
			30:'',
			31:'',
			36:'',
			37:'',
			38:'',
			43:'',
			44:'',
			45:''
		}
		self.resource_usage = {}
		for i in bs_list:
			self.resource_usage[i] = {}
		
		self.resource_usage['remotecloud']  = {}
		self.resource_usage['masterfog']	= {}

	def insert(self, tasks, queue, clouds, algorithm, step):
		self.result = {}
		self.resource_now = {}

		# RETORNA NUVEM COM TAREFAS ESCALONADAS E SEUS TEMPOS DE PROCESSAMENTO
		# RETORNA UTILIZACAO DOS RECURSOS NA NUVEM
		initial_time = time.time()
		if algorithm == 'MARINA':
			self.result, self.resource_now = MARINA.run(queue, clouds, tasks)

		elif algorithm == 'FCFS':
			self.result, self.resource_now = FCFS.run(queue, clouds, tasks)

		elif algorithm == 'CRATOS':
			self.result, self.resource_now = CRATOS.run(queue, clouds, tasks)
		
		elif algorithm == 'TOVEC':
			self.result, self.resource_now = TOVEC.run(queue, clouds, tasks)

		elif algorithm == 'NANCY':
			self.result, self.resource_now = NANCY.run(queue, clouds, tasks)

		elif algorithm == 'PARETO':
			self.result, self.resource_now = PARETO.run(queue, clouds, tasks)

		elif algorithm == 'TITS':
			self.result, self.resource_now = TITS.run(queue, clouds, tasks)

		elif algorithm == 'FARIMA':
			self.result, self.resource_now = FARIMA.run(queue, clouds, tasks)

		elif algorithm == 'NEW':
			self.result, self.resource_now = NEW.run(queue, clouds, tasks)

		else:
			raise Exception("INVALID")
		
		final_time = time.time()
		log.log_time(float(final_time - initial_time))

		# TODO: 
		# - Verificar cada nuvem contida no self.result
		# - Verificar cada tarefa que foi adicionada na nuvem anterior
		# - Atualiza recursos na VC com base na utilização atual [OK, porém falta adicionar ao monitor]
		for id_cloud in self.resource_now:
			self.resource_usage[id_cloud].update(self.resource_now[id_cloud])
			
		print("Escalonamento:")
		# print(self.result)

		for cloud in self.result:
			
			cloud_cpu_load = 0

			for task in self.result[cloud]:
				
				print(" > Iniciando processamento da tarefa %s!" % task)

				self.task_id 											= task
				self.task_size											= queue.task_queue_control[self.task_id]['size']
				self.task_value											= queue.task_queue_control[self.task_id]['value']
				self.task_cpu 											= queue.task_queue_control[self.task_id]['cpu']
				self.task_deadline 										= queue.task_queue_control[self.task_id]['deadline']
				
				print(" * size: ",self.task_size)
				print(" * deadline: ",self.task_deadline)
				# ADICIONA TEMPO DE INICIO DO PROCESSAMENTO
				self.task_start_time 									= float(step) # time.time()
				queue.task_queue_control[self.task_id]['start_time'] 	= self.task_start_time
				queue.final_queue[self.task_id]['start_time']			= self.task_start_time

				# ADICIONA TEMPO ESTIMATIDO PARA CONCLUSAO DO PROCESSAMENTO
				self.task_finish_time									= step + self.result[cloud][self.task_id]
				queue.task_queue_control[self.task_id]['finish_time']	= self.task_finish_time
				queue.final_queue[self.task_id]['finish_time']			= self.task_finish_time

				print(" * finish_time: ",self.task_finish_time)
				
				# ATUALIZA STATUS
				self.task_status										= 'SUBMITTED'
				queue.task_queue_control[self.task_id]['status']	 	= self.task_status
				queue.final_queue[self.task_id]['status']				= self.task_status

				if cloud not in self.escalonamento:
					self.escalonamento[cloud] = {
						self.task_id:{
							'size':self.task_size,
							'value':self.task_value,
							'deadline':self.task_deadline,
							# 'insert_time':self.task_insert_time,
							'start_time':self.task_start_time,
							'finish_time':self.task_finish_time,
							'status':self.task_status
						}
					}
				else:
					self.escalonamento[cloud].update(
						{
							self.task_id:{
								'size':self.task_size,
								'value':self.task_value,
								'deadline':self.task_deadline,
								# 'insert_time':self.task_insert_time,
								'start_time':self.task_start_time,
								'finish_time':self.task_finish_time,
								'status':self.task_status
							}
						}
					)

				cloud_cpu_load += self.task_size


			# print("Split Resource:")
			# print(self.resource_usage[cloud])
			# ATUALIZA INFORMACOES DA NUVEM
			if cloud == 'remotecloud':
				clouds.update(cloud, self.resource_usage[cloud], 'add', 'remotecloud')
			elif cloud == 'masterfog':
				clouds.update(cloud, self.resource_usage[cloud], 'add', 'masterfog')
			else:
				clouds.update(cloud, self.resource_usage[cloud], 'add', 'vcs')

		# print("RemoteCloud:",clouds.remotecloud)
		# print("MasterFogNodes:",clouds.masterfognodes)

	# TODO:
	# * ATUALIZAR RECURSOS FUTUROS COM BASE NA UTILIZAÇÃO DAS NUVENS ATUAIS
	# * código base em: use_resource.py
	def update_vc_resources(self):

		return 0

	def get_scheduling(self):
		# retorna o status de execucao das tarefas
		print(" * ",self.escalonamento)
