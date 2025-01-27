#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, copy, heapq, math

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
        self.h = self.heuristic() if h is not 0 else 0
        self.f =  self.h + self.g

    # heuristic functions. The heuristic value given on command line determines
    # the heuristic to be used
    def heuristic(self):
        # if the heuristic is 1 then the heuristic value is the number of tiles displaced 
        # from the goal state
        if h is 1:
            count = 0
            for i in range(3):
                for j in range(3):
                    if goal[i][j] != self.puzzle[i][j]:
                        count += 1
            return count
        # if the heuristic is 2 then the heuristic value is the sum of the Manhattan distance
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

    # check if the puzzle being passed is the goal
    def isGoal(self):
        for i in range(3):
            for j in range(3):
                if goal[i][j] != self.puzzle[i][j]:
                    return False
        return True

     #find the depth of the goal node
    def depth(self):
        count = 0
        while self.parent is not None:
            count += 1
            self = self.parent
        return count
    
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

        # use the formula to calculate b is d is not 0
        # to avoid errors
        if d is not 0:
            b = N**(1.0/d)
        else:
            b = 0

        # V = total nodes expanded, N = maximum nodes stared in memory (closed list + open lst),
        # d = depth of the solution, b = opproximate effective branching factor (N = b^d)
        # print the V, N, d, and b values
        print("V=%d\nN=%d\nd=%d\nb=%.5f\n" % (V, N, d, b))
        # print all the states of the puzzles from shuffled to goal
        while len(reverse):
            print(reverse.pop())
        
        #print the puzzle in the desired format
    def __str__(self):
        return '%d %d %d\n%d %d %d\n%d %d %d\n'%(
                self.puzzle[0][0],self.puzzle[0][1],self.puzzle[0][2],
                self.puzzle[1][0],self.puzzle[1][1],self.puzzle[1][2],
                self.puzzle[2][0],self.puzzle[2][1],self.puzzle[2][2])


# create the children of the parent node
def children(node):
    child = []
    
    # create a child state of the zero moved to the up
    upState = state(node.puzzle)
    up = upState.up()
    if up is not None:
        child.append(up)
    # create a child state of the zero moved to the down
    downState = state(node.puzzle)
    down = downState.down()
    if down is not None:
        child.append(down)
    # create a child state of the zero moved to the left
    leftState = state(node.puzzle)
    left = leftState.left()
    if left is not None:
        child.append(left)
    # create a child state of the zero moved to the right
    rightState = state(node.puzzle)
    right = rightState.right()
    if right is not None:
        child.append(right)
    
    return child

# perform the A* seearch
def aStar(root, puzzle):
    # create a closed list and open list (frontier) and add the first node to the frontier
    frontier = PriorityQueue()
    closed = Set()
    frontier.push(root)
    # while the frontier is not empty, keep searching
    while not frontier.isEmpty():
        #set current equal to the node at the front of the queue
        current = frontier.pop()
        # if the current node is the goal, print out and end
        if current.isGoal():
            current.display(closed.length(), closed.length() + frontier.length(), current.depth())
            break
        # if the current node is not the goal, keep going
        else:
            # add the current node to the closed list
            closed.add(current.tuple)
            # create a list of the children's puzzle states
            moves = children(current)
            #for each puzzle state list of children, create their own node
            for item in moves:
                # reate a tuple of the state return so that it can be check that its not
                # same orientation as it's parent
                itemsTiles = tuple(sum(item.tiles, []))
                # create a child node and add it to the frontier if the child's state
                # is not already a state of a parent
                if not closed.isMember(itemsTiles):
                    child = node(item.tiles, current)
                    frontier.push(child)


# take in the heuristic value from the command line
h = int(sys.argv[1])
# goal puzzle orientation
goal = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
def main():
    # turn the shuffled puzzle from stdin to a nested list
    numbers = sys.stdin.read()
    temp = list(map(int, numbers.split()))
    puzzle = [temp[i:i+3] for i in range(0, len(temp), 3)]
        
    #create the root and pass it to the aStar function and begin searching
    root = node(puzzle, None)
    aStar(root, puzzle)
    
main()
