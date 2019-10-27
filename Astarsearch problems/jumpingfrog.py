import search
import random

class FrogPuzzleState:

    def __init__(self, numbers):
        self.cells = numbers[:]
        self.blankLocation = self.cells.index(0)

    def isGoal(self):
        goal = [2,2,2,0,1,1,1]
        if self.cells == goal:
            return True
        return False
    def legalMoves(self):
        moves = []
        row = self.blankLocation #index of 0
        if (row + 1)<=len(self.cells)-1:
            moves.append('right')
        if (row + 2)<=len(self.cells)-1:
            moves.append('double_right')
        if (row - 1)>=0:
            moves.append('left')
        if (row - 2)>=0:
            moves.append('double_left')
        return moves

    def result(self, move):
        row = self.blankLocation
        if (move == 'double_left'):
            newrow = row - 2
        elif (move == 'double_right'):
            newrow = row + 2
        elif (move == 'left'):
            newrow = row -1
        elif (move == 'right'):
            newrow = row + 1
        else:
            raise "Illegal Move"

        # Create a copy of the current eightPuzzle
        newPuzzle = FrogPuzzleState([0, 0, 0, 0, 0, 0, 0, 0, 0])
        newPuzzle.cells = self.cells.copy()
        # And update it to reflect the move
        newPuzzle.cells[row] = self.cells[newrow]
        newPuzzle.cells[newrow] = self.cells[row]
        newPuzzle.blankLocation = newrow
        #print (newPuzzle)
        return newPuzzle

    # Utilities for comparison and display
    def __eq__(self, other):
        if other == None:
            return False
        if self.cells != other.cells:
            return False
        return True

    def __hash__(self):
        return hash(str(self.cells))

    def __getAsciiString(self):
        rowLine = ''
        for row in self.cells:
            if row == 0:
                dsp = '-'
            elif row == 1:
                dsp = 'G'
            elif row == 2:
                dsp = 'R'
            rowLine = rowLine + dsp
        return rowLine

    def __str__(self):
        return self.__getAsciiString()

class FrogPuzzleSearchProblem(search.SearchProblem):

    def __init__(self, puzzle):
        "Creates a new FrogPuzzleSearchProblem which stores search information."
        self.puzzle = puzzle

    def getStartState(self):
        return puzzle

    def isGoalState(self, state):
        return state.isGoal()

    def getSuccessors(self, state):
        succ = []
        for a in state.legalMoves():
            if a == 'right' or a == 'left':
                succ.append((state.result(a), a, state, 1))
            elif a == 'double_right' or a == 'double_left':
                succ.append((state.result(a), a, state, 2))
        return succ

    def getCostOfActions(self, actions):
        cost = 0
        for a in actions:
            if a == 'right' or a == 'left':
                cost += 1
            elif a == 'double_right' or a == 'double_left':
                cost += 2
        return cost

    def getHeuristic(self, state):  # misplaced tiles
        # goal = [2, 2, 2, 0, 1, 1, 1]
        h = 0
        for i in range(len(state.cells)):
            if state.cells[i]==2 and i>2:
                h+=1
            elif state.cells[i]==0 and i!=3:
                h+=1
            elif state.cells[i]==1 and i<3:
                h+=1
        return h

FROG_PUZZLE_DATA = [[1, 1, 1, 0, 2, 2, 2],
                    [1, 2, 0, 1, 2, 1, 2],
                    [2, 1, 2, 2, 1, 1, 0],
                    [2, 2, 0, 1, 1, 1, 2],
                    [1, 2, 2, 2, 1, 1, 0],
                    [2, 2, 2, 1, 1, 1, 0]]


def loadFrogPuzzle(puzzleNumber):
    return FrogPuzzleState(FROG_PUZZLE_DATA[puzzleNumber])


def createRandomFrogPuzzle(moves=100):
    puzzle = FrogPuzzleState([0,1,1,1,2,2,2])
    for i in range(moves):
        # Execute a random legal move
        puzzle = puzzle.result(random.sample(puzzle.legalMoves(), 1)[0])
    return puzzle


# Main program
#puzzle = loadFrogPuzzle(1)
puzzle = createRandomFrogPuzzle(1)
problem = FrogPuzzleSearchProblem(puzzle)
path = search.aStarSearch(problem)

#print(path)
for i in path:
    print(i)
print('Search found a path of %d moves: ' % (len(path)))
