# Minesweeper Terminal
import random
import re 

class Board:

    def __init__(self, size, bombs):
        self.bombs = bombs
        self.size = size
        self.dug = set()

        self.createBoard()
        self.assignValues()

        
    def createBoard(self):
        self.board = [[0 for row in range(self.size)] for col in range(self.size)]

        bombsPlanted = 0

        while bombsPlanted < self.bombs:
            row = random.randint(0,self.size-1)
            col = random.randint(0,self.size-1)

            if self.board[row][col] == '*':
                continue
            
            self.board[row][col] = '*'
            bombsPlanted += 1

    def assignValues(self):
        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] != '*':
                    self.board[row][col] = self.getNumNeighbouringBombs(row,col)


    def getNumNeighbouringBombs(self, row, col):
        # top left: (row-1, col-1)
        # top middle: (row-1, col)
        # top right: (row-1, col+1)
        # left: (row, col-1)
        # right: (row, col+1)
        # bottom left: (row+1, col-1)
        # bottom middle: (row+1, col)
        # bottom right: (row+1, col+1)

        neighbouringBombs = 0
        for x in range(max(0, row - 1), min(self.size -1, row + 1) + 1):
            for y in range(max(0, col - 1), min(self.size - 1, col + 1) + 1):
                if self.board[x][y] == '*':
                    neighbouringBombs += 1

        return neighbouringBombs
         
    def welcome(self):
        print("WELCOME TO MINESWEEPER")

    def displayBoard(self):
        visibleBoard = [['?' for row in range(self.size)] for col in range(self.size)]

        for row in range(self.size):
            for col in range(self.size):
                if (row, col) in self.dug:
                    visibleBoard[row][col] = str(self.board[row][col])
                else:
                    visibleBoard[row][col] = '?'

        for row in visibleBoard:
            print(" ".join(str(cell) for cell in row))

    def dig(self, row, col):
        self.dug.add((row,col))

        if self.board[row][col] == '*':
            print("GAME OVER")
            return False
        elif self.board[row][col] > 0:
            return True
        
        # If there are no neighbouring bombs then keep digging!
        for x in range(max(0, row-1), min(self.size-1, row + 1) + 1):
            for y in range(max(0, col - 1), min(self.size - 1, col + 1) + 1):
                if (x,y) in self.dug:
                    # location has been dug
                    continue
                else:
                    self.dig(x,y)
                    

def play(size=10, bombs=4):

    # Create board
    board = Board(size, bombs)
    board.welcome()
    board.displayBoard()

    # Ask where user wants to dig
    safe = True

    while len(board.dug) < board.size ** 2 - bombs:
        # board.displayBoard()

        userInput = re.split(',(\\s)*', input("Where would you like to dig? Enter as row,col: "))
        row, col = int(userInput[0]), int(userInput[-1])
        # print(row, col)
        if row < 0 or row >= board.size or col < 0 or col >= board.size:
            print("Out of Bounds. Try again.")
            continue

        # if it is valid, start to dig
        safe = board.dig(row, col)
        if not safe:
            break
        else:
            board.displayBoard()

    # Check if they won
    if safe:
        print("Congratulations! You have defused all the bombs!")
    else:
        print("Sorry! Game Over :(")
        # Reveal board
        board.dug = [(row, col) for row in range(board.size) for col in range(board.size)]

        board.displayBoard()


            
def main():
    play(6,2)

if __name__ == "__main__":
    main()