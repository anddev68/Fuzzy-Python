set terminal png
set xrange [0.0:1.0]
set yrange [0.0:1.0]
set output 'tn_result.png'
set datafile separator ','
plot 'tn_xy0.csv' using 1:2 with p lc 3 title 'C0','tn_xy1.csv' using 1:2 with p lc 4 title 'C1','tn_v.csv' using 1:2 with p lc 2 title 'V'