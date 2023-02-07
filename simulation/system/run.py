#!/usr/bin/python3
# title: run.py
# author: Joahannes Costa <joahannes@lrc.ic.unicamp.br
# date: 22.09.2021

import argparse
import sys
import os

parser = argparse.ArgumentParser(description='Simulator for Task Scheduling in Vehicular Edge Computing ')
parser.add_argument("-a", "--scenario", dest="scenario", help="", metavar="SCENARIO")
parser.add_argument("-b", "--interval", dest="interval", default=10, help="", metavar="INTERVAL")
parser.add_argument("-c", "--tasks", dest="tasks", default=1, help="", metavar="TASKS")
parser.add_argument("-d", "--begin", dest="begin", default=1, help="", metavar="BEGIN")
parser.add_argument("-e", "--end", dest="end", default=3600, help="", metavar="END")
parser.add_argument("-f", "--radius", dest="radius", default=2000, help="", metavar="RADIUS")
parser.add_argument("-g", "--resources", dest="resources", default=1, help="", metavar="RESOURCES")
parser.add_argument("-i", "--weight", dest="weight", default=10, help="", metavar="WEIGHT")
parser.add_argument("-j", "--taskrate", dest="taskrate", default=1, help="", metavar="RATE")
parser.add_argument("-k", "--cpucycle", dest="cpucycle", default=10, help="", metavar="CPU")
parser.add_argument("-l", "--algorithm", dest="algorithm", default="MARINA", help="", metavar="ALGORITHM")
parser.add_argument("-m", "--seed_sumo", dest="seed_sumo", default=1, help="", metavar="SEED_SUMO")
parser.add_argument("-n", "--seed_task", dest="seed_task", default=1, help="", metavar="SEED_TASK")
parser.add_argument("-o", "--deadline", dest="deadline", default=1, help="", metavar="DEADLINE")

options = parser.parse_args()

# if not len(sys.argv) > 0:
#     print("ERROR")
# else:
print("\n******************************")
print("Cenário:",options.scenario)
print("Intervalo:",options.interval)
print("Tasks:",options.tasks)
print("Inicio:",options.begin)
print("Final:",options.end)
print("Raio:",options.radius)
print("Recursos:",options.resources)
print("Peso:",options.weight)
print("Rate:",options.taskrate)
print("CPU:",options.cpucycle)
print("Algoritmo:",options.algorithm)
print("SeedSUMO:",options.seed_sumo)
print("SeedTask:",options.seed_task)
print("Deadline:",options.deadline)
print("******************************")

# LOG PARA CADA SIMULACAO
configuracao_atual = str(options.algorithm) + '_TASKS_' + str(options.tasks) + '_RESOURCES_' + str(options.resources) + '_SIZE_' + str(options.weight) + '_RATE_' + str(options.taskrate) + '_CPU_' + str(options.cpucycle) + '_DEADLINE_' + str(options.deadline) + '_SEED-SUMO_' + str(options.seed_sumo) + '_SEED-TASK_' + str(options.seed_task) + '.txt'

# REMOVE ARQUIVO JA CRIADO
if os.path.exists('log/'+configuracao_atual):
	os.system('rm log/' + configuracao_atual)

os.system('python src/main.py --scenario scenario/porto/porto.sumocfg --network scenario/porto/porto.net.xml --interval ' + str(options.interval) + ' --requests ' + str(options.tasks) + ' --begin ' + str(options.begin) + ' --end ' + str(options.end) + ' --output output/cologne-output.xml --logfile log/' + configuracao_atual + ' --summary summary/cologne.summary.xml --radius ' + str(options.radius) + ' --resource ' + str(options.resources) + ' --weight ' + str(options.weight) + ' --rate ' + str(options.taskrate) + ' --megacycles ' + str(options.cpucycle) + ' --algorithm ' + str(options.algorithm) + ' --seed_sumo ' + str(options.seed_sumo) + ' --seed_task ' + str(options.seed_task) + ' --deadline ' + str(options.deadline))

# parallel -j2 'python run.py -a {1} -b {2} -c {3} -d {4} -e {5} -f {6} -g {7} -i {8} -j {9} -k {10} -l {11} -m {12}' ::: cologne ::: 10 ::: 10 ::: 20 ::: 30 ::: 999 ::: 1 ::: 10 ::: 1 ::: 10 ::: MARINA ::: 1 2

# testes
# python run.py --scenario cologne --interval 10 --tasks 10 --begin 20 --end 30 --radius 999 --resources 1 --weight 10 --taskrate 1 --cpucycle 10 --algorithm MARINA --seed 1