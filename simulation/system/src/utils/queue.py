#!/usr/bin/python3
# title: queue.py
# author: Joahannes Costa <joahannes@lrc.ic.unicamp.br
# date: 29.10.2021

class Queue():

	def __init__(self):
		self.task_queue = []
		self.task_queue_control = {}
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
		self.local_task[task_id]['start_time']		= None #TALVEZ NAO PRECISE
		self.local_task[task_id]['finish_time']		= None #TALVEZ NAO PRECISE
		self.local_task[task_id]['remove_time']		= self.insert_time + tasks_set[task_id]['deadline'] # TODAS COMECAM NO PIOR CASO, PASSAR O PERIODO INTEIRO NA FILA
		self.local_task[task_id]['waiting_time']	= self.insert_time + tasks_set[task_id]['deadline']
		self.local_task[task_id]['cost']			= None
		self.local_task[task_id]['status']			= 'PENDING'

		# FILA = [TAMANHO, DEADLINE, ID_TAREFA]
		self.task_queue.append([self.local_task[task_id]['size'], task_id])

		self.task_queue_control[task_id] = self.local_task[task_id]
		self.final_queue[task_id] = self.local_task[task_id].copy() # COPY PARA PRESERVAR OS VALORES INICIAIS

	def update(self, step, schedule):
		# print("UPDATE")
		self.tarefas_deadline = []
		for task in range(len(self.task_queue)):
			task_id = self.task_queue[task][1]
			self.task_queue_control[task_id]['deadline'] -= 1
			task_deadline = self.task_queue_control[task_id]['deadline']
			if task_deadline <= 0:
				print(task_id, "precisa ser removida da fila!")
				self.tarefas_deadline.append(self.task_queue[task])

		if len(self.tarefas_deadline) > 0:
			for task in self.tarefas_deadline:
				id_tarefa = task[1]
				self.task_queue_control[id_tarefa]['status'] = 'EXPIRED'
				self.final_queue[id_tarefa]['status'] = 'EXPIRED'

				remove_time = float(step)
				self.task_queue_control[id_tarefa]['remove_time'] = remove_time
				self.final_queue[id_tarefa]['remove_time'] = remove_time

				# REMOVE DA FILA
				self.task_queue.remove(task)

				# ATUALIZA NO ESCALONAMENTO A TAREFA QUE EXPIROU DEADLINE
				for expired in schedule.escalonamento:
					if id_tarefa in schedule.escalonamento[expired]:
						schedule.escalonamento[expired][id_tarefa]['status'] = 'EXPIRED'

	def get_queue(self):
		return self.task_queue
	
	def size_queue(self):
		return len(self.task_queue)