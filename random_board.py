# Create a Python program which performs A* search for the 8-puzzle problem (a-star.py)
# The purpose of this program is to determine a solution (sequential set of board configurations
# leading back to the goal configuration [[0, 1, 2], [3, 4, 5], [6, 7, 8]]

import sys, copy, heapq, math

# state class supplied by Dr. Phillips 
class state():
    def __init__(self, tiles):
        self.xpos = 0
        self.ypos = 0
        self.tiles = copy.deepcopy(tiles)
        self.findZero()

    # find the location of zero in the puzzle of the node
    def findZero(self):
        for i in range(3):
            for j in range(3):
                if self.tiles[i][j] == 0:
                    xpos = i
                    ypos = j
        self.xpos = xpos
        self.ypos = ypos
        return
    
    def left(self):
        if (self.ypos == 0):
            return None
        s = self
        s.tiles[s.xpos][s.ypos] = s.tiles[s.xpos][s.ypos-1]
        s.ypos -= 1
        s.tiles[s.xpos][s.ypos] = 0
        return s
    def right(self):
        if (self.ypos == 2):
            return None
        s = self
        s.tiles[s.xpos][s.ypos] = s.tiles[s.xpos][s.ypos+1]
        s.ypos += 1
        s.tiles[s.xpos][s.ypos] = 0
        return s
    def up(self):
        if (self.xpos == 0):
            return None
        s = self
        s.tiles[s.xpos][s.ypos] = s.tiles[s.xpos-1][s.ypos]
        s.xpos -= 1
        s.tiles[s.xpos][s.ypos] = 0
        return s
    def down(self):
        if (self.xpos == 2):
            return None
        s = self
        s.tiles[s.xpos][s.ypos] = s.tiles[s.xpos+1][s.ypos]
        s.xpos += 1
        s.tiles[s.xpos][s.ypos] = 0
        return s

# Set class provided by Dr. Phillips
class Set():
    def __init__(self):
        self.thisSet = set()
    def add(self,entry):
        if entry is not None:
            self.thisSet.add(entry.__hash__())
    def length(self):
        return len(self.thisSet)
    def isMember(self,query):
        return query.__hash__() in self.thisSet

# PriorityQueue class provided by Dr. Phillips
class PriorityQueue():
    def __init__(self):
        self.thisQueue = []
    def push(self, thisNode):
        heapq.heappush(self.thisQueue, (thisNode.f, -thisNode.id, thisNode))
    def pop(self):
        return heapq.heappop(self.thisQueue)[2]
    def isEmpty(self):
        return len(self.thisQueue) == 0
    def length(self):
        return len(self.thisQueue)

