# coding: UTF-8

# -- iris2.py --
# 11.21 updated.
# 二次元配列が縦横逆になっていたのを修正しました。
# calc_uikとcalc_viの修正を行いました。

import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets as ds 
from sklearn.metrics import accuracy_score
import random
import math
import sys
import copy

# 定数宣言
E1 = 0.01
E2 = 0.01
RAND_MIN = 1
RAND_MAX = 8
C = 3 # クラスタ中心の数
N = 150 # データ個数
P = 3 # データ次元
Cd = 2.0 # VFAの定数
Thigh = 2.0
q  = 2.0


# ここからメイン
def main():
	
  # Irisのデータを読み込む
  # x.shape => (150,4)
  # 4項目の150個 
  iris = ds.load_iris() # Irisのデータをロードする
  x = iris.data  # Irisの4次元データ(150個)
  target = iris.target  # 正解データ [0,0,0,1....  
  
  #	fcmを適用する
  result = fcm(x,C,Thigh,q)
  predict = result[0]
  loop = result[1]  

  # 結果を表示する
  print "target="
  np.savetxt(sys.stdout,target[None],fmt="%.0f",delimiter=" ")
  print "predict="
  np.savetxt(sys.stdout,predict[None],fmt="%.0f",delimiter=" ")

  # 正解率の表示
  score = accuracy_score(target,predict)
  print str(score*100) + "% (" + str(score*N) + "/" + str(N) + ")"

  # ループ回数の表示
  print "loop=" + str(loop) 
 
 
  
#
# 収束判定のための移動度を求める関数
# デバッグ終了
# @param v1
# @param v2
# @return max 移動した距離の最大値
#
def distance(v1,v2):
  max = 0.0
  for i in range(v1.shape[0]):
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
  # データ個数
  N = x.shape[0]
  # クラスタ個数
  C = v.shape[0]
  # 次元数
  P = x.shape[1]

  for i in range(C):
    for j in range(N):
      # uik =uijの計算  
      #dik2 = np.linalg.norm( x[j,:] - v[i,:] )
      # 距離dikの計算を行う
      dik = 0.0
      for l in range(P):
        dik += math.pow(x[j,l]-v[i,l],2)
      # 分子を作成
      numerator = ( 1.0-(1.0/T)*(1-q)*dik ) ** (1.0/(1.0-q)) 
      # 分母の計算を行う
      denominator =  0.0
      for k in range(C):      
        # djkの計算を行う
        djk = 0.0
        for l in range(P):
          djk += math.pow(x[j][l]-v[k][l],2)
        denominator += ( 1.0-(1.0/T)*(1.0-q)*djk ) ** (1.0/1.0-q)
      # 分子/分母をuとする
      u[j,i] = numerator / denominator

  #print u
  #print v
  #sys.exit()      


#
# クラスタ中心を計算する
# @param ref u
# @param ref v
# @param ref x
# @param const q
def calc_vi(u,v,x,q):
  
  # データ個数
  N = x.shape[0]
  # クラスタ個数
  C = v.shape[0]
  # 次元数
  P = x.shape[1]
  # P = v.shape[1] #同じになるはず 
  # vを計算
  for i in range(C):
    for l in range(P):
      uikm = sum( [ u[j,i] ** q for j in range(N) ] )
      uikmxk = sum( [ u[j,i] ** q * x[j,l]  for j in range(N) ])
      v[i,l] = uikmxk / uikm 
 
    
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
  # v.shape => (3,4)
  # 4次元の3個
  v = np.random.rand(C,x.shape[1]) * ( RAND_MAX - RAND_MIN ) + RAND_MIN
  #print "init v = " + str(v)  
  # 帰属度関数を初期化する
  # u.shape => (150,3)
  # xに対してのV
  u = np.zeros( (x.shape[0],C) )
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
      copied_vi = copy.deepcopy(v)
      # uikを計算する
      calc_uik(u,v,x,q,T)
      # print u
      # viを計算する
      calc_vi(u,v,x,q)
      # ループカウントをインクリメントする
      loop_count += 1
      # debug
      print "loop=" + str(loop_count) + " T=" + str(T)
      print v
      #if loop_count == 5:
      #  sys.exit()   
      #print "v=" + str(v)
      #print "u=" + str(u[0:150,:])
      # 収束チェック  
      if distance(v,copied_vi) < E1:
        break
    # 収束チェック
    if distance(v,copied_Vi) < E2:
      break
    # 温度更新
    temperature_update_count +=1
    # 超高速アニーリング
    T = Thigh * math.exp(-2.0*temperature_update_count**(1.0/x.shape[1]))
    
  # loop end
  #print v

  # クラスタリング結果を取得
  #for k in range(x.shape[0]):
  #  print np.argmax(u[k,:])

  predict = np.array( [ np.argmax(u[k,:]) for k in range(x.shape[0]) ] )
  # print predict
  # print loop_count

  # ラベルの再割り振り
  first = predict[0]
  last = predict[N-1]
  for k in range(N):
    if predict[k] == first:
      predict[k] = 0
    elif predict[k] == last:
      predict[k] = 1
    else:
      predict[k] = 2
		  

  return [predict,loop_count]
  





# ---
main()
