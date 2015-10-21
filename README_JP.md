Fuzzy-Python
=============================
Fuzzy-c-meansを実行するためのスクリプトです。  
以下のライブラリを導入しておいてください。
* numpy

使い方
-----

### script/fuzzy_tsallis.py ###
Tsallisエントロピー正則化FCM法のサンプルです。  
実行するとカレントディレクトリに以下のファイルが出来上がります。  
作成されるファイルの説明は次の通り。
<dl> 
	<dt>ts_xyi.csv (iは任意の数字)</dt>
	<dd>Ci個目のクラスタの集合です。</dd>
	<dt>ts_v.csv</dt>
	<dd>クラスタ中心の一覧です。</dd>
	<dt>ts_u.csv</dt>
	<dd>出来上がった帰属度関数です。</dd>
	<dt>ts_macro.plt</dt>
	<dd>
	gnuplot描画用マクロです。これを使うとクラスタを色分けしてpngにしてくれます。<BR>
	クラスタ中心の数に応じてマーカーの形や色を変えます。
	</dd>
</dl>