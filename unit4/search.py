# my search version

# ----------
# User Instructions:
# 
# Define a function, search() that takes no input
# and returns a list
# in the form of [optimal path length, x, y]. For
# the grid shown below, your function should output
# [11, 4, 5].
#
# If there is no valid path from the start point
# to the goal, your function should return the string
# 'fail'
# ----------

# Grid format:
#   0 = Navigable space
#   1 = Occupied space

grid = [[0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 0],
        [0, 0, 1, 1, 1, 0],
        [0, 0, 0, 0, 1, 0]]

init = [0, 0]
goal = [len(grid)-1, len(grid[0])-1] # Make sure that the goal definition stays in the function.

delta = [[-1, 0 ], # go up
        [ 0, -1], # go left
        [ 1, 0 ], # go down
        [ 0, 1 ]] # go right

delta_name = ['^', '<', 'v', '>']

cost = 1

def search():
    open = [[0, init[0], init[1]]]
    expanded = []

    while 1:
        #print "open list: ", open

        ### check step: did we reach the goal ?
        for i in range(len(open)):
            if open[i][1] == goal[0] and open[i][2] == goal[1]:
                return open[i]

        ### expand step

        # prepare updated open list
        new_open = [x for x in open]

        # find node with minimal g-value
        node = min(new_open)
        new_open.remove(node)

        #print "node with minimal g: ", node

        # add this node to expanded list
        expanded.append([node[1], node[2]])

        # expand node with minimal g-value
        for i in range(len(delta)):

            # check bounds and fences
            if node[1] + delta[i][0] < 0 or node[1] + delta[i][0] > len(grid) - 1:
                continue
            if node[2] + delta[i][1] < 0 or node[2] + delta[i][1] > len(grid[0]) - 1:
                continue
            if grid[node[1] + delta[i][0]][node[2] + delta[i][1]] == 1:
                continue

            # check if such element is already in open list
            if [node[1] + delta[i][0], node[2] + delta[i][1]] in [[x[1], x[2]] for x in new_open]:
                continue

            # check if such element already was expanded
            if [node[1] + delta[i][0], node[2] + delta[i][1]] in expanded:
                continue

            new_open.append([node[0] + cost, node[1] + delta[i][0], node[2] + delta[i][1]])

        ### everything discovered: no goal
        if new_open == []:
            return "fail"

        open = new_open

# main:
print search()

