import numpy as np
import random
import sys
import csv

##	vertex Initalize function

def randomVertex(p):
	v = []
	for i in range(p):
		v.append(random.random())
	return np.array(v)	

def zeroVertex(p):
	return np.zeros(p)
	

##	Constants Value
C = 2	# v length
N = 100	# x length
m = 1.1	# u[i][k] parameter
P = 2	# Demention



##
##	Initalize
##
#	Initalize x
x = []
for i in range(N):
	#x.append(np.array([random.random(),random.random()]))
	x.append(randomVertex(P))
	
# x = sorted(x)

#	Initalize v
v = []
for j in range(C):
	#v.append(np.array([random.random(),random.random()]))
	v.append(randomVertex(P))

#	Initalize membership function,u[i][k]
u = [ [0 for k in range(N)] for i in range(C)]


##
##	MainLoop
##
loop = 0
Jbefore = float("inf")
while True:
	loop+=1
	
	#	Cal u[i][k]
	for i in range(C):
		for k in range(N):
			dik = np.linalg.norm(v[i]-x[k])
			
			total = 0.0
			for j in range(C):
				djk = np.linalg.norm(v[j]-x[k])
				total += (dik/djk)**(1.0/(m-1.0))
			u[i][k] = 1.0 / total
		
	
	#	Cal v[i]
	for i in range(C):
		
		#	cal denominator
		denominator = 0.0
		for k in range(N):
			denominator += u[i][k]**m
		
		#	cal numerator
		numerator = zeroVertex(P) #np.array([0.0,0.0])
		for k in range(N):
			numerator += (u[i][k] ** m)*x[k]
		
		#	cal v
		v[i] = numerator / denominator
		
	
	#	Cal Jfcm, object function
	Jfcm = 0.0
	for k in range(N):
		for i in range(C):
			dik = np.linalg.norm(v[i]-x[k])
			Jfcm += (u[i][k] ** m) * dik  	
	
		
	#	Check continue condition
	if Jbefore <= Jfcm:
		break
		
	#	update Jbefore
	Jbefore = Jfcm


##
##	print
##

#	print loop counter
print "# loop="+str(loop)

#	print v[i]
print " #v=" + str(v)

#	print u[i][k]
for k in range(N):
	sys.stdout.write(str(x[k][0]))
	sys.stdout.write(",")
	sys.stdout.write(str(u[0][k]))
	sys.stdout.write(",")
	print u[1][k]
	

#	write x to file
#	np.savetxt("x_nomal.csv",x,delimiter=",")
f1 = open("xy1.csv","w")
f2 = open("xy2.csv","w")
for k in range(N):
	if(u[0][k]<u[1][k]):
		f2.write(str(x[k][0])+","+str(x[k][1])+"\n")	
		
	else:
		f1.write(str(x[k][0])+","+str(x[k][1])+"\n")	

	
f1.close()
f2.close()
	




	
