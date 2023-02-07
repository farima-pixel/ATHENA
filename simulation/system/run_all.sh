#!/bin/bash

OPCAO=$1

if [ $OPCAO == 'check' ]
then
    parallel -j2 --dryrun 'python run.py -a {1} -b {2} -c {3} -d {4} -e {5} -f {6} -g {7} -i {8} -j {9} -k {10} -l {11} -m {12}' ::: cologne ::: 10 ::: 10 ::: 20 ::: 30 ::: 999 ::: 1 ::: 10 ::: 1 ::: 10 ::: MARINA ::: 1 2 3 4
elif [ $OPCAO == 'bar' ]
then
    parallel -j2 --bar 'python run.py -a {1} -b {2} -c {3} -d {4} -e {5} -f {6} -g {7} -i {8} -j {9} -k {10} -l {11} -m {12}' ::: cologne ::: 10 ::: 10 ::: 20 ::: 30 ::: 999 ::: 1 ::: 10 ::: 1 ::: 10 ::: MARINA ::: 1 2 3 4
elif [ $OPCAO == 'run' ]
then
    parallel -j2 --bar 'python run.py -a {1} -b {2} -c {3} -d {4} -e {5} -f {6} -g {7} -i {8} -j {9} -k {10} -l {11} -m {12}' ::: cologne ::: 10 ::: 10 ::: 20 ::: 30 ::: 999 ::: 1 ::: 10 ::: 1 ::: 10 ::: MARINA ::: 1 2 3 4
else
    echo 'Opcao inválida!'
    echo 'Escola entre: check, bar e run'
fi