##
##	Warning
##	This script does not work
##



import numpy as np
import random
import sys
import csv
import coppy
import math

##
##	Constants Value
##
C = 3	# v length
N = 100	# x length
m = 2	# u[i][k] parameter
P = 1	# data demention
e1 = 0.01	# continue condition
e2 = 0.01	# continue condition
Cd = 2.0	# VFA parameter
Thigh = 500


##
##	vertex Initalize function
##
def randomVertex(p):
	v = []
	for i in range(p):
		v.append(random.random())
	return np.array(v)	

def zeroVertex(p):
	return np.zeros(p)
	
##
##	get error v1,v2
##
def getError(v1,v2):
	m = 0.0
	for i in range(C):
		score = np.linalg.norm(v1[i]-v2[i])
		m = max(score,m)
	return m
	



##
##	Initalize
##
#	Initalize x
x = []
for i in range(N):
	#x.append(np.array([random.random(),random.random()]))
	x.append(randomVertex(P))
	
#	Initalize v
v = []
for j in range(C):
	#v.append(np.array([random.random(),random.random()]))
	v.append(randomVertex(P))

#	Initalize membership function,u[i][k]
u = [ [0 for k in range(N)] for i in range(C)]

# Initalize temperature
T = Thigh

# Initalize Vdash,vdash
vdash = copy.deepcopy(v)
Vdash = copy.deepcopy(v)

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
				total += (dik/djk)**(1/(m-1))
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
	
	#	compeare solution before 1 step as same temperature
	#	if Not max_{1<=i<=c}{|vi-v'i|}<=e1
	#		then goto loop
	if !(getError(vdash,v)<=e1):
		vdash = copy.deepcopy(v)	# save v as same temperature
		continue
	
	
	
	#	compere solution between before temperature and now temperature
	#	if max_{1<=i<=c}{|Vi-V'i|<=e2}
	#		then end loop
	#	else
	#		then goto loop and update T
	if getError(Vdash,v)<=e2:
		break
	
	Vdash = copy.deepcopy(v)	#save v as deferent temperature	
	T = Thigh * math.exp(-Cd*(loop**(1.0/p)))	# update temperature
	


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
	sys.stdout.write(str(x[k][1]))
	sys.stdout.write(",")
	sys.stdout.write(str(u[0][k]))
	sys.stdout.write(",")
	print u[1][k]
	
	
#	write x to file
np.savetxt("x.csv",x,delimiter=",")



	
