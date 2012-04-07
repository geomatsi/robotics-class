Suppose we store data in the file test.out in the following format:

# columns separated by whitespaces
# x1  y1  x2  y2
1.0  2.4  4.3  5.4
3.3  3.2  5.6  3.2

gnuplot> plot "./test.out" using 1:2 with lines, "./test.out" using 3:4 with lines
