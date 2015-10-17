import math

#	output t,q-n graph
#	@author Hideki.KANO

##	Initalize Parameter

#	Initalize temperature
Thigh = 10.0
#	param for cooling schedule
Cd = 2.0
#	Demention of data
D = 2
#	for avoiding to q = 1.0
e = 0.01
#	loopcounter
m = 1


##	main loop
while m < 12:
	#	VFA
	T = Thigh * math.exp(-Cd*(m**(1.0/D)))	
	#T = Thigh * math.exp(-Cd*m)
	
	#	calculate q
	q = (Thigh+e) / T
	#	plot
	print str(m) + " " + str(T) + " " + str(q)
	
	m+=1
	
	



