set terminal png
set output "image.png"
set y2tics
set y2range [0:800]
set y2label "q"
set ylabel "T"
set xlabel "n"
plot "dump" using 1:3 title "n-q" w lp axes x1y2, \
		"dump" using 1:2 title "n-T" w lp axes x1y1