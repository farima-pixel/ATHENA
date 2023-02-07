# -*- coding: utf-8 -*-
#!/usr/bin/env python
# title: main.py
# author: Joahannes Costa <joahannes@lrc.ic.unicamp.br>
# date: 02.03.2021

from __future__ import division

import sys
import subprocess
import logging
import time
import numpy as np

import warnings
from optparse import OptionParser

# Vehicular Cloud
import sumo_manager
import log_manager
import traci

import utils.globals as GLOBAL

# cont = 0
# for i in sys.argv:
# 	print(i, cont)
# 	cont += 1

# NEW IMPORTS
if sys.argv[30] == "MARINA":
	from utils.priority_queue import Priority
	queue = Priority()
else:
	from utils.queue import Queue
	queue = Queue()

from task_manager import Task
tasks = Task()

from cluster_manager import Clouds
clouds = Clouds()

from scheduling_manager import SchedulingManager
schedule = SchedulingManager()

from monitor import SchedulingMonitor
monitor = SchedulingMonitor()

def clustering(step, radius, resource):
	clouds.build_vehicular_clouds(step, resource, schedule)

def run_scheduling(step, algorithm):
	schedule.insert(tasks, queue, clouds, algorithm, step)

def run(network, begin, end, interval, requests, radius, resource, weight, rate, megacycles, algorithm, seed_sumo, seed_task, deadline):

	logging.debug("Building scenario")	
	logging.debug("Running simulation now")
	logging.debug("Algorithm -> " + algorithm)
	logging.debug("Generating tasks")

	# LOG
	log_manager.get_information(radius, resource, weight, rate, megacycles, algorithm, seed_task, deadline)
	
	# CARREGA DISTRIBUICAO DE POISSON & CRIA CONJUNTO DE TAREFAS
	tasks.number_of_tasks(rate, seed_task)
	tasks.load_task_file(weight, megacycles, seed_task, deadline)

	# interval in seconds
	logging.debug("Clustering interval: %d" % interval)
	logging.debug("Tasks interval: %d" % requests)

	# contabiliza total de tarefas no sistema
	total_tasks = 0

	# CARREGA ARQUIVO DE BS
	# clouds.get_rsu_positions_list()

	seed_sumo = seed_sumo

	# INICIO DA SIMULACAO
	step = 1
	while step == 1 or traci.simulation.getMinExpectedNumber() > 0:

		logging.debug("Minimum expected number of vehicles: %d" % traci.simulation.getMinExpectedNumber())
		traci.simulationStep()
		logging.debug("Simulation time %d" % step)

		print("Step %d" % step)

		if step >= begin:

			monitor.get_status(step, schedule, tasks, clouds, queue)

			if step % interval == 0:

				logging.debug("Formando Nuvens Veiculares no step %d" % step)
				clustering(step, radius, resource)

			tasks_now = tasks.tasks_number.pop(0)
			# print("task now",tasks_now[1])
			total_tasks = total_tasks + tasks_now[1]

			logging.debug("Numero de tarefa de chegou agora: %d" % tasks_now[1])
			# print("Numero de tarefa de chegou agora %d" % tasks_now)

			# SE CHEGOU TAREFA NO INSTANTE ATUAL
			if tasks_now[1] > 0:

				internal_control = 0
				temp = []
				for i in tasks.task_set:
					if internal_control != tasks_now[1]:
						logging.debug("Adicionando tarefa %s ao sistema" % i)
						# print("Adicionando tarefa %s ao sistema" % i)
						queue.enqueue(i, tasks.task_set, step)
						temp.append(i)
						internal_control += 1
					else:
						break
									
				# REMOVE TAREFAS DO CONJUNTO INICIAL
				for i in temp:
					logging.debug("Removendo tarefa %s do conjunto inicial de tarefas" % i)
					# print("Removendo tarefa %s do conjunto inicial de tarefas" % x)
					del tasks.task_set[i]	

			# VERIFICA FILA DE ESPERA
			if len(queue.get_queue()) > 0:
				# pass
				run_scheduling(step, algorithm)

			print()
		
		# TERMINA SIMULACAO
		if step > end:
			break
		
		# INCREMENTA UNIDADE DE TEMPO DA SIMULACAO
		step += 1

	# finaliza dicionario de tempos de fila
	# if len(fila) > 0:
	# 	for i in fila:
	# 		tempoRemocao[i[0]] = step

	# log_manager.log_allocation(step, len(tempoInsercao), allocation_manager.tempo_alloc)
	# log_manager.log_time(step, algorithm, tempoInsercao, tempoRemocao)

	print("\n* Total de tarefas inseridas no sistema:",total_tasks)
	logging.debug("* Total de tarefas inseridas no sistema %d " % total_tasks)

	# TODO: ADICIONAR TAREFAS EXPIRADAS E CONCLUIDAS COM SUCESSO

	# print("Controle final de tarefas:")
	# for i in queue.final_queue:
	# 	print(i, queue.final_queue[i])

	# log_manager.log_results(queue.final_queue)
	log_manager.log_results_final(queue.final_queue)

	# CONTROLE FINAL DE SIMULACAO
	time.sleep(1)
	logging.debug("Simulation finished")
	print("\nSimulation finished\n")
	traci.close()
	sys.stdout.flush()
	time.sleep(1)
		
