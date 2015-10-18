import random
import copy
import numpy as np
import math

##	Initialize Parameter

#	qvalue
q = 1.1
#	Number of data,x (Integer)
N = 20
#	Number of center of cluster,v(Integer)
C = 2
#	Initialize temperature
Thigh = T = 20
#	Continue Conditions
e1 = 0.01
e2 = 0.01
#	param for cooling schedule
Cd = 2.0
#	Demention of data
D = 2


##	Print Method
def printArray(array,name):
	i = 0
	for v in array:
		print name + "[" + str(i) + "]=" + str(v)
		i+=1
			
			
##	Calculate vbefore[i] - vafter[i]
##	@return
##		sum distance that v moved
def sumDistance(before,after):
	total = 0
	for i in range(C):
		t = after[i] - before[i]
		dist = np.linalg.norm(t)	# calculate a distance v moved
		total+=dist
	return total	

				

##	Initalize

#	Initialize center of cluster,v[i] as random
#	demation p = 2D
i = 0
v = []
while i<C:
	v.append(np.array([random.random(),random.random()]))
	i+=1
v1 = copy.deepcopy(v)
v2 = copy.deepcopy(v)
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
#print "---------- DATA SET ----------"
#printArray(x,"x")
#print ""
#printArray(v,"v")

#	update q value
q = (Thigh+0.01) / T 

##	mainLoop	
##
##	Continue Conditions:
##		Not convergence
m = 0	#	loop counter
while m < 100:
	#	inc loop counter
	m+=1
	
	printArray(v,"v")
	
	#	calculate u[i][k]
	beta = 1.0/T
	k = 0
	while k<N:
		denominator = 0.0
		j = 0
		while j<C:
			t = x[k] - v[j]
			djk = np.linalg.norm(t)	# calculate djk with norm method
			denominator += (1.0-beta*(1.0-q)*djk)**(1.0/(1.0-q))
			j+=1
		i = 0
		while i<C:
			t = x[k] - v[i]
			dik = np.linalg.norm(t)
			numerator = (1.0-beta*(1.0-q)*dik)**(1.0/(1.0-q))
			#	This line is changing u[i][k]
			u[i][k] = numerator / denominator
			i+=1
		k+=1	
		

	#	calculate v[i]
	i = 0
	while i<C:
		denominator = 0.0
		numerator = np.array([0.0,0.0])
		k = 0
		while k<N:
			denominator += u[i][k] ** q
			numerator += x[k]*(u[i][k] ** q)
			k+=1
		v[i] = numerator  / denominator
		i+=1
	
	#	distance center of claster moved compare with same q value	
	d1 = sumDistance(v,v1)
	if e1 < d1:
		# copy v1
		v1 = copy.deepcopy(v)
		# goto loop
		continue
	
	#	with before q value
	d2 = sumDistance(v,v2)
	if e2 < d2:
		
		#	cool T
		#	VFA
		T = Thigh * math.exp(-Cd*(m**(1.0/D)))			
		#	update q value
		q = (Thigh+0.01) / T 
		#	copy v2
		v2 = copy.deepcopy(v)
		#	goto loop
		continue


	#	result converged
	break
	
	
printArray(x,"x")

print u[0]
		
	
printArray(v,"v")






