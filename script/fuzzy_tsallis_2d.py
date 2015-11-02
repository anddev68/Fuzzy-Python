# coding: UTF-8
import numpy as np
import matplotlib.pyplot as plt

#	
#	二次元データをクラスタリングする
#


#
#	各種パラメータの設定
#
C = 2	# v length
N = 20	# x length
P = 2	# Demention
q = 1.1
T = 20


#
#	乱数による初期データの生成
#
x = np.array( [ np.random.rand(P) for i in range(N) ]) # クラスタ対象のデータ集合
v = np.array( [ np.random.rand(P) for i in range(C) ]) # クラスタ中心
u = np.zeros([C,N])

print x


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
	
	beta = 20
	
	
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
		
	#	update Jbefore
	Jbefore = Jfcm


#
#	vの表示
#
print "v="
print v


#
#	u[i][k]ごとにクラスターを抽出
#	帰属度が最大であるクラスターごとに色分けする
#	
for i in range(C):
	max_index = u[i,:].index(max(u[i,:])) # x[i]が帰属するクラスタの要素番号を取得
	x2[max_index].append(v[i]) # 要素を追加する
	


#
#	グラフ表示
#
plt.axis([0.0,1.0,0.0,1.0])
plt.plot(x[:][:,1],x[:][:,0],"o") # データ集合を二次元平面にプロットする
plt.plot(v[:][:,1],v[:][:,0],"x") # クラスタ集合を二次元平面にプロットする
plt.show()
	






