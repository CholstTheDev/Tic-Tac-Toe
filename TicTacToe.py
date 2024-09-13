import random

# region Variables
isXTurn = False
currentPlayer = "O"
board = []
boardSize = 6
totalSquares = boardSize * boardSize # hvor mange felter der er på banen. Skal genereres.

againstAI = True
playerIsX = False
# endregion

# region AI logic
def EvaluateAllSpaces():
    global boardSize
    spaceRatings = []

    print("The AI chooses...")

    for row in range(boardSize):
        for column in range(boardSize):
            if ValidateMove(row, column):
                spaceRatings.append(EvaluateSpace(row, column))
    
    move = PickMove(spaceRatings)
    ExecuteMove(move[0], move[1])

def EvaluateSpace(x, y):
    
    rating = 0

    for column in range(boardSize):
        if column != y:
            if type(board[x][column]) != int:
                if board[x][column] != currentPlayer:
                    rating += 2
                else:
                    rating += 1
                
    
    for row in range(boardSize):
        if row != x:
            if type(board[row][y]) != int:
                if board[row][y] != currentPlayer:
                    rating += 2
                else:
                    rating += 1

    return (x, y, rating)

def PickMove(ratings):
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
    print(len(ratings))
    return equivelantMoves[random.randint(0, len(equivelantMoves)-1)]
# endregion

# region Move logic
def ValidateMove(targetRow, targetColumn):
    global board
    
    if type(board[targetRow][targetColumn]) == type("string"):
        return False

    return True

def ExecuteMove(targetRow, targetColumn):
    global currentPlayer
    global isXTurn
    global board
    global againstAI
    global playerIsX

    board[targetRow][targetColumn] = currentPlayer

    PrintBoard()
    
    if CheckVictory():
        Victory()
        return
    
    
    
    if isXTurn:
        isXTurn = False
        currentPlayer = "O"
    else:
        isXTurn = True
        currentPlayer = "X"
    
    if againstAI and playerIsX == False and isXTurn:
        EvaluateAllSpaces()
    elif againstAI and playerIsX and isXTurn == False:
        EvaluateAllSpaces()

        
# endregion
    
# region Evaluate game ending

def Victory():
    global currentPlayer
    global isXTurn
    global board
    
    print(f"{currentPlayer} has won!")
    input("Press enter to play again...")
    InitializeBoard()


def CheckVictory():
    global currentPlayer
    global isXTurn
    global board
    
    if CheckHorizontalVictory() or CheckVerticalVictory() or CheckDiagonalVictory() or CheckStalemate():
        return True
    return False
    
def CheckVerticalVictory():  
    global currentPlayer
    global isXTurn
    global board
    global boardSize
    
    for columns in range(boardSize):
        counter = 0
        for rows in range(boardSize):
            if board[rows][columns] == currentPlayer:
                counter += 1
        if counter == boardSize:
            print("Victory by vertical!")
            return True
            Victory()
    return False
    
def CheckHorizontalVictory(): 
    global currentPlayer
    global isXTurn
    global board
    global boardSize
    
    for rows in range(boardSize):
        counter = 0
        for columns in range(boardSize):
            if board[rows][columns] == currentPlayer:
                counter += 1
        if counter == boardSize:
            print("Victory by horizontal!")
            return True
            Victory()
    return False

def CheckDiagonalVictory():
    global currentPlayer
    global isXTurn
    global board
    global boardSize
    
    counter = 0
    for x in range(boardSize):
        if board[x][x] == currentPlayer:
            counter += 1
    if counter == boardSize:
        print("Victory by diagonal!")
        return True
    
    counter = 0
    yValue = 0
    for x in range(boardSize-1, -1, -1):
        if board[x][yValue] == currentPlayer:
            counter += 1
        yValue += 1
    if counter == boardSize:
        print("Victory by diagonal!")
        return True
        
    return False
    
def CheckStalemate():
    global boardSize
    global board

    for row in range(boardSize):
        for column in range(boardSize):
            if type(board[row][column]) == int:
                return
    
    print("Stalemate")
    input("Press enter to play again...")
    InitializeBoard()
# endregion

# region Utilities
def PrintBoard():
    global board
    global boardSize

    rowString = ""
    
    if totalSquares > 9:
        for row in range(boardSize):
            print("-" * 5 + "-" * 4 * boardSize)
            rowString = "| "
            for column in range(boardSize):
                if row * boardSize + column < 9 or type(board[row][column]) == str:
                    rowString = rowString + f"{board[row][column]}  | "
                else:
                    rowString = rowString + f"{board[row][column]} | "
            print(rowString)
        print("-" * 5 + "-" * 4 * boardSize) # Printer nederste række.
    else:
        for row in range(boardSize):
            print("-" * 4 + "-" * 3 * boardSize)
            rowString = "| "
            for column in range(boardSize):
                rowString = rowString + f"{board[row][column]} | "
            print(rowString)
        print("-" * 4 + "-" * 3 * boardSize) # Printer nederste række.
    

def InitializeBoard():
    global currentPlayer
    global isXTurn
    global board
    global boardSize
    
    SoloOrMulti()
    PopulateEmptyBoard(boardSize, boardSize)
    isXTurn = False
    currentPlayer = "O"
    PrintBoard()
    if againstAI and playerIsX:
        EvaluateAllSpaces()



def PopulateEmptyBoard(sizeX, sizeY):
    boardCounter = 1
    board.clear()
    for row in range(sizeX):
        board.append([])
        for column in range(sizeY):
            board[row].append(boardCounter)
            boardCounter = boardCounter + 1


# endregion

# region input
def AwaitUserInput():
    global currentPlayer
    
    move = input(f"Waiting for {currentPlayer} player move...\n")
    if ValidateInput(move) == True:
        boardCoordinate = InputToBoardCoordinate(move)
        if ValidateMove(boardCoordinate[0], boardCoordinate[1]) == True:
            ExecuteMove(boardCoordinate[0], boardCoordinate[1])
        else:
            print("Square is already taken")
    
    return

def ValidateInput(input):
    
    if input.isnumeric() == False:
        print("Input must be a whole number")
        return False
    
    if int(input) == 0 or int(input)-1 > totalSquares:
        print(f"Input must be a number from 1 - {totalSquares}")
        return False
    
    return True

def InputToBoardCoordinate(input):
    global boardSize

    counter = 0
    for row in range(boardSize):
        for column in range(boardSize):
            counter += 1
            if counter == int(input):
                return (row, column)

def SoloOrMulti():
    global againstAI
    
    inp = input("Play against AI? y/n\n")
    evaluatedInput = EvaluateYesNo(inp)

    if type(evaluatedInput) == type("string"):
        print("Not a valid input")
        SoloOrMulti()
        return

    againstAI = evaluatedInput
    if againstAI == False:
        return
    
    PlayerChooseSymbol()
    

def PlayerChooseSymbol():
    global playerIsX

    inp = input("Play as X? y/n\n")
    evaluatedInput = EvaluateYesNo(inp)

    if type(evaluatedInput) == type("string"):
        print("Not a valid input")
        PlayerChooseSymbol()
        return
    
    playerIsX = evaluatedInput
    
    if evaluatedInput:
        print("Player is X. The AI makes the first move...")
    else:
        print("Player is O. You will make the first move...")


def EvaluateYesNo(input):
    if input.lower()[0] == "y":
        return True
    elif input.lower()[0] == "n":
        return False
    else:
        return "invalid"
# endregion

InitializeBoard()
while True:
    AwaitUserInput()