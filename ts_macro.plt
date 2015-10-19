set terminal png
set output 'fuzzy.png'
set datafile separator ','
plot 'ts_xy0.csv' using 1:2 with p lc 3 title 'C0','ts_xy1.csv' using 1:2 with p lc 4 title 'C1','ts_xy2.csv' using 1:2 with p lc 5 title 'C2','ts_xy3.csv' using 1:2 with p lc 6 title 'C3','ts_v.csv' using 1:2 with p lc 2 title 'V'