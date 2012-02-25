# globals

colors = [['red', 'green', 'green', 'red' , 'red'],
          ['red', 'red', 'green', 'red', 'red'],
          ['red', 'red', 'green', 'green', 'red'],
          ['red', 'red', 'red', 'red', 'red']]

measurements = ['green', 'green', 'green' ,'green', 'green']
motions = [[0,0],[0,1],[1,0],[1,0],[0,1]]
sensor_right = 0.7
p_move = 0.8

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
                q[i][j] = (1-p_move)*p[i][j] + p_move*p[i][(j-1) % cols]
            elif U == [0,-1]:
                q[i][j] = (1-p_move)*p[i][j] + p_move*p[i][(j+1) % cols]
            elif U == [1,0]:
                q[i][j] = (1-p_move)*p[i][j] + p_move*p[(i-1) % rows][j]
            elif U == [-1,0]:
                q[i][j] = (1-p_move)*p[i][j] + p_move*p[(i+1) % rows][j]
            else:
                print "ERROR"

    return q

### main

p = init()

for m in range(len(motions)):
    p = move(p, motions[m])
    p = sense(p, measurements[m])

show(p)



