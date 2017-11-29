import sys

def main():
    inputFile, outputFile = argCheck(sys.argv)
    sudoku = Board()
    print(sudoku.board)
    # for key,value in sudoku.board:
    #     print(key,value)
    # print(len(sudoku.board))

class Board:
    def __init__(self, board=81*"0"):
        print(len(board))
        self.board = createDict(board)
        self.domain = [i for i in range(1,10)]

    def ac3(self, X, domain, ):
        print("AC3")
    
    #def setBoard(board_string):
    #dict = {}
    #    for i in range(1,10):
    #        for j in range(1,10):
    #            pos = chr(64+i)+str(j)
    #            dict[pos] = board[(i-1)*10 + j-1]
    #    return dict
        


# create a sudoku board
def createDict(board):
    dict = {}
    for i in range(1,10):
        for j in range(1,10):
            pos = chr(64+i)+str(j)
            #print((i-1)*9 + j-1)
            dict[pos] = board[(i-1)*9 + j-1]
    return dict
    
# argument check
def argCheck(argv):
    if len(argv) != 3:
        exit("I need 2 arguments")
    
    return argv[1],argv[2]

if __name__ == "__main__":
    main()

