# -*- coding: utf-8 -*-
#!/usr/bin/env python
# title: main.py

from __future__ import division

import sys
import subprocess
import logging
import time
import numpy as np

import warnings
from optparse import OptionParser

from shapely.geometry import Point, Polygon

# Vehicular Cloud
import sumo_manager
import traci
import sumolib

import json

PATH = 'results/'
NETWORK = sumolib.net.readNet('scenario/porto.net.xml')

def run(network, begin, end, interval, seed_sumo):

	logging.debug("Building scenario")	
	logging.debug("Running simulation now")

	first_region = build_cells()

	# print(first_region[1])

	step = 1
	while step == 1 or traci.simulation.getMinExpectedNumber() > 0:

		logging.debug("Minimum expected number of vehicles: %d" % traci.simulation.getMinExpectedNumber())
		traci.simulationStep()
		logging.debug("Simulation time %d" % step)

		# print("Step %d" % step)
		# if interval == 1:
		# 	# timeseries(step)
		# 	pass

		if step >= begin:
			if step % interval == 0:
				# print("Running...")
				check_cells(step, first_region)
				# getVehicleData(step, interval)
		
		if step > end:
			break
		
		step += 1

	time.sleep(1)
	logging.debug("Simulation finished")
	print("\nSimulation finished\n")
	traci.close()
	sys.stdout.flush()
	time.sleep(1)
		
def start_simulation(sumo, scenario, network, begin, end, interval, output, summary, seed_sumo):
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
		run(network, begin, end, interval, seed_sumo)
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
	parser.add_option("-t", "--logfile", dest="logfile", default="output/sumo-launchd.log", help="log messages to logfile [default: %default]", metavar="FILE")
	parser.add_option("-i", "--summary", dest="summary", default="summary.xml", help="The XML file at which the summary output must be written [default: %default]", metavar="FILE")

	# sumo seed
	parser.add_option("-q", "--seed_sumo", dest="seed_sumo", default=1, help="Seed for SUMO [default: %default]", metavar="SEED-SUMO")

	(options, args) = parser.parse_args()
	
	logging.basicConfig(filename=options.logfile, level=logging.DEBUG)
	logging.debug("Logging to %s" % options.logfile)
	
	if args:
		logging.warning("Superfluous command line arguments: \"%s\"" % " ".join(args))

	start_simulation(options.command, options.scenario, options.network, options.begin, options.end, options.interval, options.output, options.summary, options.seed_sumo)

	global INTERVAL
	INTERVAL = options.interval

def getVehicleData(step, interval):

	vehicles = traci.vehicle.getIDList()

	for index in range(len(vehicles)):

		filename = open(PATH + 'vehicles/interval_' + str(interval) + '/' + str(vehicles[index]) + '.txt', 'a')

		sumo_position = traci.vehicle.getPosition(vehicles[index])
		real_position = NETWORK.convertXY2LonLat(sumo_position[0],sumo_position[1])
		speed		  = traci.vehicle.getSpeed(vehicles[index])
		edge_id		  = traci.vehicle.getRoadID(vehicles[index])
		lane_id		  = traci.vehicle.getLaneID(vehicles[index])
		route_id	  = traci.vehicle.getRouteID(vehicles[index])

		filename.write(
			str(step) + '\t' +
			str(sumo_position) + '\t' +
			str((real_position[1],real_position[0])) + '\t' +
			str(speed) + '\t' +
			str(edge_id) + '\t' +
			str(lane_id) + '\t' +
			str(route_id) + '\n'
			)
		filename.close()

def saveTime(before, after):
	filename_time = open(PATH + 'times/simulation_time_' + str(INTERVAL) + '.txt', 'w')
	filename_time.write(str(round((after - before), 3)))
	filename_time.close()
	print("Time:",round((after - before), 3))

def timeseries(step):
	vehicles = traci.vehicle.getIDList()
	filename_serie = open(PATH + '/timeseries.txt', 'a')
	filename_serie.write(str(step) + '\t' + str(len(vehicles)) + '\n')
	filename_serie.close()

def build_cells():
	cells = {}
	f = open('utils/cells.json')
	data = json.load(f)
	f.close()
	# build cells as polygons
	for cell in data:
		poly = Polygon(data[cell])
		cells[int(cell)] = poly

	return cells

def check_cells(step, cells):

	vehicles = traci.vehicle.getIDList()
	# print("Vehicles online:",len(vehicles))
	coverage = {}
	for cell in cells:
		counter = 0
		for index in range(len(vehicles)):
			point = Point(traci.vehicle.getPosition(vehicles[index]))
			# make point with car's position
			# if point within polygon
			if point.within(cells[cell]) == True:
				counter += 1
		coverage[cell] = counter

	# create a timeseries for each cell
	for cell in coverage:
		filename = open('output/data/cell_' + str(cell) + '.txt', 'a')
		filename.write(str(step) + '\t' + str(coverage[cell]) + '\n')
		filename.close()


if __name__ == "__main__":
	before = time.time()
	warnings.simplefilter("ignore")
	main()
	after = time.time()
	saveTime(before, after)