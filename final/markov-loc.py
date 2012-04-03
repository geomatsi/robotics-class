# FINAL 4,5,6,7

# globals

colors = [['green', 'green'],
          ['red', 'green']]

measurements = ['red', 'red', 'red']
motions = [[-1,0], [0,0]]
sensor_right = 0.8
p_move = 1.0

### aux

rows = len(colors)
cols = len(colors[0])

### functions

def show(p):
    for i in range(len(p)):
        print p[i]

#

def creat():
    q = []

    for i in range(rows):
        q.append(list())
        for j in range(cols):
            q[i].append(0.0)

    return q

#

def init():
    q = creat()

    for i in range(rows):
        for j in range(cols):
            q[i][j] = 1.0/(rows*cols)

    return q

#

def sense(p, Z):
    q = creat()

    for i in range(rows):
        for j in range(cols):
            hit = (Z == colors[i][j])
            q[i][j] = p[i][j]*(hit*sensor_right + (1-hit)*(1.0-sensor_right))

    s = 0.0
    for i in range(rows):
        for j in range(cols):
            s = s + q[i][j]

    for i in range(rows):
        for j in range(cols):
            q[i][j] = q[i][j] / s
    
    return q

#

def move(p, U):

    if U == [0,0]:
        return p

    q = creat()

    for i in range(rows):
        for j in range(cols):
            if U == [0,1]:
                if j == (cols - 1):
                    q[i][j] = p[i][j] + p[i][j-1]
            elif U == [0,-1]:
                if j == 0:
                    q[i][j] = p[i][j] + p[i][j+1]
            elif U == [1,0]:
                if i == (rows - 1):
                    q[i][j] = p[i][j] + p[i-1][j]
            elif U == [-1,0]:
                if i == 0:
                    q[i][j] = p[i][j] + p[i+1][j]
            else:
                print "ERROR"

    return q

### main

p = init()
show(p)

for m in range(len(motions)):
    p = sense(p, measurements[m])
    print "----> sense"
    show(p)
    p = move(p, motions[m])
    print "----> move"
    show(p)

