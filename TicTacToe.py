import random
import time

"""
Comtek første semester opgave.

Programmet er blevet forholdsvist langt, og kan nok simplificeres på mange måder. Koden er delt op i regioner, så de nemt kan pakkes sammen for bedre læselighed (også så de arme medstuderende der skal vurdere det ikke skal læse 500 linjer kode)

Det gør brug af klasser, som ikke er noget vi decideret har lært om endnu, men jeg håber alligevel det er let forståeligt.

Lidt om programmets features:
 - Det er muligt at spille mod en computerstyret modstander

 - Hvis du ændrer i koden, så er der fuld funktionalitet til at øge størrelsen af brættet. 
   Computer-modspilleren er dog ikke særlig god til at spille på større bræt - men den kan godt. 
   Du skal ændre variablen "enableBoardSizeChoice" til "True".
"""

# region classes
class Player(object):
    """Holds data about the player"""
    def __init__(self, symbol, opponentSymbol, isAI):
        self.symbol = symbol
        self.opponentSymbol = opponentSymbol
        self.isAI = isAI

class Board:
    """Holds data about the board"""
    def __init__(self, size):
        self.size = size
        self.data = []
        self.totalSquares = size * size
    
    def PopulateEmptyBoard(self):
        boardCounter = 1
        self.data.clear()
        for x in range(self.size):
            self.data.append([])
            for y in range(self.size):
                self.data[x].append(boardCounter)
                boardCounter = boardCounter + 1
        
# endregion

# region Variables
enableBoardSizeChoice = False #If true lets the players choose board size
players = [] #A list of players
currentPlayer = -1
# endregion

# region AI
def EvaluateAllSpaces():
    """Main AI function. Evaluates all spaces, and picks a move"""
    global board
    spaceRatings = []

    print("The AI chooses...")

    for row in range(board.size):
        for column in range(board.size):
            if ValidateMove(row, column):
                spaceRatings.append(EvaluateSpace(row, column))
    
    move = PickMove(spaceRatings)
    time.sleep(0.5)
    ExecuteMove(move[0], move[1])

def EvaluateSpace(x, y):
    """Scans the board, and gives a rating to each square."""
    global board
    global currentPlayer
    global players
    ratingColumnSelf = 0
    ratingColumnOther = 0
    ratingColumn = 0
    ratingRowSelf = 0
    ratingRowOther = 0
    ratingRow = 0

    #checks verticaly for which spaces are taken
    for column in range(board.size):
        if column != y:
            if type(board.data[x][column]) != int:
                if board.data[x][column] == players[currentPlayer].opponentSymbol:
                    ratingColumnOther += 1
                elif board.data[x][column] == players[currentPlayer].symbol:
                    ratingColumnSelf += 1
    if ratingColumnSelf == board.size - 1:
        return (x,y,board.size * 3)
    elif ratingColumnOther == board.size - 1:
        return (x,y,board.size * 2)
    ratingColumn = ratingColumnSelf - ratingColumnOther

    # checks horizontall for which spaces are taken
    for row in range(board.size):
        if row != x:
            if type(board.data[row][y]) != int:
                if board.data[row][y] == players[currentPlayer].opponentSymbol:
                    ratingRowOther += 1
                elif board.data[row][y] == players[currentPlayer].symbol:
                    ratingRowSelf += 1
    if ratingRowSelf == board.size - 1:
        return (x,y,board.size * 3)
    elif ratingRowOther == board.size - 1:
        return (x,y,board.size * 2)
    ratingRow = ratingRowSelf - ratingRowOther

    if (CheckImpendingDiagonalWin(x, y)):
        return (x,y, board.size * 3)
    if (CheckImpendingDiagonalLoss(x,y)):
        return (x,y, board.size * 2)


    return (x, y, ratingRow + ratingColumn)

def CheckImpendingDiagonalWin(x, y):
    """Ai logic: check if any player is only one placement diagonally from winning, and returns true if so"""
    #Checks if a placement here will win diagonally (upper left corner to bottom right)
    global players
    global currentPlayer

    isOnThisDiagonal = False
    counter = 0
    for i in range(board.size):
        if x == i and y == i:
            isOnThisDiagonal = True
        if board.data[i][i] == players[currentPlayer].symbol:
            counter += 1
    if counter == board.size - 1  and isOnThisDiagonal == True:
        return True
    isOnThisDiagonal = False

    #Checks if a placement here will win diagonally (upper right corner to bottom left)
    counter = 0
    yValue = 0
    for i in range(board.size-1, -1, -1):
        if x == i and y == yValue:
            isOnThisDiagonal = True
        if board.data[i][yValue] == players[currentPlayer].symbol:
            counter += 1
        yValue += 1
    if counter == board.size - 1 and isOnThisDiagonal == True:
        return True
    return False

