import sys
import argparse

def main():
    # argument parsing part
    parser = argparse.ArgumentParser()
    parser.add_argument("inputFile", help="file contaning sudoku strings, 0 for empty squares")
    parser.add_argument("outputFile", help="the file which solutions are going to be written to")
    parser.add_argument("-d","--display", help="display each solution", action="store_true")
    args = parser.parse_args()

    inputFile, outputFile = args.inputFile, args.outputFile
    display = True if args.display else False
    sudoku = Sudoku()
    grids = []
    solutions = []
    final = []

    # open file and read all input strings
    with open(inputFile) as inputF:
        for line in inputF:
            gridString = line.split(' ')[0][:-1]
            grids.append(gridString)

    # solve sudokus and store the solutions
    for i,grid in enumerate(grids):
        sudoku.setGrid(grid)
        sudoku.backTrack()
        solutions.append(sudoku.getFinalGridString())
        if display:
            print("Sudoku No. "+str(i+1))
            print(sudoku)

    # write the solutions to the output file
    with open(outputFile, "w") as solstxt:
        for sol in solutions:
            solstxt.write(sol+"\n")

class Sudoku():
    def __init__(self, gridString =81*"0"):
        self.digits      = '123456789'
        self.rows        = 'ABCDEFGHI'
        self.cols        = self.digits
        self.orderedKeys = dotProduct(self.rows, self.digits)
        self.gridString  = gridString
        self.values      = parseGridString(self.orderedKeys, gridString)
        self.domains     = getDomains(self.values, self.digits)
        self.squares     = [dotProduct(a, b) for a in ('ABC','DEF','GHI') for b in ('123','456','789')]
        self.neighbors   = getNeighbors(self.orderedKeys, self.digits, self.rows, self.squares)

    # print sudoku board with good formatting and seperators
    def __repr__(self):
        width = 1+max(len(self.values[s]) for s in self.values)
        seperator = '+'.join(['-'*(width*3)]*3)
        string = ""
        for row in self.rows:
            string+=''.join([self.values[row+col].center(width)+('|' if col in '36' else '') for col in self.cols])
            string+="\n"
            if row in 'CF':
                string+=seperator+'\n'
        return string

    # solve sudoku using the Backtracking algorithm
    def backTrack(self):
        if self.isFull():
            return True # we're done here

        key = self.getFirstEmpty()
        # for every possible value of key, check if it satifies the constraints
        for val in self.digits:
            if self.satisfiesConstraints(key, val):
                self.values[key] = val # if yes, use the value
                if self.backTrack():   # move to the next variable with recursion
                    return True
                self.values[key] = '0' # remove previous value and try again

        return False # triggers backtracking

    # returns true if the key value pair satisfies all constraints, else returns False
    def satisfiesConstraints(self, key, val):
        for k in self.neighbors[key]:
            if self.values[k] == val:
                return False
        return True

    # return the first unassigned variable key
    def getFirstEmpty(self):
        for key in self.orderedKeys:
            if self.values[key] == '0':
                return key

    # returns false if there is at least one unassigned variable, else the grid is full
    def isFull(self):
        result =  False if any(self.values[key] == '0' for key in self.values) else True
        return result

    # set the grid values to the gridString provided
    def setGrid(self, gridString):
        self.gridString = gridString
        self.values = parseGridString(self.orderedKeys, gridString)

    # return the gridString of the solved Sudoku
    def getFinalGridString(self):
        gridString = ""
        for key in self.orderedKeys:
            gridString += self.values[key]
        return gridString

# Dot product of elements in A and elements in B.
def dotProduct(A,B):
    return [a+b for a in A for b in B]

# creates and returns a dict that contains key:value pairs, for every key the value is a list of
# all the neighbors/arcs that need to satisfy the AllDiff constraint, meaning : they all must have different values
def getNeighbors(orderedKeys, digits, rows, squares):
    square = []
    neighbors = {}
    for key in orderedKeys:
        rowKeys = dotProduct(key[0], digits) # get the cell's row
        colKeys = dotProduct(rows, key[1])   # get the cell's column

        # get the cell's square
        for sqr in squares:
            if key in sqr:
                square = sqr
                break

        constraints = rowKeys + square + colKeys # sum'em up
        constraints = list(filter((key).__ne__, constraints)) # remove all instances of key, because the key's value cannot be different from itself
        neighbors[key] = constraints
    return neighbors


# Returns a dict containing variable:domain pair, the domains are all the possible values for that
# variable if its not assigned any value, else it is its value.
def getDomains(values, digits):
    domains = {key: digits if values[key] == '0' else values[key] for key in values}
    return domains

# Returns a dict containing variable:value pair, all values are described in gridString string.
def parseGridString(orderedKeys, gridString):
    grid = {}
    for i, key in enumerate(orderedKeys):
        grid[key] = gridString[i]
    return grid

if __name__ == "__main__":
    main()
