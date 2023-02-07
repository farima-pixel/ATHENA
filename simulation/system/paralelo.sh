#!/bin/bash

CORES=$1
INICIO=$2
FINAL=$3
ALGORITMOS="MARINA CRATOS FIFO UNC AHP PSO"

echo "VEC Simulation"
echo "* Inicio: $INICIO"
echo "* Final: $FINAL"
echo "* Numero de cores usados: $CORES"
echo "* Algoritmos: $ALGORITMOS"

parallel -j $CORES ./run.sh cologne 10 10 $INICIO $FINAL 999 ::: {1,2,3,4} ::: {10,15,20,25,30} ::: {1,2,3,4,5} ::: {10,20,30} ::: $ALGORITMOS ::: {1,2,3,4,5}