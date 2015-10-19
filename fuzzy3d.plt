set terminal png
set output "fuzzy3d.png"

set zrange [0.0:1.0]
set ticslevel 0

set datafile separator ","

splot "fuzzy" using 1:2:3 w lp ,\
 "x.csv" using 1:2:(0) with p ps 1 pt 65 lc 3,\
 "x.csv" using 1:3:(0) with p ps 1 pt 68 lc 4