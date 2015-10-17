import random
import numpy as np

##	Initialize

#	qvalue
q = 1.1
#	Number of data,x (Integer)
N = 20
#	Number of center of cluster,v(Integer)
C = 2
#	Initialize temperature
T = 2000
#	Continue Conditions
e1 = 0.01
e2 = 0.01


##	Print Method
def printArray(array,name):
	i = 0
	for v in array:
		print name + "[" + str(i) + "]=" + str(v)
		i+=1
		
##	Calculate u[i][k]
def calculateU(){
	
}






		


#	Initialize center of cluster,v[i] as random
#	demation p = 2D
i = 0
v = []
while i<C:
	v.append(np.array([random.random(),random.random()]))
	i+=1
#	Initalize set of data,x[k] as random
#	demation p = 2D
x = []
k = 0
while k<N:
	x.append(np.array([random.random(),random.random()]))
	k+=1
#	Initalize membership function,u[i][k]
u = [ [0 for k in range(N)] for i in range(C)]

#	Print
print "---------- DATA SET ----------"
printArray(x,"x")
print ""
printArray(v,"v")

##	mainLoop	
##
##	Continue Conditions:
##		Not convergence





pre_temperature = temperature	# temperature before changing 


#	calculate u[i][k]
beta = 1.0/T
k = 0
while k<N:
	denominator = 0
	j = 0
	while j<C:
		t = x[k] - v[j]
		djk = np.linalg.norm(t)	# calculate djk with norm method
		denominator += (1.0-beta*(1-q)*djk)**(1/(1-q))
		j+=1
	i = 0
	while i<C:
		t = x[k] - v[i]
		dik = np.linalg.norm(t)
		numerator = (1-beta*(1-q)*dik)**(1/(1-q))
		u[i][k] = numerator / denominator
		i+=1
	k+=1



#	calculate v[i]
i = 0
while i<C:
	denominator = 0
	numerator = np.array([0,0])
	k = 0
	while k<N:
		denominator += u[i][k] ** q
		numerator += denominator * x[k]
		k+=1
	v[i] = numerator / denominator
	i+=1


#	d1 is a distance that center of cluster,v moved at same temperature
d1 = 
#	d2 is a distance that center of cluster,v moved at before temperature
d2 = 

#	Check convergence
#	The distance is so long at same temperature,
#	do loop with same temperature
if( e1 < d1 ){
	 
}

#	Check convergence
#	The distance is so long at before temperature,
#	do loop, and cool tempareture
if( e2 < d2){
	
}



#	calculate object function, J_tsallis
J = 0
J1 = 0	# first section of J function
J2 = 0	# second section of J function
ramuda = 1 / beta
for k in range(N):
	for i in range(C):
		t = x[k] - v[i]
		dik = np.linalg.norm(t)
		J1 += u[i][k] ** q * dik
		J2 += u[i][k] ** q * log(q) * u[i][k]
J = J1 + J2*ramuda








