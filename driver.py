def main():
    sudoku = Board()
    # for key,value in sudoku.board:
    #     print(key,value)
    # print(len(sudoku.board))

class Board:
    def __init__(self, board=str([0*81])):
        self.board = createDict(board)
        self.domain = [i for i in range(1,10)]

    def ac3(self, X, domain, ):
        print("AC3")


# create a sudoku board
def createDict(board):
    dict = {}
    for i in range(1,10):
        for j in range(1,10):
            pos = chr(64+i)+str(j)
            dict[pos] = board[(i-1)*10 + j-1]
    return dict

if __name__ == "__main__":
    main()

