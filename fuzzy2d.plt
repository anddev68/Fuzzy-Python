set terminal png
set output "fuzzy.png"
set datafile separator ","

plot "xy1.csv" using 1:2 with p lc 12 ,\
"xy2.csv" using 1:2 with p