# node class
nodeid = 0
class node():
    def __init__(self, puzzle, parent):
        global nodeid
        self.id = nodeid
        nodeid += 1
        self.parent = parent
        self.puzzle = puzzle
        #create a one dimensional tuple of the puzzle
        self.tuple = tuple(sum(self.puzzle, []))
        # coordinates of each number in the goal nested list
        self.coord = {0:(0,0), 1:(1,0), 2:(2,0), 3:(0,1), 4:(1,1), 5:(2,1), 6:(0,2), 7:(1,2), 8:(2,2)}
        self.g = parent.g + 1 if parent is not None else 0
        self.f =  self.heuristic() + self.g

    # heuristic functions. The heuristic value given on command line determines
    # the heuristic to be used
    def heuristic(self):
        # if the heuristic is 0 then the heuristic value just the step cost value
        if h is 0:
            return 0
        # if the heuristic is 1 then the heuristic value is the number of tiles displaced 
        # from the goal + step cost
        elif h is 1:
            count = 0
            for i in range(3):
                for j in range(3):
                    if goal[i][j] != self.puzzle[i][j]:
                        count += 1
            return count
        # if the heuristic is 2 then the heuristic value is the sum of the Manhattan distance
        # + step cost
        elif h is 2:
            count = 0
            for i in range(3):
                for j in range(3):
                    xpos1, ypos1 = self.coord[self.puzzle[i][j]]
                    xpos2, ypos2 = self.coord[goal[i][j]]
                    count += abs(xpos1-xpos2) + abs(ypos1-ypos2)
            return count
        # if the heuristic is 3 then perform the novel heuristic
        # this heuristic is like the misplaced tile heuristic but instead of
        # every time it is just the ones along each diagonal of the box
        # essentially creating an X
        elif h is 3:
            count = 0
            if goal[0][0] != self.puzzle[0][0]:
                count += 1
            if goal[0][2] != self.puzzle[0][2]:
                count += 1
            if goal[1][1] != self.puzzle[1][1]:
                count += 1
            if goal[2][0] != self.puzzle[2][0]:
                count += 1
            if goal[2][2] != self.puzzle[2][2]:
                count += 1
            return count

    # is the puzzle of the node the goal? if so, f = 0, if not, f = h + g
    def isGoal(self):
        count = 0
        for i in range(3):
            for j in range(3):
                if goal[i][j] != self.puzzle[i][j]:
                    count += 1
        if count:
            return False
        else:
            return True

    #print the puzzle in the desired format
    def __str__(self):
        return '%d %d %d\n%d %d %d\n%d %d %d\n'%(
                self.puzzle[0][0],self.puzzle[0][1],self.puzzle[0][2],
                self.puzzle[1][0],self.puzzle[1][1],self.puzzle[1][2],
                self.puzzle[2][0],self.puzzle[2][1],self.puzzle[2][2])
    
    # print out the desired values and each state of the puzzle
    # in the desired format
    def display(self, V, N, d):
        reverse = []
        # traverse the path to the goal and add it to the reverse list
        # so that the nodes can be printed starting at the puzzle given to the goal
        while self.parent != None:
            reverse.append(self)
            self = self.parent
        reverse.append(self)

        if d is not 0:
            b = N**(1.0/d)
        else:
            b = 0

        # V = total nodes expanded, N = maximum nodes stared in memory (closed list + open lst),
        # d = depth of the solution, b = opproximate effective branching factor (N = b^d)
        # print the V, N, d, and b values
        print("V=%d\nN=%d\nd=%d\nb=%f\n" % (V, N, d, b))
        # print all the states of the puzzles from shuffled to goal
        while len(reverse):
            print(reverse.pop())

    #find the depth of the goal node
    def depth(self):
        count = 0
        while self.parent is not None:
            count += 1
            self = self.parent
        return count

# create the children of the parent node
def children(node):
    child = []
    
    # create a child state of the zero moved to the up
    up = state(node.puzzle)
    up = up.up()
    if up is not None:
        child.append(up)
    # create a child state of the zero moved to the down
    down = state(node.puzzle)
    down = down.down()
    if down is not None:
        child.append(down)
    # create a child state of the zero moved to the left
    left = state(node.puzzle)
    left = left.left()
    if left is not None:
        child.append(left)
    # create a child state of the zero moved to the right
    right = state(node.puzzle)
    right = right.right()
    if right is not None:
        child.append(right)
    
    return child


# perform the A* seearch
def aStar(root, puzzle):
    # create a closed list and open list (frontier) and add the first node to the frontier
    frontier = PriorityQueue()
    closed = Set()
    frontier.push(root)
    # while the frontier is empty, keep searching
    while not frontier.isEmpty():
        #set current equal to the node at the front of the queue
        current = frontier.pop()
        # if the current node is the goal, print out and end
        if current.isGoal():
            current.display(closed.length(), closed.length() + frontier.length(), current.depth())
            break
        # if the current node is not the goal, keep going
        else:
            # create a list of the children's puzzle states
            closed.add(current.tuple)
            moves = children(current)
            #for each puzzle state list of children, create their own node
            for item in moves:
                #create a tuple of the state return so that it can be check that its not
                # same orientation as it's parent
                itemsTiles = tuple(sum(item.tiles, []))
                #create a child node and add it to the frontier
                if not closed.isMember(itemsTiles):
                    child = node(item.tiles, current)
                    frontier.push(child)







# take in the heuristic value from the command line and create a nested list
# from the puzzle given
h = int(sys.argv[1])
goal = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
def main():
    numbers = sys.stdin.read()
    temp = list(map(int, numbers.split()))
    puzzle = [temp[i:i+3] for i in range(0, len(temp), 3)]

    #puzzle = [[6, 3, 4], [1, 0, 2], [7, 5, 8]]
        
    #create the root and pass it to the aStar function and begin searching
    root = node(puzzle, None)
    aStar(root, puzzle)
main()
