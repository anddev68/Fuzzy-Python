# -- iris2.py --
# 二次元配列が縦横逆になっていたのを修正しました。

import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets as ds 
from sklearn.metrics import accuracy_score
import random
import math
import sys
import copy


E1 = 0.01
E2 = 0.01
RAND_MIN = -10000
RAND_MAX = 10000
C = 3 # クラスタ中心の数
X = 150 # データ個数
P = 4 # データ次元
Cd = 2.0 # VFAの定数
Thigh = 20.0
q  = 1.1

def main():
	
  # Irisのデータを読み込む
  iris = ds.load_iris() # Irisのデータをロードする
  x = iris.data  # Irisの4次元データ(150個)
  target = iris.target  # 正解データ [0,0,0,1....
  
  #	fcmを適用する
  fcm(x,C,Thigh,q)
  
  # 結果を表示する
  
 
 
  
#
# 収束判定のための移動度を求める関数
# デバッグ終了
# @param v1
# @param v2
# @return max 移動した距離の最大値
#
def distance(v1,v2):
  max = 0.0
  for i in range(len(v1)):
    score = np.linalg.norm(v1[i]-v2[i])
    if max < score:
      max = score
  return max


#
# 帰属度関数を計算する
# @param ref u
#   uの参照はそのままで値だけ更新する
# @param const v
# @param const x
# @param const q
# @param const T
#
def calc_uik(u,v,x,q,T):
  for k in range(len(x)):
    denominator = 0.0
    for j in range(len(v)):
      djk = np.linalg.norm(v[j]-x[k])
      denominator += (1.0-(1.0/T)*(1.0-q)*djk)**(1.0/(1.0-q))
    for i in range(len(v)):
      dik = np.linalg.norm(v[i]-x[k])
      u[i][k] = (1.0-(1.0/T)*(1.0-q)*dik)**(1.0/(1.0-q)) / denominator

#
# クラスタ中心を計算する
# @param ref u
# @param out v
#   vは参照が更新されます
# @param ref x
# @param const q
def calc_vi(u,v,x,q):
  # vをゼロクリアする
  v = np.zeros(v.shape)
  # vを計算する
  for i in range(len(v)):
    #	cal denominator
    denominator = 0.0
    for k in range(len(x)):
      denominator += u[i][k]**q
    #	cal numerator
    for k in range(len(x)):
      v[:,i] += (u[i][k] ** q)*x[:,k]
    #	cal v
    v[:,i] /= denominator
    


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
# @param C クラスタ中心の数
# @param Thigh 初期温度
# @param q q値
# @return [predict,loop]
#   loop:ループ回数
#   predict:クラスタリング結果
#
def fcm(x,C,Thigh,q):

  # クラスタ中心を初期化する
  # RAND_MINからRAND_MAXの間の値を取ることとする
  v = np.random.rand(C,x.ndim) * ( RAND_MAX - RAND_MIN ) + RAND_MIN
  print "init v = " + str(v)  
  # 帰属度関数を初期化する
  u = np.zeros(C,len(x))
  # 初期温度はThigh
  T = Thigh
  # ループカウント
  loop_count = 0
  # 温度の更新回数
  temperature_update_count = 0
  
  # ループ
  while True:
    # 外ループのviのバックアップ
    copied_Vi = copy.deepcopy(v)
    # 内ループ
    while True:
      # 内ループのviのバックアップ
      copy_vi = copy.deepcopy(v)
      # uikを計算する
      calc_uik(u,v,x,q,T)
      # viを計算する
      calc_vi(u,v,x,q)
      # ループカウントをインクリメントする
      loop_count += 1
      # 収束チェック  
      if distance(v,copied_vi) < E1:
        break
    # 収束チェック
    if distance(v,copied_Vi) < E2:
      break
    # 温度更新
    # 超高速アニーリング
    T = Thigh * math.exp (-2.0*temperature_update_count**(1.0/x.ndim)
    
  # loop end

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
		  

  return [predict,total_loop]
  





# ---
main()