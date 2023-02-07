#!/usr/bin/python3
# title: priority_queue.py
# author: Joahannes Costa <joahannes@lrc.ic.unicamp.br
# date: 29.10.2021

from queue import PriorityQueue

import heapq
import time

class Priority():

	def __init__(self):
		# self.task_queue = PriorityQueue() # usa a lib queue
		self.task_queue = [] # usa a lib heapq
		self.task_queue_control = {}
		# UTILIZADA PARA O CONTROLE FINAL DE RESULTADOS
		self.final_queue = {} 

	def enqueue(self, task_id, tasks_set, step):

		self.insert_time = float(step) # time.time()
		print("Adicionando task %s aos %f s" % (task_id, self.insert_time))
		
		self.local_task								= {}
		self.local_task[task_id]					= {}
		self.local_task[task_id]['size']			= tasks_set[task_id]['size']
		self.local_task[task_id]['value']			= tasks_set[task_id]['value']
		self.local_task[task_id]['cpu']				= tasks_set[task_id]['cpu']
		self.local_task[task_id]['deadline']		= tasks_set[task_id]['deadline']
		self.local_task[task_id]['insert_time']		= self.insert_time
		self.local_task[task_id]['start_time']		= None # WHEN PROCESSING STARTS
		self.local_task[task_id]['finish_time']		= None # WHEN PROCESSING ENDS
		self.local_task[task_id]['remove_time']		= self.insert_time + tasks_set[task_id]['deadline'] # TODAS COMECAM NO PIOR CASO, PASSAR O PERIODO INTEIRO NA FILA
		self.local_task[task_id]['waiting_time']	= self.insert_time + tasks_set[task_id]['deadline']
		self.local_task[task_id]['cost']			= None
		self.local_task[task_id]['status']			= 'PENDING'

		self.job_priority = tasks_set[task_id]['deadline']
		# VERIFICAR COMPLEXIDADE DO HEAPPUSH PARA INSERIR NO PAPER
		heapq.heappush(self.task_queue, [self.job_priority, task_id])

		self.task_queue_control[task_id] = self.local_task[task_id]
		self.final_queue[task_id] = self.local_task[task_id].copy() # COPY PARA PRESERVAR OS VALORES INICIAIS

		# print(' * Deadline: %d' % (self.local_task[task_id]['deadline']))

	'''
	Atualiza deadline das tarefas enfileiradas e não escalonadas.
	'''
	def update(self, step, schedule):
		
		# print("FILA AGORA:",self.task_queue)
		# print("Fila antes:",self.task_queue)
		self.tarefas_deadline = []

		# DIMINUI DEADLINE EM 1 UNIDADE DE TEMPO
		# print("Atualizando dados da fila...")
		for task in range(len(self.task_queue)):
			# print('Antes:',self.task_queue[task])
			self.task_queue[task][0] -= 1
			# DEBUG: ATUALIZA DEADLINE NA FILA DE CONTROLE!
			self.task_queue_control[self.task_queue[task][1]]['deadline'] -= 1
			# print('Depois:',self.task_queue[task])

			# VERIFICA TAREFAS COM DEADLINE ESTOURADO
			if self.task_queue[task][0] <= 0:
				# print(" *** ESTOUROU DEADLINE!!!!")
				print(self.task_queue[task][1], "precisa ser removida da fila!")
				self.tarefas_deadline.append(self.task_queue[task])

		# REMOVE TAREFAS COM DEADLINE ESTOURADO
		if len(self.tarefas_deadline) > 0:
			# print("A SEREM REMOVIDAS:")
			# print(self.tarefas_deadline)
			for task in self.tarefas_deadline:
				id_tarefa = task[1]
				# MARCAR TAREFA COMO NEGADA
				# print(id_tarefa)
				self.task_queue_control[id_tarefa]['status'] = 'EXPIRED'
				self.final_queue[id_tarefa]['status'] = 'EXPIRED'

				remove_time = float(step)
				self.task_queue_control[id_tarefa]['remove_time'] = remove_time
				self.final_queue[id_tarefa]['remove_time'] = remove_time

				# REMOVE DO HEAP
				heapq.heappop(self.task_queue)

				# ATUALIZA NO ESCALONAMENTO A TAREFA QUE EXPIROU DEADLINE
				for expired in schedule.escalonamento:
					if id_tarefa in schedule.escalonamento[expired]:
						schedule.escalonamento[expired][id_tarefa]['status'] = 'EXPIRED'

		
		# HEAPFY NA FILA
		heapq.heapify(self.task_queue)
		# print("Fila depois:",self.task_queue)
		# print("FILA FINAL:")
		# for i in self.task_queue_control:
		#     print(i, self.task_queue_control[i]['status'])

	def get_queue(self):
		return self.task_queue

	def size_queue(self):
		return len(self.task_queue)

	def get_specific_item(self, id_item):
		print(self.task_queue_control[id_item])
