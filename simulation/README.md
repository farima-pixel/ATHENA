# VEC - Vehicular Edge Computing in Python

Mobility-aware Task Scheduling Mechanism for Vehicular Cloud Environments

### RUN:

> python run.py --scenario cologne --interval 10 --tasks 10 --begin 20 --end 30 --radius 2000 --resources 1 --weight 10 --taskrate 1 --cpucycle 10 --algorithm MARINA --seed_sumo 1 --seed_tasks 1

### Run in GNU Parallel:

> parallel -j2 'python run.py --scenario {1} --interval {2} --tasks {3} --begin {4} --end {5} --radius {6} --resources {7} --weight {8} --taskrate {9} --cpucycle {10} --algorithm {11} --seed {12}' ::: cologne ::: 10 ::: 10 ::: 20 ::: 30 ::: 2000 ::: 1 ::: 10 ::: 1 ::: 10 ::: MARINA UNC ::: 1 2

### Assessment:

* Tarefas alocadas (%)
* Custo de utilização dos recursos ($)
* Utilização dos recursos (s ou #)
* Tempo de CPU (s)
* Delay de computação (s)

### Parametrização:

* Intervalo de clusterização = [10, 15, 20, 25, 30]
* Cores de CPU nos veículos = [1, 2, 4, 8]
* Peso médio das tarefas = [1, 5, 10, 15, 20, 25, 30]
* Taxa de chegada de tarefas = [1, 2, 3, 4, 5]
* Ciclos de CPU necessário nas tarefas = [10, 20, 30]

### Ideias futuras:

* Criar GRAFO para o backhaul
* Selecionar veículo para requisição de tarefas
* Tarefa com a locaização do veículo
* Requisição vai para RSU mais próxima
* _k-shortest path_ entre RSU, com link entre RSU tendo o peso da distância entre elas

### Requisitos:

- Python 3.8.10
- SUMO >= 1.11.0
- sudo apt install python-tk
- sudo apt install parallel

### Uso:

- python3 -m venv venv/
- source virtualenv.sh init
- pip install --user -r requirements.txt
- source virtualenv.sh close

### Observações:

 - Alterar variável `path` em system/src/utils/globals.py
 - 
