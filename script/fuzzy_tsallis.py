
import numpy as np
import random
import sys
import csv
import copy
import math

##
##	Constants Value
##
C = 3	# v length
N = 80	# x length
#q = 2	# u[i][k] parameter
P = 2	# data demention
e1 = 0.01	# continue condition
e2 = 0.01 	# continue condition
Cd = 2.0	# VFA parameter
Thigh = 20


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

print "#v=" + str(v)

##
##	MainLoop
##
loop = -1
while True:
	loop+=1
	
	#	update q
	q = (Thigh+0.1)/T
	
	print "#q="+str(q)
	
	#	Cal u[i][k]
	beta = 1.0/T
	for k in range(N):
		denominator = 0.0
		for j in range(C):
			djk = np.linalg.norm(v[j]-x[k])
			denominator += (1.0-beta*(1.0-q)*djk)**(1.0/(1.0-q))
		for i in range(C):
			dik = np.linalg.norm(v[i]-x[k])
			numerator = (1.0-beta*(1.0-q)*dik)**(1.0/(1.0-q))
			u[i][k] = numerator / denominator
	
	#print "#u="+str(u[0])
	

	#	Cal v[i]
	for i in range(C):
		
		#	cal denominator
		denominator = 0.0
		for k in range(N):
			denominator += u[i][k]**q
		
		#	cal numerator
		numerator = zeroVertex(P) #np.array([0.0,0.0])
		for k in range(N):
			numerator += (u[i][k] ** q)*x[k]
		
		#	cal v
		v[i] = numerator / denominator
		
	# print "#v=" + str(v)
	
	#	compeare solution before 1 step as same temperature
	#	if Not max_{1<=i<=c}{|vi-v'i|}<=e1
	#		then goto loop
	error = getError(vdash,v)
	print "#e1-error="+str(error)
	if (error <=e1) == False:
		vdash = copy.deepcopy(v)	# save v as same temperature
		continue
	
	
	
	#	compere solution between before temperature and now temperature
	#	if max_{1<=i<=c}{|Vi-V'i|<=e2}
	#		then end loop
	#	else
	#		then goto loop and update T
	error = getError(Vdash,v)
	print "#e2-error="+str(error)
	if error<=e2:
		break
	
	Vdash = copy.deepcopy(v)	#save v as deferent temperature	
	T = Thigh * math.exp(-Cd*(loop**(1.0/P)))	# update temperature
	


##
##	print
##

#	print loop counter
print "# loop="+str(loop)

#	print v[i]
print " #v=" + str(v)

	
	
#	write x to file
#	np.savetxt("x_nomal.csv",x,delimiter=",")
f = []
for i in range(C):
	f.append( open("ts_xy"+str(i)+".csv","w") )

for k in range(N):
	#	get max of u[i][k] 
	maxindex = 0
	maxvalue = 0.0
	for j in range(0,C):
		cur = u[j][k]
		if maxvalue < cur:
			maxvalue = cur
			maxindex = j
	#	write to file, v[k] has biggest value
	f[maxindex].write(str(x[k][0])+","+str(x[k][1])+"\n")
	

	
for i in range(C):
	f[i].close()
	
np.savetxt("ts_u.csv",u,delimiter=",")



	
