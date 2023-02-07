#import benchmarks as bench
import random
import numpy

sw = 0 #soma de resursos

#nao estou usando
def euclidiana(y,z):
	# x, y, z = C, XP, X
	return (numpy.sqrt(sum((y - z) ** 2))) #distancia euclidiana

def update_Coeficientes(a):
	
	r1 = random.randrange(0,11)/10
	r2 = random.randrange(0,11)/10
	C = 2*r2
	A = 2*a*r1-a
	
	return A,C

def F5(x):
	dim  = len(x)
	o = numpy.sum(100*(x[1:dim]-(x[0:dim-1]**2))**2+(x[0:dim-1]-1)**2)
	return o;

def F6(x):
	o=numpy.sum(abs((x+.5))**2);
	return o;

def gwo_solution(sw, tasks):

	# tranforma dicionario em lista
	Serv_List = []
	for task in tasks:
		Serv_List.append([task, tasks[task][0], tasks[task][1]])

	Fog_nro = sw
	MaxIter = 10
	dim = 2

	Pos = {}
	Nro_serv = len(Serv_List)

	Alpha = numpy.zeros(1)
	Alpha_pos = numpy.zeros(dim)
	Alpha_score = float("inf")

	Beta = numpy.zeros(1)
	Beta_pos = numpy.zeros(dim)
	Beta_score = float("inf")

	Delta = numpy.zeros(1)
	Delta_pos = numpy.zeros(dim)
	Delta_score = float("inf")

	Positions = numpy.zeros((Nro_serv,2))

	# print("GWO SOLTION")

	# for z in range(0, dim):
	#     for p in range(0, Nro_serv):
	#         print(Serv_List[p][z+1])

	# print("Tarefas atuais:",Serv_List)


	for i in range(0,dim):
		for j in range(0, Nro_serv):
			#print ([Serv_List[j][i+1]])
			y = numpy.array([Serv_List[j][i+1]])
			#x = numpy.array([Fog_nro])
			#p = euclidiana(y,x)
			#print ("valor e euclidiana: ", y, p) #Positions[j,i] = p
			#if (j == 0):
			#	Positions[j,i] = p
			#else:
			#    Positions[j,i] = y
			Positions[j,i] = y
	#print (Positions)
	aux = (2/MaxIter)
	a = 2
	A, C = update_Coeficientes(a)
	
	for l in range(0,MaxIter): #máximo de iterações

		for j in range(0,Nro_serv): #passar por todos os serviços
				   
			fitness = F5(Positions[j,:])
				
			
			if (fitness < Alpha_score):
				
				Alpha = j
				Alpha_score = fitness
				Alpha_pos=Positions[j,:].copy()
			elif (fitness > Alpha_score and fitness < Beta_score):
				
				Beta = j
				Beta_score = fitness
				Beta_pos=Positions[j,:].copy()
			elif (fitness > Alpha_score and fitness < Beta_score and fitness < Delta_score):
			
				Delta = j
				Delta_score = fitness
				Delta_pos=Positions[j,:].copy()
			
		a = a - aux 
		
		for i in range(0,Nro_serv):
			for j in range (0,dim):
				#X = numpy.array([Fog_nro])
				
				#atualiza_Coeficientes(a)
				#a = a - aux
				A1, C1 = update_Coeficientes(a)
				D_alpha=abs(C1*Alpha_pos[j]-Positions[i,j]); # Equation ()-part 1
				X1=Alpha_pos[j]-A1*D_alpha; # Equation ()
				#a = a - aux    
				A2, C2 = update_Coeficientes(a)
				D_beta=abs(C2*Beta_pos[j]-Positions[i,j]); # Equation ()
				X2=Beta_pos[j]-A2*D_beta; # Equation ()       
				#a = a - aux    
				A3, C3 = update_Coeficientes(a)
				D_delta=abs(C3*Delta_pos[j]-Positions[i,j]); # Equation ()
				X3=Delta_pos[j]-A3*D_delta; # Equation ()             

				Positions[i,j] =(X1+X2+X3)/3  # Equation ()
				
		#print(['At iteration '+ str(l)+ ' the best fitness is '+ str(Alpha_score)]);
	
	# retorna posicao da solucao
	best_schedule = Serv_List[Alpha]
	return best_schedule