def CheckImpendingDiagonalLoss(x, y):
    """Ai logic: check if any player is only one placement diagonally from losing, and returns true if so"""
    global players
    global currentPlayer
    isOnThisDiagonal = False
    #Checks if a placement here would stop the other player from winning diagnoally (upper left corner to bottom right)
    
    counter = 0
    for i in range(board.size):
        if x == i and y == i:
            isOnThisDiagonal = True
        if board.data[i][i] == players[currentPlayer].opponentSymbol:
            counter += 1
    if counter == board.size - 1  and isOnThisDiagonal == True:
        return True
    isOnThisDiagonal = False

    #Checks if a placement here would stop the other player from winning diagnoally(upper right corner to bottom left)
    counter = 0
    yValue = 0
    for i in range(board.size-1, -1, -1):
        if x == i and y == yValue:
            isOnThisDiagonal = True
        if board.data[i][yValue] == players[currentPlayer].opponentSymbol:
            counter += 1
        yValue += 1
    if counter == board.size - 1  and isOnThisDiagonal == True:
        return True
    return False

def PickMove(ratings):
    """Picks a square, based on the ratings. If multiple are tied, pick one at random"""
    # determine highest value
    highestValue = 0
    for value in ratings:
        if value[2] > highestValue:
            highestValue = value[2]
    
    if highestValue == 0:
        return ratings[random.randint(0, len(ratings)-1)]

    # new list of tuples with that value
    equivelantMoves = []
    for value in ratings:
        if value[2] == highestValue:
            equivelantMoves.append(value)
    # choose randomly from list
    
    if len(equivelantMoves) == 1:
        return equivelantMoves[0]
    return equivelantMoves[random.randint(0, len(equivelantMoves)-1)]
# endregion

# region Move logic
def ExecuteNextTurn():
    """Is called continually, and increments which player is active."""
    global currentPlayer
    global players
    currentPlayer += 1
    if currentPlayer >= len(players):
        currentPlayer = 0

    if players[currentPlayer].isAI:
        EvaluateAllSpaces()
    else:
        AwaitUserInput()

def ValidateMove(targetRow, targetColumn):
    """Validates whether the square is already taken"""
    global board
    
    if type(board.data[targetRow][targetColumn]) == type("string"):
        return False

    return True

def ExecuteMove(targetRow, targetColumn):
    """Perfoms the move, prints the board and checks if anyone won"""
    global currentPlayer
    global board
    global players

    board.data[targetRow][targetColumn] = players[currentPlayer].symbol

    PrintBoard()
    
    if CheckVictory():
        Victory()
# endregion
    
# region Evaluate game ending
def Victory():
    """Displays the winner and gives the player the chance to play again"""
    global currentPlayer
    global players
    global board
    
    print(f"{players[currentPlayer].symbol} has won!")
    input("Press enter to play again...")
    InitializeGame()


def CheckVictory():
    """If any victory condition is fulfilled, return true"""
    if CheckHorizontalVictory() or CheckVerticalVictory() or CheckDiagonalVictory() or CheckStalemate():
        return True
    return False
    
def CheckVerticalVictory():
    """If a player has attained victory with vertical placements, return true. Else, return false"""
    global currentPlayer
    global board
    
    for columns in range(board.size):
        counter = 0
        for rows in range(board.size):
            if board.data[rows][columns] == players[currentPlayer].symbol:
                counter += 1
        if counter == board.size:
            print("Victory by vertical!")
            return True
    return False
    
def CheckHorizontalVictory(): 
    """If a player has attained victory with horizontal placements, return true. Else, return false"""
    global currentPlayer
    global board
    
    for rows in range(board.size):
        counter = 0
        for columns in range(board.size):
            if board.data[rows][columns] == players[currentPlayer].symbol:
                counter += 1
        if counter == board.size:
            print("Victory by horizontal!")
            return True
    return False

def CheckDiagonalVictory():
    """If a player has attained diagonal victory with vertical placements, return true. Else, return false"""
    global currentPlayer
    global board

    counter = 0
    for x in range(board.size):
        if board.data[x][x] == players[currentPlayer].symbol:
            counter += 1
    if counter == board.size:
        print("Victory by diagonal!")
        return True
    
    counter = 0
    yValue = 0
    for x in range(board.size-1, -1, -1):
        if board.data[x][yValue] == players[currentPlayer].symbol:
            counter += 1
        yValue += 1
    if counter == board.size:
        print("Victory by diagonal!")
        return True
        
    return False
    