def start_simulation(sumo, scenario, network, begin, end, interval, requests, output, summary, radius, resource, weight, rate, megacycles, algorithm, seed_sumo, seed_task, deadline):
	logging.debug("Finding unused port")
	
	unused_port_lock = sumo_manager.UnusedPortLock()
	unused_port_lock.__enter__()
	remote_port = sumo_manager.find_unused_port()

	logging.debug("Port %d was found" % remote_port)
	
	logging.debug("Starting SUMO as a server")
	
	sumo = subprocess.Popen([sumo, "-c", scenario, "--seed", seed_sumo, "-W", "--tripinfo-output", output, "--device.emissions.probability", "1.0", "--summary-output", summary ,"--remote-port", str(remote_port)], stdout=sys.stdout, stderr=sys.stderr)    
	
	unused_port_lock.release()
	
	try:
		traci.init(remote_port)
		run(network, begin, end, interval, requests, radius, resource, weight, rate, megacycles, algorithm, seed_sumo, seed_task, deadline)
	except:
		logging.exception("Something bad happened")
	finally:
		logging.exception("Terminating SUMO")  
		sumo_manager.terminate_sumo(sumo)
		unused_port_lock.__exit__()
		
def main():
	# Option handling
	parser = OptionParser()
	parser.add_option("-a", "--command", dest="command", default="sumo", help="The command used to run SUMO [default: %default]", metavar="COMMAND")
	parser.add_option("-b", "--scenario", dest="scenario", default="cologne.sumo.cfg", help="A SUMO configuration file [default: %default]", metavar="FILE")
	parser.add_option("-c", "--network", dest="network", default="network.net.xml", help="A SUMO network definition file [default: %default]", metavar="FILE")    
	parser.add_option("-d", "--begin", dest="begin", type="int", default=0, action="store", help="The simulation time (s) at which the re-routing begins [default: %default]", metavar="BEGIN")
	parser.add_option("-e", "--end", dest="end", type="int", default=10800, action="store", help="The simulation time (s) at which the re-routing ends [default: %default]", metavar="END")
	parser.add_option("-f", "--interval", dest="interval", type="int", default=10, action="store", help="The interval (s) of clustering [default: %default]", metavar="INTERVAL")
	parser.add_option("-g", "--output", dest="output", default="reroute.xml", help="The XML file at which the output must be written [default: %default]", metavar="FILE")
	parser.add_option("-t", "--logfile", dest="logfile", default="sumo-launchd.log", help="log messages to logfile [default: %default]", metavar="FILE")
	parser.add_option("-i", "--summary", dest="summary", default="summary.xml", help="The XML file at which the summary output must be written [default: %default]", metavar="FILE")
	
	# for Vehicular Cloud Environments
	parser.add_option("-j", "--radius", dest="radius", type="int", default=100, action="store", help="Transmission range [default: %default]", metavar="RADIUS")
	parser.add_option("-k", "--resource", dest="resource", type="int", default=1, action="store", help="Resource for each vehicle [default: %default]", metavar="RESOURCE")
	parser.add_option("-l", "--weight", dest="weight", type="int", default=1, action="store", help="Avg weight for each task [default: %default]", metavar="WEIGHT")
	parser.add_option("-m", "--requests", dest="requests", type="int", default=15, action="store", help="The interval (s) of tasks arrival [default: %default]", metavar="REQUESTS")
	parser.add_option("-n", "--rate", dest="rate", type="int", default=10, action="store", help="The interval (s) of tasks arrival [default: %default]", metavar="RATE")
	parser.add_option("-o", "--megacycles", dest="megacycles", type="int", default=10, action="store", help="The interval (s) of tasks arrival [default: %default]", metavar="MEGACYCLES")
	parser.add_option("-p", "--algorithm", dest="algorithm", default="MARINA", help="Algorithm for task scheduling [default: %default]", metavar="ALGORITHM")

	# sumo seed
	parser.add_option("-q", "--seed_sumo", dest="seed_sumo", default=1, help="Seed for SUMO [default: %default]", metavar="SEED-SUMO")
	# task seed
	parser.add_option("-r", "--seed_task", dest="seed_task", default=1, help="Seed for task scheduling [default: %default]", metavar="SEED-TASK")
	# deadline
	parser.add_option("-s", "--deadline", dest="deadline", default=1, help="Deadline for task scheduling [default: %default]", metavar="DEADLINE")

	(options, args) = parser.parse_args()
	
	logging.basicConfig(filename=options.logfile, level=logging.DEBUG)
	logging.debug("Logging to %s" % options.logfile)
	
	if args:
		logging.warning("Superfluous command line arguments: \"%s\"" % " ".join(args))

	start_simulation(options.command, options.scenario, options.network, options.begin, options.end, options.interval, options.requests, options.output, options.summary, options.radius, options.resource, options.weight, options.rate, options.megacycles, options.algorithm, options.seed_sumo, options.seed_task, options.deadline)

if __name__ == "__main__":
	warnings.simplefilter("ignore")
	main()