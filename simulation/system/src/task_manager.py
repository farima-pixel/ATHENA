#!/usr/bin/env python
# title: task_manager.py
# author: Joahannes Costa <joahannes@lrc.ic.unicamp.br>
# date: 30.03.2021

import utils.globals as GLOBAL

class Task():

	def __init__(self):
		self.task_set = {}
		self.task_set_control = {}
		self.tasks_number = []

	def number_of_tasks(self, rate, seed):
		print("Carregando numero de tarefas...")
		# formato arquivo -> task_seed_2_rate_5
		self.number_tasks_file = GLOBAL.path + 'input/tasks/task_seed_' + str(seed) + '_rate_'  + str(rate) + '.txt'
		cont = 0
		for i in open(self.number_tasks_file):
			self.tasks_number.append([cont, int(i.split()[0])])
			cont += 1
	
	def load_task_file(self, size_n, cycles_n, seed_n, deadline_n):
		print("Carregando tarefas...")
		self.tasks_file = GLOBAL.path + 'input/tasks/deadline/' + str(deadline_n) + '/TASKS_SIZE_' + str(size_n) + '_CPU_' + str(cycles_n) + '_SEED_' + str(seed_n) + '.txt'
		for i in open(self.tasks_file):
			self.task_set[i.split()[0]]				= {}
			self.task_set[i.split()[0]]['size']		= int(i.split()[1])
			self.task_set[i.split()[0]]['value']	= int(i.split()[2])
			self.task_set[i.split()[0]]['cpu']		= int(i.split()[3])
			self.task_set[i.split()[0]]['deadline'] = int(i.split()[4])

			self.task_set_control[i.split()[0]]				= {}
			self.task_set_control[i.split()[0]]['size']		= int(i.split()[1])
			self.task_set_control[i.split()[0]]['value']	= int(i.split()[2])
			self.task_set_control[i.split()[0]]['cpu']		= int(i.split()[3])
			self.task_set_control[i.split()[0]]['deadline'] = int(i.split()[4])

	def get_task(self, task_id, field):
		print(self.task_set_control[task_id])
		return self.task_set_control[task_id][field]

'''
USAR CASO ALGUM ERRO OCORRA COM NOVA VERSAO!
'''
class OldTask():

	def load_number_of_tasks(rate, seed):

		print("Carregando número de tarefas...")

		# task_seed_2_rate_5
		tasks_file = 'input/tasks/task_seed_' + str(seed) + '_rate_'  + str(rate) + '.txt'
		tasks_set_number = []

		for i in open(tasks_file):
			tasks_set_number.append(int(i.split()[0]))

		return tasks_set_number

	def load_task_file(size_n, cycles_n, seed_n):
		print("Carregando tarefas...")
		# TASKS_SIZE_10_CPU_30_SEED_4
		task_file = 'input/tasks/TASKS_SIZE_' + str(size_n) + '_CPU_' + str(cycles_n) + '_SEED_' + str(seed_n) + '.txt'
		task_set = []

		for i in open(task_file):
			# print(i.split())
			# tarefa = [id, peso(Mb), valor($), ciclos(MHz), deadline(s)]
			# id-00000	1	2	9	9
			# print(i.split())
			# old
			task_set.append([i.split()[0], int(i.split()[1]), int(i.split()[2]), int(i.split()[3]), int(i.split()[4])])

		return task_set