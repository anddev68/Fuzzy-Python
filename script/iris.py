# coding: UTF-8
#	
#	--- Iris.py ---
# Irisのデータを用いてtsaliisエントロピー正則化FCM法を試す
#


import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets as ds 
from sklearn.metrics import accuracy_score
import random
import math
import sys


def main():

  # Irisのデータを読み込む
  iris = ds.load_iris() # Irisのデータをロードする
  data = iris.data  # Irisの4次元データ(150個)
  target = iris.target  # 正解 [0,0,0,1....
  
  # 標準偏差を表示する
  # print "std="+str(np.std(x))

  #	各種パラメータの設定
  C = 3	# v length
  N = 150	# x length
  P = 4	# Demention
  Thigh = 0.0000000001
  q = 1.1


  # fcmで求める 
  result = fcm(data,P,N,C,Thigh,q)
  predict = result[0]
  loop = result[1]

  # 正解とpredictを表示
  print "target="
  np.savetxt(sys.stdout,target[None],fmt='%.0f',delimiter=' ')

  print "predict="
  np.savetxt(sys.stdout,predict[None],fmt='%.0f',delimiter=' ')

  #	正答率を表示
  score = accuracy_score(target,predict)
  print str(score*100) + "% (" + str(score*N) + "/" + str(N) + ")"

  #	ループ回数の表示
  print "loop=" + str(loop)




#
# fuzzy_clustring_method
# ファジィクラスタリングを実行する
#
# 1.クラスタ中心vをランダムに決定する
# 2.帰属度関数uをゼロクリアする
# 3.以下の操作を繰り返す
# 3-1.ループ回数を更新する
# 3-2.温度を更新する
# 3-3.uを更新する
# 3-4.vを更新する
# 3-5.終了条件を判定
# 4.クラスタリング結果をpredictに保存する
# 5.ラベルを先頭が0,後ろが2になるように再配置する
# 6.[predict,loop]を返す
#
# @param x データ集合
# @param P データの次元数
# @param N データ集合の個数
# @param C クラスタ中心の数
# @param Thigh 初期温度
# @param q q値
# @return [predict,loop]
#   loop:ループ回数
#   predict:クラスタリング結果
#
def fcm(x,P,N,C,Thigh,q):

  # クラスタ中心を初期化する
  v = np.array( [ np.random.rand(P) for i in range(C) ]) 
  
  # 帰属度関数を初期化する
  u = np.zeros([C,N])
  
  # ループ開始
  loop = 0
  update_temperature = 0
  while True:
    # ループを更新する
    loop+=1
    # 温度を更新する
    T = Thigh * math.exp (-2.0*loop**(1.0/P))  
    beta = 1.0 / T
    
    #	--- Cal u[i][k] ---
    # ここの部分はデバッグ済み。触らない。
    for k in range(N):
		
		  denominator = 0.0
		  for j in range(C):
			  djk = np.linalg.norm(v[j]-x[k])
			  denominator += (1.0-beta*(1.0-q)*djk)**(1.0/(1.0-q))
		
		  for i in range(C):
			  dik = np.linalg.norm(v[i]-x[k])
			  u[i][k] = (1.0-beta*(1.0-q)*dik)**(1.0/(1.0-q)) / denominator
		
    #	--- Cal v[i] ---
    # ここの部分はデバッグ済み。触らない。
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
		  
    # 収束判定を行う  
    break 
  
  
  # クラスタリング結果を取得
  predict = np.array( [ np.argmax(u[:,k]) for k in range(N) ] )

  # ラベルの再割り振り
  first = predict[0]
  last = predict[N-1]
  for k in range(N):
	  if predict[k] == first:
		  predict[k] = 0
	  elif predict[k] == last:
		  predict[k] = 2
	  else:
		  predict[k] = 1	

  return [predict,loop]


# ---
main()

