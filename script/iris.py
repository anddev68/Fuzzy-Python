# coding: UTF-8
import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets as ds 
from sklearn.metrics import accuracy_score
import random
import math
import sys

#	
#	Irisのデータを用いてクラスタリングを行う
#


#
#	各種パラメータの設定
#
C = 3	# v length
N = 30	# x length
P = 4	# Demention
q = 2.5
Thigh = 0.0000000001


#
#	Irisのデータを用いて初期データを生成
#	[2:4] 花弁の長さと幅のみ
# 	[1:3]
iris = ds.load_iris()
x = iris.data
N = len(x)

#
#	Irisの正解データ
#
target = iris.target

#
#	乱数による初期データの生成
#
v = np.array( [ np.random.rand(P) for i in range(C) ]) # クラスタ中心
u = np.zeros([C,N])

#
#	標準偏差の表示
#
print "std="+str(np.std(x))



##
##	メインループ
##
loop = 0
Jbefore = float("inf")
while True:
	loop+=1
	
	T = Thigh * math.exp (-2.0*loop**(1.0/P))
	beta = 1.0 / T
	
	
	#	Cal u[i][k]
	for k in range(N):
		
		denominator = 0.0
		for j in range(C):
			djk = np.linalg.norm(v[j]-x[k])
			denominator += (1.0-beta*(1.0-q)*djk)**(1.0/(1.0-q))
		
		for i in range(C):
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
		
	Jbefore = Jfcm


	#	update Jbefore
#
#	vの表示
#
print "v="
print v

#
#	ループ回数の表示
#
print "loop=" + str(loop)




#	帰属するクラスタの番号を保存しておく配列
#	targetと比較するために作成
result = np.array( [ np.argmax(u[:,k]) for k in range(N) ] )

#
#	結果のインデックスがバラバラなので先頭を0にするように変更する
#	先頭のデータは0へ変更
#	最後尾のデータは2へ変更
#	変更をすべてに適用
first = result[0]
last = result[N-1]
for k in range(N):
	if result[k] == first:
		result[k] = 0
	elif result[k] == last:
		result[k] = 2
	else:
		result[k] = 1	

print "target="
np.savetxt(sys.stdout,target[None],fmt='%.0f',delimiter=' ')

print "result="
np.savetxt(sys.stdout,result[None],fmt='%.0f',delimiter=' ')


#
#	正答率を表示
#
score = accuracy_score(target,result)
print str(score*100) + "% (" + str(score*N) + "/" + str(N) + ")"



#
#	グラフにプロットする
#
#colors = ['g','r','c','m','y','k','w']
#plt.axis([0.0,1.0,0.0,1.0])
#for i in range(C):
#	plt.plot(x2[i],y2[i],"o",color=colors[i]) 
	
#plt.plot(v[:][:,1],v[:][:,0],"x",color='b') # クラスタ集合を二次元平面にプロットする
#plt.show()
	