def CheckStalemate():
    """Ends the game if all squares are taken"""
    global board

    for row in range(board.size):
        for column in range(board.size):
            if type(board.data[row][column]) == int:
                return
    
    print("Stalemate")
    input("Press enter to play again...")
    InitializeGame()
# endregion

# region Utilities
def PrintBoard():
    """Prints the current board"""
    global board

    rowString = ""
    
    if board.totalSquares > 9:
        for row in range(board.size):
            print("-" * 5 + "-" * 4 * board.size)
            rowString = "| "
            for column in range(board.size):
                if row * board.size + column < 9 or type(board.data[row][column]) == str:
                    rowString = rowString + f"{board.data[row][column]}  | "
                else:
                    rowString = rowString + f"{board.data[row][column]} | "
            print(rowString)
        print("-" * 5 + "-" * 4 * board.size) # Printer nederste række.
    else:
        for row in range(board.size):
            print("-" * 4 + "-" * 3 * board.size)
            rowString = "| "
            for column in range(board.size):
                rowString = rowString + f"{board.data[row][column]} | "
            print(rowString)
        print("-" * 4 + "-" * 3 * board.size) # Printer nederste række.
# endregion

# region input
def AwaitUserInput():
    """Reads the user input until a valid position is given"""
    global currentPlayer
    
    move = input(f"Waiting for {players[currentPlayer].symbol} player move...\n")
    if ValidateMoveInput(move) == True:
        boardCoordinate = InputToBoardCoordinate(move)
        if ValidateMove(boardCoordinate[0], boardCoordinate[1]) == True:
            ExecuteMove(boardCoordinate[0], boardCoordinate[1])
        else:
            print("Square is already taken")
            AwaitUserInput()
    else:
        AwaitUserInput()

def ValidateMoveInput(input):
    """Validates whether the input is valid, in terms of input. Returns true if input is valid"""
    if input.isnumeric() == False:
        print("Input must be a whole number")
        return False
    
    if int(input) == 0 or int(input)-1 > board.totalSquares:
        print(f"Input must be a number from 1 - {board.totalSquares}")
        return False
    
    return True

def InputToBoardCoordinate(input):
    """Takes an input number, and returns the board coordinate"""
    global board

    counter = 0
    for row in range(board.size):
        for column in range(board.size):
            counter += 1
            if counter == int(input):
                return (row, column)

def QuestionAI():
    """Asks the player whether they want to play against AI or a human"""
    global againstAI
    
    inp = input("Play against AI? y/n\n")
    evaluatedInput = EvaluateYesNo(inp)

    if type(evaluatedInput) == type("string"):
        print("Not a valid input")
        QuestionAI()
        return

    againstAI = evaluatedInput
    return(againstAI)

def PlayerChooseSymbol():
    """If playing against AI, evaluates whether the player should be X or O"""
    inp = input("Play as X? y/n\n")
    evaluatedInput = EvaluateYesNo(inp)

    if type(evaluatedInput) == str:
        print("Not a valid input")
        PlayerChooseSymbol()
        return
    
    
    if evaluatedInput:
        print("Player is X. The AI makes the first move...")
        return "X"
    else:
        print("Player is O. You will make the first move...")
        return "O"


def EvaluateYesNo(input):
    """Returns true if the first letter is y, returns false if the first letter is n. 
    Returns a string if neither is true"""
    if input.lower()[0] == "y":
        return True
    elif input.lower()[0] == "n":
        return False
    else:
        return "invalid"
    
def ChooseBoardSize(inp):
    """Validates the chosen boardsize"""
    if inp.isnumeric == False:
        return ChooseBoardSize(input("That wasn't a number, try again\n"))
    elif 3 <= int(inp):
        return int(inp)    
    else:
        return ChooseBoardSize(input("The size of the board must be greater than 2. Try again\n"))

    
# endregion

def InitializeGame():
    """Initializes the game - resets values if a previous game was played"""
    

    global currentPlayer
    global board

    if enableBoardSizeChoice:
        boardSize = ChooseBoardSize(input("Which size should the board be?\n"))
        board = Board(boardSize)
    else:
        board = Board(3)
    board.PopulateEmptyBoard()

    players.clear()

    isAgainstAI = QuestionAI()
    if isAgainstAI:
        if PlayerChooseSymbol() == "O":
            players.append(Player("O", "X", False))
            players.append(Player("X", "O", True))
        else:
            players.append(Player("O", "X", True))
            players.append(Player("X", "O", False))
    else:
        players.append(Player("O", False))
        players.append(Player("X", False))

    PrintBoard()

    currentPlayer = -1   

InitializeGame() #Initializes the game
while True: #Runs forever, makes sure the game doesn't stop
    ExecuteNextTurn()
    