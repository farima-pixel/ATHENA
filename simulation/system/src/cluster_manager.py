#!/usr/bin/env python
# title: cluster_manager.py
# author: Joahannes Costa <joahannes@lrc.ic.unicamp.br>
# date: 30.03.2021

import numpy as np

import log_manager
import traci

import math
from scipy.spatial import distance

import utils.globals as GLOBAL

# CONSTANTS
RSU_FILE 			= GLOBAL.path + 'src/new_rsu_centro.txt'
BS_CPU 				= 20
BS_MEMORY			= 20
PREDICTION_WINDOW 	= 5

NUMBER_MASTER_FOGS  = 7
CPU_MFN				= 10
CPU_RC				= 150

# EXPERIMENTS 		= 'mobility'
EXPERIMENTS 		= 'temp'
BS_FILE				= GLOBAL.path + 'input/' + EXPERIMENTS + '/new/'

# FARIMA'S PAPER
# RSU_LIST = [2, 8, 9, 15, 16, 17, 22, 23, 24, 29, 30, 31, 36, 37, 38, 43, 44, 45]

class Clouds():

	def __init__(self):
		self.clouds = {}
		self.remotecloud = {}
		self.masterfognodes = {}

	def add(self, cloud_id, members, v_cpu, v_memory, bs_cpu, bs_memory, mips_future):

		self.id					= cloud_id
		self.members			= members
		self.v_cpu 				= v_cpu
		self.v_memory			= v_memory
		self.bs_cpu 			= bs_cpu
		self.bs_memory			= bs_memory
		self.mips				= self.v_cpu + self.bs_cpu
		self.prediction			= mips_future # FOR PREDICTION
		self.clouds[self.id] 	= {
			'members':self.members,
			'vehicle_cpu':self.v_cpu,
			# 'vehicle_memory':self.v_memory,
			'bs_cpu':self.bs_cpu,
			# 'bs_memory':self.bs_memory,
			'mips':self.mips,
			'prediction':self.prediction
		}

	def vc_update(self, cloud_id, members, v_cpu, v_memory, bs_cpu, bs_memory, mips_future):
		
		self.id					= cloud_id
		self.members			= members
		self.v_cpu 				= v_cpu
		self.v_memory			= v_memory
		self.bs_cpu 			= bs_cpu
		self.bs_memory			= bs_memory
		self.mips				= self.v_cpu + self.bs_cpu
		self.prediction			= mips_future # FOR PREDICTION

		self.clouds[self.id].update({'members':self.members})
		self.clouds[self.id].update({'vehicle_cpu':self.v_cpu})
		# self.clouds[cloud_id].update({'v_memory':v_memory})
		self.clouds[self.id].update({'bs_cpu':self.bs_cpu})
		# self.clouds[cloud_id].update({'bs_memory':bs_memory})
		self.clouds[self.id].update({'mips':self.mips})
		self.clouds[self.id].update({'prediction':self.prediction})

	def update(self, cloud_id, usage, update_type, cloud_type):
		
		self.cloud_id = cloud_id
		self.cpu_usage = 0
		self.usage = usage

		if cloud_type == 'remotecloud':

			if update_type == 'add':
				for i in self.usage:
					self.cpu_usage += self.usage[i]['rc']
					self.remotecloud[0]['cpu'] -= self.usage[i]['rc'] 
				self.remotecloud[0]['mips'] -= self.cpu_usage

			elif update_type == 'complete':
				self.cpu_usage += self.usage['rc']
				self.remotecloud[0]['cpu'] += self.usage['rc'] 
				self.remotecloud[0]['mips'] += self.cpu_usage

			else:
				print("INVALID!")

		elif cloud_type == 'masterfog':

			if update_type == 'add':
				for i in self.usage:
					self.cpu_usage += self.usage[i]['mfn']
					self.masterfognodes[0]['cpu'] -= self.usage[i]['mfn'] 
				self.masterfognodes[0]['mips'] -= self.cpu_usage

			elif update_type == 'complete':
				self.cpu_usage += self.usage['mfn']
				self.masterfognodes[0]['cpu'] += self.usage['mfn'] 
				self.masterfognodes[0]['mips'] += self.cpu_usage

			else:
				print("INVALID!")

		elif cloud_type == 'vcs':
			if update_type == 'add':
				for i in self.usage:
					self.cpu_usage += (self.usage[i]['vehicle'] + self.usage[i]['bs'])
					self.clouds[self.cloud_id]['vehicle_cpu'] -= self.usage[i]['vehicle']
					self.clouds[self.cloud_id]['bs_cpu'] -= self.usage[i]['bs']
				
				self.clouds[self.cloud_id]['mips'] -= self.cpu_usage

			elif update_type == 'complete':
				self.cpu_usage += (self.usage['vehicle'] + self.usage['bs'])
				self.clouds[self.cloud_id]['vehicle_cpu'] += self.usage['vehicle']
				self.clouds[self.cloud_id]['bs_cpu'] += self.usage['bs']
				self.clouds[self.cloud_id]['mips'] += self.cpu_usage

			else:
				print("INVALID!")

		else:
			print("CLOUD TYPE INVALID!")

	def print_vehicles(self):
		print(self.vehicles)

	def build_vehicular_clouds(self, step, resources, schedule):
		"Build vehicular clouds base on dataset."

		self.resources = resources

		# TODO: ALTERAR ESTRTURA PARA DICIONARIO INDICANDO O STEP
		# PARA AUXILIAR MONITOR DE RECURSOS *ATUAL* VS *PREDITO* PARA ATUALIZAR USO PELOS ALGORITMOS EM TEMPO REAL

		prediction_window = [(x+step) for x in range(PREDICTION_WINDOW+1)]
		print(prediction_window)
		# [t, t+1, t+2, ..., t+PREDICTION_WINDOW]
		# {t:value_t, t+1:value_t+1, t+2:value_t+2, ..., t+PREDICTION_WINDOW: value_PREDICTION_WINDOW}
		bs_file = open(RSU_FILE,'r')
		# first time
		print("DEBUG")
		if len(self.clouds) == 0:
			for bs in bs_file:
				print(bs)
				self.predictions = []
				bs = bs.split()
				id_bs = int(bs[0])

				# current value
				self.clouds[id_bs] = {}

				if id_bs < 10:
					mobility_data = open(BS_FILE + '0' + str(id_bs) + '.txt', 'r')
				else:
					mobility_data = open(BS_FILE + str(id_bs) + '.txt', 'r')
				with mobility_data as f:
					lines = f.readlines()
				
				cont_control = 0
				for i in lines:
					# print(i.split())
					if int(i.split()[0]) in prediction_window:
						self.predictions.append(int(i.split()[1]) * self.resources)
						cont_control += 1
						# break for loop to reduce computing time
						if cont_control == PREDICTION_WINDOW+1:
							break
				
				# example
				# predictions = [1, 2, 3, 4, 5, 6]
				# predictions[0] = 1
				self.members = self.predictions[0]
				self.v_cpu = self.members * self.resources

				# example
				# predictions[1:6] = [2, 3, 4, 5, 6]
				# resource_prediction = [(2+BS_CPU), (3+BS_CPU), (4+BS_CPU), (5+BS_CPU), (6+BS_CPU)]
				self.resource_prediction = [(mips + BS_CPU) for mips in self.predictions[1:PREDICTION_WINDOW+1]]
				self.add(id_bs, self.members, self.v_cpu, self.v_cpu, BS_CPU, BS_MEMORY, self.resource_prediction)
		else:

			# VERIFICA RECURSOS JA EM USO E CONSIDERA O VALOR NA ATUALIZACAO ATUAL
			# print(" >>>>>>> SITUACAO")
			# # schedule.get_scheduling()
			# print(schedule.resource_usage)

			self.discount = {}
			for current_proc in schedule.resource_usage:
				self.discount[current_proc] = {}
				self.discount[current_proc]['vehicle'] = 0
				self.discount[current_proc]['bs'] = 0
				if len(schedule.resource_usage[current_proc]) > 0:
					for each_task in schedule.resource_usage[current_proc]:
						if 'vehicle' in schedule.resource_usage[current_proc][each_task].keys():
							self.discount[current_proc]['vehicle'] += schedule.resource_usage[current_proc][each_task]['vehicle']
							self.discount[current_proc]['bs'] += schedule.resource_usage[current_proc][each_task]['bs']
				# print(current_proc)

			# print("TOTAL DE DESCONTOS:")
			# print(self.discount)

			for bs in bs_file:
				self.predictions = []
				bs = bs.split()
				id_bs = int(bs[0])

				if id_bs < 10:
					mobility_data = open(BS_FILE + '0' + str(id_bs) + '.txt', 'r')
				else:
					mobility_data = open(BS_FILE + str(id_bs) + '.txt', 'r')
				with mobility_data as f:
					lines = f.readlines()
				
				cont_control = 0
				for i in lines:
					if int(i.split()[0]) in prediction_window:
						self.predictions.append(int(i.split()[1]) * self.resources)
						cont_control += 1
						# break for loop to reduce computing time
						if cont_control == PREDICTION_WINDOW+1:
							break

				self.members = self.predictions[0]
				self.v_cpu = (self.members * self.resources) - (self.discount[id_bs]['vehicle'])
				self.bs_cpu = BS_CPU - self.discount[id_bs]['bs']
				# mips = v_cpu + BS_CPU
				self.resource_prediction = [(mips + BS_CPU) for mips in self.predictions[1:PREDICTION_WINDOW+1]]
				self.vc_update(id_bs, self.members, self.v_cpu, self.v_cpu, self.bs_cpu, BS_MEMORY, self.resource_prediction)
		
		# REMOTE CLOUD
		if len(self.remotecloud) == 0:
			self.remotecloud[0] = {
				'size':CPU_RC,
				'cpu':CPU_RC,
				'mips':CPU_RC
			}
		else:
			self.discount = {}
			for current_proc in schedule.resource_usage:
				self.discount['rc'] = 0
				if len(schedule.resource_usage[current_proc]) > 0:
					for each_task in schedule.resource_usage[current_proc]:
						if 'rc' in schedule.resource_usage[current_proc][each_task].keys():
							self.discount['rc'] += schedule.resource_usage[current_proc][each_task]['rc']

			self.cpu = (CPU_RC * self.resources) - (self.discount['rc'])
			self.remotecloud[0].update({'size':self.cpu})
			self.remotecloud[0].update({'cpu':self.cpu})
			self.remotecloud[0].update({'mips':self.cpu})
		
		# MASTER FOG NODES
		if len(self.masterfognodes) == 0:
			self.masterfognodes[0] = {
				'size':NUMBER_MASTER_FOGS * CPU_MFN,
				'cpu':NUMBER_MASTER_FOGS * CPU_MFN,
				'mips':NUMBER_MASTER_FOGS * CPU_MFN
			}
		else:
			self.discount = {}
			for current_proc in schedule.resource_usage:
				self.discount['mfn'] = 0
				if len(schedule.resource_usage[current_proc]) > 0:
					for each_task in schedule.resource_usage[current_proc]:
						if 'mfn' in schedule.resource_usage[current_proc][each_task].keys():
							self.discount['mfn'] += schedule.resource_usage[current_proc][each_task]['mfn']
			
			self.cpu = ((NUMBER_MASTER_FOGS * CPU_MFN) * self.resources) - (self.discount['mfn'])
			self.masterfognodes[0].update({'size':self.cpu})
			self.masterfognodes[0].update({'cpu':self.cpu})
			self.masterfognodes[0].update({'mips':self.cpu})
		# print("CLOUDS")
		# for i in self.clouds:
		# 	print(i, self.clouds[i])

		# schedule.get_scheduling()