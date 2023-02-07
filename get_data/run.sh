#!/bin/bash

# + 100

# LIMIT=2398180
# 1003110 - 2000 seconds
# 1003110 + 2000 seconds
BEGIN=1001110
LIMIT=1005110

# python3 main.py --scenario scenario/porto.sumocfg --network scenario/porto.net.xml --interval 1 --begin 0 --end $LIMIT --output output.xml --summary summary.xml --seed_sumo 1
# python3 main.py --scenario scenario/porto.sumocfg --network scenario/porto.net.xml --interval 5 --begin 0 --end $LIMIT --output output.xml --summary summary.xml --seed_sumo 1
# python3 main.py --scenario scenario/porto.sumocfg --network scenario/porto.net.xml --interval 10 --begin 0 --end $LIMIT --output output.xml --summary summary.xml --seed_sumo 1
python3 main.py --scenario scenario/porto.sumocfg --network scenario/porto.net.xml --interval 1 --begin $BEGIN --end $LIMIT --output output/output.xml --summary output/summary.xml --seed_sumo 1