set terminal png
set output "fuzzy.png"
set datafile separator ","

plot "ts_xy0.csv" using 1:2 with p lc 11 title "C0",\
"ts_xy1.csv" using 1:2 with p lc 12 title "C1",\
"ts_xy2.csv" using 1:2 with p title "C2"
