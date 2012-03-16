# my version of policy calculation: differs from class example

# ----------
# User Instructions:
# 
# Create a function compute_value() which returns
# a grid of values. Value is defined as the minimum
# number of moves required to get from a cell to the
# goal. 
#
# If it is impossible to reach the goal from a cell
# you should assign that cell a value of 99.

# ----------

grid = [[0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 1, 1],
        [0, 1, 0, 0, 0, 0]]

init = [0, 0]
goal = [len(grid)-1, len(grid[0])-1]

delta = [[-1, 0 ], # go up
         [ 0, -1], # go left
         [ 1, 0 ], # go down
         [ 0, 1 ]] # go right

delta_name = ['^', '<', 'v', '>']

cost_step = 1 # the cost associated with moving from a cell to an adjacent one.

# ----------------------------------------
# insert code below
# ----------------------------------------

def optimum_policy():
    policy = [[' ' for row in range(len(grid[0]))] for col in range(len(grid))]
    value = [[99 for row in range(len(grid[0]))] for col in range(len(grid))]
    close = [[0 for row in range(len(grid[0]))] for col in range(len(grid))]

    x = goal[0]
    y = goal[1]

    delta_name_inv = ['v', '>', '^', '<']
    policy[x][y] = '*'
    value[x][y] = 0
    close[x][y] = 1

    open = [[0, x, y]]

    while len(open) > 0:
            open.sort()
            open.reverse()
            next = open.pop()

            v = next[0]
            x = next[1]
            y = next[2]

            for i in range(len(delta)):
                x2 = x + delta[i][0]
                y2 = y + delta[i][1]
                if x2 >= 0 and x2 < len(grid) and y2 >=0 and y2 < len(grid[0]):
                    if close[x2][y2] == 0 and grid[x2][y2] == 0:
                        v2 = v + 1
                        open.append([v2, x2, y2])
                        close[x2][y2] = 1
                        value[x2][y2] = v2
                        policy[x2][y2] = delta_name_inv[i]

    return value, policy

val, pol = optimum_policy()

for e in range(len(val)):
    print val[e]

print " "

for e in range(len(pol)):
    print pol[e]
