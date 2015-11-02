# coding: UTF-8

import numpy as np
import random
import sys
import csv


##
##	Fuzzy clustring with Tsallis Entropy
##


##
##	Constans
##
C = 2	# v length
N = 20	# x length
#m = 1.1	# u[i][k] parameter
P = 2	# Demention
q = 1.1
T = 20

##
##	Initalize
##
#	init x
x = []
for i in range(N):
	if np.random.rand() < 0.5:
		#x.append(np.random.rand(P))
		x.append(np.array([0.1+np.random.rand()*0.1,0.1+np.random.rand()*0.1]))
	else:
		x.append(np.array([0.7+np.random.rand()*0.1,0.1+np.random.rand()*0.1]))
		
#	init v
v = []
for k in range(C):
	v.append(np.random.rand(P))
#	init u
u = [ [0 for k in range(N)] for i in range(C)]


##
##	初期データ分布の共分散を求める
##
sigmaX = 0.0
sigmaY = 0.0



##
##	main loop
##
loop = 0
Jbefore = float("inf")
while True:
	loop+=1
	
	beta = 20
	
	
	#	Cal u[i][k]
	for i in range(C):
		
		denominator = 0.0
		for j in range(C):
			djk = np.linalg.norm(v[j]-x[k])
			denominator += (1.0-beta*(1.0-q)*djk)**(1.0/(1.0-q))
		
		for k in range(N):
			dik = np.linalg.norm(v[i]-x[k])
			u[i][k] = (1.0-beta*(1.0-q)*dik)**(1.0/(1.0-q)) / denominator
		
	
	#	Cal v[i]
	for i in range(C):
		
		#	cal denominator
		denominator = 0.0
		for k in range(N):
			denominator += u[i][k]**q
		
		#	cal numerator
		numerator = np.zeros(P)
		for k in range(N):
			numerator += (u[i][k] ** q)*x[k]
		
		#	cal v
		num = numerator / denominator

			
		v[i] = num
		
	
	#	Cal Jfcm, object function
	Jfcm = 0.0
	for k in range(N):
		for i in range(C):
			dik = np.linalg.norm(v[i]-x[k])
			Jfcm += (u[i][k] ** q) * dik  	
	
		
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

	
	
#	print data set to tx_xyi.csv
f = []
for i in range(C):
	f.append( open("tn_xy"+str(i)+".csv","w") )

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

#	print v
np.savetxt("tn_v.csv",v,delimiter=",")

#	print u
np.savetxt("tn_u.csv",u,delimiter=",")


#	print macro
macro = open("tn_macro.plt","w")
macro.write("set terminal png\n")
macro.write("set xrange [0.0:1.0]\n")
macro.write("set yrange [0.0:1.0]\n")
macro.write("set output 'tn_result.png'\n")
macro.write("set datafile separator ','\n")
macro.write("plot 'tn_xy0.csv' using 1:2 with p lc 3 title 'C0'")
for i in range (1,C):
	macro.write(",'tn_xy"+str(i)+".csv' using 1:2 with p lc "+str(i+3)+" title 'C"+str(i)+"'")
macro.write(",'tn_v.csv' using 1:2 with p lc 2 title 'V'")	

macro.close()
	




	
