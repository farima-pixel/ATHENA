#!/bin/bash
# Autor: Joahannes B.D. da Costa <joahannes@lrc.ic.unicamp.br>
# Data: 13.07.2019
# Rodar: ./run.sh cenario intervalo_de_clusterizacao inicio final raio_comunicacao recursos peso_medio_tarefa info

CENARIO=$1
INTERVALO=$2
TAREFAS=$3
BEGIN=$4
END=$5
RAIO=$6
RESOURCE=$7
WEIGHT_TASK=$8
RATE=$9
MEGACYLES=${10}
ALGORITHM=${11}
SEED=${12}

if [ -z $CENARIO ] || [ -z $INTERVALO ] || [ -z $TAREFAS ] || [ -z $BEGIN ] || [ -z $END ] || [ -z $RAIO ] || [ -z $RESOURCE ] || [ -z $WEIGHT_TASK ] || [ -z $RATE ] || [ -z $MEGACYLES ] || [ -z $ALGORITHM ] || [ -z $SEED ]
then
	echo " >> Verifique os parametros: cenario intervalo_clusterizacao chegada_tarefas inicio fim raio recursos peso algoritmo seed"
elif [ $CENARIO == 'cologne' ]
then
	#===================================#
	#									#
	#			LUXEMBURGO				#
	#									#
	#===================================#
	echo 'Cenario:' $CENARIO
	echo 'Intervalo de formação de VCs:' $INTERVALO's'
	echo 'Intervalo de chegada de tarefas:' $TAREFAS's'
	echo 'Inicio em:' $BEGIN's'
	echo 'Final em:' $END's'
	echo 'Radio de:' $RAIO'm'
	echo 'Recurso por veiculo:' $RESOURCE
	echo 'Peso medio de cada tarefa:' $WEIGHT_TASK
	echo 'Taxa de chegada das tarefas (lambda):' $RATE
	echo 'Ciclo médio das tarefas (MI):' $MEGACYLES
	echo 'Algoritmo selecionado:' $ALGORITHM
	echo 'Semente de simulação:' $SEED
	python src/main.py -s scenario/cologne/cologne100.sumocfg -n scenario/cologne/cologne2.net.xml -i $INTERVALO -x $TAREFAS -b $BEGIN -e $END -o output/cologne-output.xml -l log/cologne-log.xml -m summary/cologne.summary.xml -t $RAIO -r $RESOURCE -w $WEIGHT_TASK -d $RATE -f $MEGACYLES -a $ALGORITHM -z $SEED
else
	echo ">> Cenario nao reconhecido!"
fi
