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
import itertools

# 定数宣言
E1 = 0.01
E2 = 0.01
RAND_MIN = 0
RAND_MAX = 8
C = 3 # クラスタ中心の数
N = 150 # データ個数
P = 3 # データ次元
Cd = 2.0 # VFAの定数
Thigh = 2.0
q  = 2.0



# ここからメイン
def main():
  # sys.exit()	


  # Irisのデータを読み込む
  # x.shape => (150,4)
  # 4項目の150個 
  iris = ds.load_iris() # Irisのデータをロードする
  x = iris.data  # Irisの4次元データ(150個)
  target = iris.target  # 正解データ [0,0,0,1....  
  
  # 結果初期化
  total_loop = 0.0
  total_error = 0.0
  min_loop = 1000000000
  min_error =  10000000000 
  max_loop = -1
  max_error = -1

  # MAX回数 で fcmを適用する
  MAX = 10
  for i in range(MAX):
    # fcmを適用
    result = fcm(x,C,Thigh,q)
    predict = result[0]
    loop = result[1]  

    # 評価する
    result = evaluate(predict,target)
    predict = result[0]
    score = result[1] # 正答率
    error = x.shape[0] * (1.0-score) # 間違った数

    # 結果を更新
    total_loop += loop # 平均を出すため合計値を記録しておく
    total_error += error
    min_loop = min(min_loop,loop) # 最小値更新
    min_error = min(min_error,error)
    max_loop = max(max_loop,loop) # 最大値更新
    max_error = max(max_error,error)
    

    # 結果を表示する
    #print "target="
    #np.savetxt(sys.stdout,target[None],fmt="%.0f",delimiter=" ")
    #print "predict="
    #np.savetxt(sys.stdout,predict[None],fmt="%.0f",delimiter=" ")

    # 正解率の表示
    #print str(score*100) + "% (" + str(score*N) + "/" + str(N) + ")"

    # 計算回数の表示
    #print "loop=" + str(loop) 
 
    # 進捗を表示
    print str(i+1) + "/" + str(MAX) + " passed."

  # 結果を表示
  print "--------------------------------------------"
  print "q=" + str(q)
  print "min_loop=" + str(min_loop)
  print "max_loop=" + str(max_loop)
  print "ave_loop=" + str(total_loop/MAX)
  print "min_error=" + str(min_error)
  print "max_error=" + str(max_error)
  print "ave_error=" + str(total_error/MAX)

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
    #score = np.linalg.norm(v1[i]-v2[i])
    score = measure(v1[i],v2[i])
    if max < score:
      max = score
  return max

#
# p1とp2の距離を測定する
# @param p1
# @param p2
#
def measure(p1,p2):
  return  sum( [ (p1[i]-p2[i])**2 for i in range(len(p1)) ] )**0.5





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
        denominator += ( 1.0-(1.0/T)*(1.0-q)*djk ) ** (1.0/(1.0-q))
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
# 評価関数
# fcm法で得られるpredict配列について、
# 本来とは異なるクラスタ番号が割り当てられる可能性がある。
# クラスタ番号については順不同であるため、
# 考えられるすべての組み合わせについて、番号を振り直して計算を行う
# 80%を超えた時点でその答えを解とする。
# @return [copy,score]
#  並び替え後の配列とスコアを返す
#
def evaluate(predict,target):
  # 最高スコア
  max_score = 0.0
  max_array = None
  # 0=>1,1=>2,2=>0のようにすべての組み合わせについて検証する
  for replace in itertools.permutations((0,1,2),3):
    # コピーに番号を振り直したものを保存する
    copy = [ replace[index] for index in predict  ]
    # 高速化のため80%を超えた時点で終了する
    score = accuracy_score(copy,target)
    if max_score < score:
      # 評価値（正答率）と再割り当てしたpredictを返す
      #return [np.array(copy),score]
      max_score = score
      max_array = copy
  # ここまで来た場合はエラー
  #print "Exception: evalute() failed"
  #sys.exit()    
  #print copy
  return [np.array(copy),max_score]


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
  # 縦方向をxとする
  # 横方向に各クラスタへの帰属度を示す
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
      # viを計算する
      calc_vi(u,v,x,q)
      # ループカウントをインクリメントする
      loop_count += 1
      # debug
      print "loop=" + str(loop_count) + " T=" + str(T) + " q=" + str(q)
      #for i in range(v.shape[0]):
      #  print "v[" + str(i) + "] measure=" + str(measure(v[i],copied_vi[i]))
      #np.savetxt(sys.stdout,u[None],fmt="%10.5f",delimiter=" ")      
      #if loop_count == 20:
      #  sys.exit()   
      print "v=" + str(v)
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
    Tdash = Thigh * math.exp(-2.0*temperature_update_count**(1.0/x.shape[1]))
    #q=4.6676*math.pow( Thigh*math.exp(-Cd*math.pow(temperature_update_count,1.0/x.shape[1])),-1.066 )
    q = (Thigh+0.01)/Tdash

  # loop end
  #print v
  # クラスタリング結果を取得
  #for k in range(x.shape[0]):
  #  print np.argmax(u[k,:])

  predict = np.array( [ np.argmax(u[k,:]) for k in range(x.shape[0]) ] )
  # print predict
  # print loop_count

  return [predict,loop_count]
  





# ---
main()
