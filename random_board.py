import sys, copy, random

class state():
    def __init__(self, tiles):
        self.xpos = 0
        self.ypos = 0 
        self.tiles = copy.deepcopy(tiles)
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
    def __str__(self):
        return '%d %d %d\n%d %d %d\n%d %d %d\n'%(
                self.tiles[0][0],self.tiles[0][1],self.tiles[0][2],
                self.tiles[1][0],self.tiles[1][1],self.tiles[1][2],
                self.tiles[2][0],self.tiles[2][1],self.tiles[2][2])

def main():
    #read in the random seed and number of moves to be performed
    random.seed(int(sys.argv[1]))
    number_of_moves = int(sys.argv[2])

    # read in the goal orientation and turn it into a nested list
    numbers = sys.stdin.read()
    temp    = list(map(int, numbers.split()))
    puzzle  = [temp[i:i+3] for i in range(0, len(temp), 3)]
    start   = state(puzzle)

    # move the 0 around within the puzzle the desired number of times
    for x in range(number_of_moves):
        move = random.randrange(4) 
        if move is 0:
            start.up()
        elif move is 1:
            start.down()
        elif move is 2:
            start.left()
        elif move is 3:
            start.right()

    #print the puzzle
    print(start)

main()
