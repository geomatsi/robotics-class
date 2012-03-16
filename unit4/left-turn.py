# ----------
# User Instructions:
#
# Implement the function optimum_policy2D() below.
#
# You are given a car in a grid with initial state
# init = [x-position, y-position, orientation]
# where x/y-position is its position in a given
# grid and orientation is 0-3 corresponding to 'up',
# 'left', 'down' or 'right'.
#
# Your task is to compute and return the car's optimal
# path to the position specified in `goal'; where
# the costs for each motion are as defined in `cost'.

# EXAMPLE INPUT:

# grid format:
#     0 = navigable space
#     1 = occupied space
grid = [[1, 1, 1, 0, 0, 0],
        [1, 1, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 0],
        [1, 1, 1, 0, 1, 1],
        [1, 1, 1, 0, 1, 1]]
goal = [2, 0] # final position
init = [4, 3, 0] # first 2 elements are coordinates, third is direction
cost = [2, 1, 20] # the cost field has 3 values: right turn, no turn, left turn

# EXAMPLE OUTPUT:
# calling optimum_policy2D() should return the array
#
# [[' ', ' ', ' ', 'R', '#', 'R'],
#  [' ', ' ', ' ', '#', ' ', '#'],
#  ['*', '#', '#', '#', '#', 'R'],
#  [' ', ' ', ' ', '#', ' ', ' '],
#  [' ', ' ', ' ', '#', ' ', ' ']]
#
# ----------


# there are four motion directions: up/left/down/right
# increasing the index in this array corresponds to
# a left turn. Decreasing is is a right turn.

forward = [[-1,  0], # go up
           [ 0, -1], # go left
           [ 1,  0], # go down
           [ 0,  1]] # do right
forward_name = ['up', 'left', 'down', 'right']

# the cost field has 3 values: right turn, no turn, left turn
action = [-1, 0, 1]
action_name = ['R', '#', 'L']


# ----------------------------------------
# modify code below
# ----------------------------------------

def optimum_policy2D():
    value = [[[999 for row in range(len(grid[0]))] for col in range(len(grid))],
        [[999 for row in range(len(grid[0]))] for col in range(len(grid))],
        [[999 for row in range(len(grid[0]))] for col in range(len(grid))],
        [[999 for row in range(len(grid[0]))] for col in range(len(grid))]]

    policy = [[[' ' for row in range(len(grid[0]))] for col in range(len(grid))],
        [[' ' for row in range(len(grid[0]))] for col in range(len(grid))],
        [[' ' for row in range(len(grid[0]))] for col in range(len(grid))],
        [[' ' for row in range(len(grid[0]))] for col in range(len(grid))]]

    policy2D = [[' ' for row in range(len(grid[0]))] for col in range(len(grid))]

    change = True

    while change:
        change = False

        for x in range(len(grid)):
            for y in range(len(grid[0])):
                for t in range(4):

                    if goal[0] == x and goal[1] == y:
                        if value[t][x][y] > 0:
                            policy[t][x][y] = '*'
                            value[t][x][y] = 0
                            change = True

                    elif grid[x][y] == 0:
                        for a in range(len(action)):

                            x2 = -1
                            y2 = -1
                            t2 = -1

                            # where we can get from current (x,y): find (x2,y2)

                            if action[a] == -1:    # right turn
                                if t == 0:
                                    x2 = x
                                    y2 = y + 1
                                    t2 = 3
                                elif t == 1:
                                    x2 = x - 1
                                    y2 = y
                                    t2 = 0
                                elif t == 2:
                                    x2 = x
                                    y2 = y - 1
                                    t2 = 1
                                elif t == 3:
                                    x2 = x + 1
                                    y2 = y
                                    t2 = 2
                            elif action[a] == 0:   # no turn
                                if t == 0:
                                    x2 = x - 1
                                    y2 = y
                                    t2 = t
                                elif t == 1:
                                    x2 = x
                                    y2 = y - 1
                                    t2 = t
                                elif t == 2:
                                    x2 = x + 1
                                    y2 = y
                                    t2 = t
                                elif t == 3:
                                    x2 = x
                                    y2 = y + 1
                                    t2 = t
                            elif action[a] == 1:   # left turn
                                if t == 0:
                                    x2 = x
                                    y2 = y - 1
                                    t2 = 1
                                elif t == 1:
                                    x2 = x + 1
                                    y2 = y
                                    t2 = 2
                                elif t == 2:
                                    x2 = x
                                    y2 = y + 1
                                    t2 = 3
                                elif t == 3:
                                    x2 = x - 1
                                    y2 = y
                                    t2 = 0

                            if x2 >= 0 and x2 < len(grid) and y2 >= 0 and y2 < len(grid[0]) and grid[x2][y2] == 0:
                                v2 = value[t2][x2][y2] + cost[a]

                                if v2 < value[t][x][y]:
                                    change = True
                                    value[t][x][y] = v2
                                    policy[t][x][y] = action_name[a]

    # set initial position and find 2D policy from 3D value matrix

    x = init[0]
    y = init[1]
    t = init[2]

    while 1:
        name = policy[t][x][y]
        policy2D[x][y] = name

        if name == 'R':    # right turn
            if t == 0:
                x = x
                y = y + 1
                t = 3
            elif t == 1:
                x = x - 1
                y = y
                t = 0
            elif t == 2:
                x = x
                y = y - 1
                t = 1
            elif t == 3:
                x = x + 1
                y = y
                t = 2
        elif name == '#':   # no turn
            if t == 0:
                x = x - 1
                y = y
                t = t
            elif t == 1:
                x = x
                y = y - 1
                t = t
            elif t == 2:
                x = x + 1
                y = y
                t = t
            elif t == 3:
                x = x
                y = y + 1
                t = t
        elif name == 'L':   # left turn
            if t == 0:
                x = x
                y = y - 1
                t = 1
            elif t == 1:
                x = x + 1
                y = y
                t = 2
            elif t == 2:
                x = x
                y = y + 1
                t = 3
            elif t == 3:
                x = x - 1
                y = y
                t = 0

        if goal[0] == x and goal[1] == y:
            policy2D[x][y] = '*'
            break

    return policy2D # Make sure your function returns the expected grid.

res = optimum_policy2D()

for i in range(len(res)):
    print res[i]
