#!/bin/bash

RESOURCES_VCS=2

TOTAL_SEEDS=5

TASK_RATE=$1

TASK_SIZE=10

CPU_CYCLE=10

START_TIME=1700
SIMULATION_TIME=2000

for (( i=1; i<=$TOTAL_SEEDS; i++ ))
do
	echo 'Rodando Seed' $i':'
	SEED_TASKS=$i

	# CRATOS
	# python3 run.py --scenario cologne --interval 5 --tasks 10 --begin $START_TIME --end $SIMULATION_TIME --radius 2000 --resources $RESOURCES_VCS --weight $TASK_SIZE --taskrate $TASK_RATE --cpucycle $CPU_CYCLE --algorithm CRATOS --seed_sumo 1 --seed_task $SEED_TASKS --deadline 1
	# python3 run.py --scenario cologne --interval 5 --tasks 10 --begin $START_TIME --end $SIMULATION_TIME --radius 2000 --resources $RESOURCES_VCS --weight $TASK_SIZE --taskrate $TASK_RATE --cpucycle $CPU_CYCLE --algorithm CRATOS --seed_sumo 1 --seed_task $SEED_TASKS --deadline 3
	# python3 run.py --scenario cologne --interval 5 --tasks 10 --begin $START_TIME --end $SIMULATION_TIME --radius 2000 --resources $RESOURCES_VCS --weight $TASK_SIZE --taskrate $TASK_RATE --cpucycle $CPU_CYCLE --algorithm CRATOS --seed_sumo 1 --seed_task $SEED_TASKS --deadline 5
	# # python3 run.py --scenario cologne --interval 5 --tasks 10 --begin $START_TIME --end $SIMULATION_TIME --radius 2000 --resources $RESOURCES_VCS --weight $TASK_SIZE --taskrate $TASK_RATE --cpucycle $CPU_CYCLE --algorithm CRATOS --seed_sumo 1 --seed_task $SEED_TASKS --deadline 7
	# python3 run.py --scenario cologne --interval 5 --tasks 10 --begin $START_TIME --end $SIMULATION_TIME --radius 2000 --resources $RESOURCES_VCS --weight $TASK_SIZE --taskrate $TASK_RATE --cpucycle $CPU_CYCLE --algorithm CRATOS --seed_sumo 1 --seed_task $SEED_TASKS --deadline 10
	# python3 run.py --scenario cologne --interval 5 --tasks 10 --begin $START_TIME --end $SIMULATION_TIME --radius 2000 --resources $RESOURCES_VCS --weight $TASK_SIZE --taskrate $TASK_RATE --cpucycle $CPU_CYCLE --algorithm CRATOS --seed_sumo 1 --seed_task $SEED_TASKS --deadline 15


	# # # FCFS
	# # python3 run.py --scenario cologne --interval 5 --tasks 10 --begin $START_TIME --end $SIMULATION_TIME --radius 2000 --resources $RESOURCES_VCS --weight $TASK_SIZE --taskrate $TASK_RATE --cpucycle $CPU_CYCLE --algorithm FCFS --seed_sumo 1 --seed_task $SEED_TASKS --deadline 1
	# python3 run.py --scenario cologne --interval 5 --tasks 10 --begin $START_TIME --end $SIMULATION_TIME --radius 2000 --resources $RESOURCES_VCS --weight $TASK_SIZE --taskrate $TASK_RATE --cpucycle $CPU_CYCLE --algorithm FCFS --seed_sumo 1 --seed_task $SEED_TASKS --deadline 3
	# python3 run.py --scenario cologne --interval 5 --tasks 10 --begin $START_TIME --end $SIMULATION_TIME --radius 2000 --resources $RESOURCES_VCS --weight $TASK_SIZE --taskrate $TASK_RATE --cpucycle $CPU_CYCLE --algorithm FCFS --seed_sumo 1 --seed_task $SEED_TASKS --deadline 5
	# # python3 run.py --scenario cologne --interval 5 --tasks 10 --begin $START_TIME --end $SIMULATION_TIME --radius 2000 --resources $RESOURCES_VCS --weight $TASK_SIZE --taskrate $TASK_RATE --cpucycle $CPU_CYCLE --algorithm FCFS --seed_sumo 1 --seed_task $SEED_TASKS --deadline 7
	# python3 run.py --scenario cologne --interval 5 --tasks 10 --begin $START_TIME --end $SIMULATION_TIME --radius 2000 --resources $RESOURCES_VCS --weight $TASK_SIZE --taskrate $TASK_RATE --cpucycle $CPU_CYCLE --algorithm FCFS --seed_sumo 1 --seed_task $SEED_TASKS --deadline 10
	# python3 run.py --scenario cologne --interval 5 --tasks 10 --begin $START_TIME --end $SIMULATION_TIME --radius 2000 --resources $RESOURCES_VCS --weight $TASK_SIZE --taskrate $TASK_RATE --cpucycle $CPU_CYCLE --algorithm FCFS --seed_sumo 1 --seed_task $SEED_TASKS --deadline 15
	
	# # FARIMA
	# # python3 run.py --scenario cologne --interval 5 --tasks 10 --begin $START_TIME --end $SIMULATION_TIME --radius 2000 --resources $RESOURCES_VCS --weight $TASK_SIZE --taskrate $TASK_RATE --cpucycle $CPU_CYCLE --algorithm FARIMA --seed_sumo 1 --seed_task $SEED_TASKS --deadline 1
	# python3 run.py --scenario cologne --interval 5 --tasks 10 --begin $START_TIME --end $SIMULATION_TIME --radius 2000 --resources $RESOURCES_VCS --weight $TASK_SIZE --taskrate $TASK_RATE --cpucycle $CPU_CYCLE --algorithm FARIMA --seed_sumo 1 --seed_task $SEED_TASKS --deadline 3
	# python3 run.py --scenario cologne --interval 5 --tasks 10 --begin $START_TIME --end $SIMULATION_TIME --radius 2000 --resources $RESOURCES_VCS --weight $TASK_SIZE --taskrate $TASK_RATE --cpucycle $CPU_CYCLE --algorithm FARIMA --seed_sumo 1 --seed_task $SEED_TASKS --deadline 5
	# # python3 run.py --scenario cologne --interval 5 --tasks 10 --begin $START_TIME --end $SIMULATION_TIME --radius 2000 --resources $RESOURCES_VCS --weight $TASK_SIZE --taskrate $TASK_RATE --cpucycle $CPU_CYCLE --algorithm FARIMA --seed_sumo 1 --seed_task $SEED_TASKS --deadline 7
	# python3 run.py --scenario cologne --interval 5 --tasks 10 --begin $START_TIME --end $SIMULATION_TIME --radius 2000 --resources $RESOURCES_VCS --weight $TASK_SIZE --taskrate $TASK_RATE --cpucycle $CPU_CYCLE --algorithm FARIMA --seed_sumo 1 --seed_task $SEED_TASKS --deadline 10
	# python3 run.py --scenario cologne --interval 5 --tasks 10 --begin $START_TIME --end $SIMULATION_TIME --radius 2000 --resources $RESOURCES_VCS --weight $TASK_SIZE --taskrate $TASK_RATE --cpucycle $CPU_CYCLE --algorithm FARIMA --seed_sumo 1 --seed_task $SEED_TASKS --deadline 15

	# # TOVEC
	# # python3 run.py --scenario cologne --interval 5 --tasks 10 --begin $START_TIME --end $SIMULATION_TIME --radius 2000 --resources $RESOURCES_VCS --weight $TASK_SIZE --taskrate $TASK_RATE --cpucycle $CPU_CYCLE --algorithm TOVEC --seed_sumo 1 --seed_task $SEED_TASKS --deadline 1
	# python3 run.py --scenario cologne --interval 5 --tasks 10 --begin $START_TIME --end $SIMULATION_TIME --radius 2000 --resources $RESOURCES_VCS --weight $TASK_SIZE --taskrate $TASK_RATE --cpucycle $CPU_CYCLE --algorithm TOVEC --seed_sumo 1 --seed_task $SEED_TASKS --deadline 3
	# python3 run.py --scenario cologne --interval 5 --tasks 10 --begin $START_TIME --end $SIMULATION_TIME --radius 2000 --resources $RESOURCES_VCS --weight $TASK_SIZE --taskrate $TASK_RATE --cpucycle $CPU_CYCLE --algorithm TOVEC --seed_sumo 1 --seed_task $SEED_TASKS --deadline 5
	# # python3 run.py --scenario cologne --interval 5 --tasks 10 --begin $START_TIME --end $SIMULATION_TIME --radius 2000 --resources $RESOURCES_VCS --weight $TASK_SIZE --taskrate $TASK_RATE --cpucycle $CPU_CYCLE --algorithm TOVEC --seed_sumo 1 --seed_task $SEED_TASKS --deadline 7
	# python3 run.py --scenario cologne --interval 5 --tasks 10 --begin $START_TIME --end $SIMULATION_TIME --radius 2000 --resources $RESOURCES_VCS --weight $TASK_SIZE --taskrate $TASK_RATE --cpucycle $CPU_CYCLE --algorithm TOVEC --seed_sumo 1 --seed_task $SEED_TASKS --deadline 10
	# python3 run.py --scenario cologne --interval 5 --tasks 10 --begin $START_TIME --end $SIMULATION_TIME --radius 2000 --resources $RESOURCES_VCS --weight $TASK_SIZE --taskrate $TASK_RATE --cpucycle $CPU_CYCLE --algorithm TOVEC --seed_sumo 1 --seed_task $SEED_TASKS --deadline 15

	# NEW
	# python3 run.py --scenario cologne --interval 5 --tasks 10 --begin $START_TIME --end $SIMULATION_TIME --radius 2000 --resources $RESOURCES_VCS --weight $TASK_SIZE --taskrate $TASK_RATE --cpucycle $CPU_CYCLE --algorithm NEW --seed_sumo 1 --seed_task $SEED_TASKS --deadline 1
	python3 run.py --scenario cologne --interval 5 --tasks 10 --begin $START_TIME --end $SIMULATION_TIME --radius 2000 --resources $RESOURCES_VCS --weight $TASK_SIZE --taskrate $TASK_RATE --cpucycle $CPU_CYCLE --algorithm NEW --seed_sumo 1 --seed_task $SEED_TASKS --deadline 3
	python3 run.py --scenario cologne --interval 5 --tasks 10 --begin $START_TIME --end $SIMULATION_TIME --radius 2000 --resources $RESOURCES_VCS --weight $TASK_SIZE --taskrate $TASK_RATE --cpucycle $CPU_CYCLE --algorithm NEW --seed_sumo 1 --seed_task $SEED_TASKS --deadline 5
	# python3 run.py --scenario cologne --interval 5 --tasks 10 --begin $START_TIME --end $SIMULATION_TIME --radius 2000 --resources $RESOURCES_VCS --weight $TASK_SIZE --taskrate $TASK_RATE --cpucycle $CPU_CYCLE --algorithm NEW --seed_sumo 1 --seed_task $SEED_TASKS --deadline 7
	python3 run.py --scenario cologne --interval 5 --tasks 10 --begin $START_TIME --end $SIMULATION_TIME --radius 2000 --resources $RESOURCES_VCS --weight $TASK_SIZE --taskrate $TASK_RATE --cpucycle $CPU_CYCLE --algorithm NEW --seed_sumo 1 --seed_task $SEED_TASKS --deadline 10
	python3 run.py --scenario cologne --interval 5 --tasks 10 --begin $START_TIME --end $SIMULATION_TIME --radius 2000 --resources $RESOURCES_VCS --weight $TASK_SIZE --taskrate $TASK_RATE --cpucycle $CPU_CYCLE --algorithm NEW --seed_sumo 1 --seed_task $SEED_TASKS --deadline 15


done