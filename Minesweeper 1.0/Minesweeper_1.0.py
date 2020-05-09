#Jessica Qinying Wu
#This is Minesweeper 1.0 - a recreation of the classic Minewsweeper game programmed using python
#Project start date: May 5th, 2020
import numpy as np
import random
import time
#constants used in this project
BLANK=0
STR_BLANK='    '
BOMB=-1
STR_BOMB='  @ '
MASKED=-2
STR_MASKED='  # '
FLAG=-3
STR_FLAG='  ~ '
WRONG=-4
STR_WRONG='  X '

#function to print the intro for user input prompt
def Intro():
    print('\n\n\nWelcome to Minesweeper 1.0\n\n')
    print('Please select a difficulty level by entering the corresponding command as stated inside the parenthesis')
    print(' (B) - Beginner (10 mines)\n (I) - Intermediate (40 mines)\n (A) - Advanced (99 mines)\n (C) - Custom')
    print('\n (Q) - Quit the game')
#functions to print the instructions for the input commands to play the game
def PrintInstructions():
    print('COMMAND INPUT INSTRUCTIONS:')
    print(' (U) - Uncover a cell')
    print(' (F) - Flag a mine as a bomb')
    print(' (L) - Unflag a mine')
    print(' (S) - See the Solution (will automatically terminate the current game)')
    print(' (R) - Restart the game')
    print(' (N) - Start a new game')
    print(' (Q) - Quit the game')
    print('Prompts will appear after a valid command input')

#functioN to print out the legends to explain the meaning of the board symbols
def PrintLegends():
    print('Legends:')
    print(STR_MASKED,' - Covered cell')
    print(STR_BLANK, ' - Uncovered cell')
    print(STR_BOMB, ' - Bomb')
    print(STR_FLAG, ' - Flag')
    print(STR_WRONG,' - Wrongly placed flag')
    print('Any numbers on the grid represent the mines count in the adjacent cells')

#function to print the game board
#parameter gameBoard is the minesweeper's current game board
def PrintBoard(gameBoard):
    print('    ',end='')
    for i in range(gameBoard.shape[1]):
        print('[ %d]'%(i+1) if i<9 else '[%d]'%(i+1),end='')
    print('\n')
    for row in range(gameBoard.shape[0]):#matrix row iteration
        print('[ %d]'%(row+1) if row<9 else '[%d]'%(row+1),end='')
        for col in range(gameBoard.shape[1]):
            if gameBoard[row,col]==MASKED: #case 1: Masked
                print(STR_MASKED,end='')
            elif gameBoard[row,col]==FLAG: #case 2: Flag
                print(STR_FLAG,end='')
            elif gameBoard[row,col]==BLANK: #case 3: Blank
                print(STR_BLANK,end='')
            elif gameBoard[row,col]==BOMB: #case 4: Bomb
                print(STR_BOMB,end='')
            elif gameBoard[row,col]==WRONG: #case 4: flagged on incorrect mine
                print(STR_WRONG,end='')
            else: #display the number of mines in the adjacent cells
                print('  %d '%gameBoard[row,col],end='')
        print('\n')
    PrintLegends()

#function to print the solution of the game
def PrintSolution(solution):
    print('\nThis is the solution of the game: ')
    PrintBoard(solution)

#function to generate the minesweeper game board based on the difficulty level chosen
#parameter difficulty is the level of difficulty requested by the player
#parameter rowSize is the count of rows of the game grid
#parameter colSize is the count of columns of the game grid
#parameter minesCount is the count of bombs to be put in the game
#returns the generated board without masking (a board consisted of only blanks and bombs)
def MakeGame(difficulty,rowSize,colSize,bombsCount):
    solution=np.zeros((rowSize,colSize),np.int8) #0 indicates blank
    while bombsCount>0: #-1 indicates a bomb
        rowIndex=random.randint(0,rowSize-1)
        colIndex=random.randint(0,colSize-1)
        if solution[rowIndex,colIndex]==BLANK:
            solution[rowIndex,colIndex]=BOMB
            bombsCount-=1
    return solution

#function that determines the location of a cell based on the type of information requested
#parameter type is the position whereabout of the cell (either row or column)
#parameter gameBoard is the current minesweeper game board
#returns the index of the the requested type (i.e. row index or column index) beginning at 0
def SelectCell(type,gameBoard):
    index=0
    while index==0:
        print('Please indicate the %s index of the cell to uncover (indicated inside the square brackets)' %type)
        index=int(input())
        if index <1 or (type=='row' and index>gameBoard.shape[0]) or (type=='column' and index>gameBoard.shape[1]):
            print('Please select a valid index within the board\'s size')
            index=0
    return index-1

#function to uncover cells based on the position of the cell selected
#parameter rowIndex is the row index of the cell beginning at 0
#parameter colIndex is the column index of the cell beginning at 0
#parameter gameBoard is the current minesweeper game board
#parameter solution is the initially generated minesweeper with bombs without any masking
#returns the game board after uncovering
def UncoverMine(rowIndex,colIndex,gameBoard,solution):
    #case 1: bomb cell
    if solution[rowIndex,colIndex]==BOMB:
        gameBoard[rowIndex,colIndex]=BOMB
    else:#not a bomb cell
        #search the adjacent 8 cells for existence of a bomb
        topRow=rowIndex-1 if rowIndex>0 else 0
        bottomRow=rowIndex+2 if rowIndex<gameBoard.shape[0]-1 else gameBoard.shape[0]
        leftCol=colIndex-1 if colIndex>0 else 0
        rightCol=colIndex+2 if colIndex<gameBoard.shape[1]-1 else gameBoard.shape[1]
        adj=solution[topRow:bottomRow,leftCol:rightCol].copy()
        if BOMB in adj: #if there is a bomb in one of the adjacent cells, print the number of bombs on the board
            gameBoard[rowIndex,colIndex]=np.count_nonzero(adj==BOMB)
        else:#if no bombs, recursively search the adjacent cells to reveal blanks
            gameBoard[rowIndex,colIndex]=BLANK
            for row in range(topRow,bottomRow):
                for col in range(leftCol,rightCol): #only uncover cells that are masked
                    if solution[row,col]==BLANK and gameBoard[row,col]==MASKED:
                        gameBoard=UncoverMine(row,col,gameBoard,solution)
    return gameBoard

#function to unflag a mine
#parameter rowIndex is the row index of the mine beginning at 0
#parameter colIndex is the column index of the mine beginning at 0
#parameter gameBoard is the current minesweeper game board
#returns the game board after unflagging if applicable
def UnflagMine(rowIndex,colIndex,gameBoard):
    if gameBoard[rowIndex,colIndex]==FLAG:
        gameBoard[rowIndex,colIndex]=MASKED
        print('Successfully unflagged mine at row %s, column %s' %(str(rowIndex),str(colIndex)))
    else:
        print('Cannot unflag a mine that is not already flagged, please only unflag flagged mines')
    return gameBoard

#function to flag a mine
#parameter rowIndex is the row index of the mine beginning at 0
#parameter colIndex is the column index of the mine beginning at 0
#parameter gameBoard is the current minesweeper game board
#returns the game board after flagging if applicable
def FlagMine(rowIndex,colIndex,gameBoard):
    if gameBoard[rowIndex,colIndex]==MASKED:
        gameBoard[rowIndex,colIndex]=FLAG
    else:
        print('Only uncovered cells can be flagged, please try again')
    return gameBoard

#function to calculate the time used to finish the game
#parameter sec is the total time used in seconds
#returns the time used as a string in the format [h]hours:[m]minutes:[s]seconds
def TimeUsed(secs):
    minutes=int(secs/60)
    hours=int(minutes/60)
    seconds=secs%60
    result='%d seconds' %seconds
    if hours>0:
        results='%d hours % minutes '%(hours, minutes)+result
    else:
        if minutes>0:
            result='%d minutes '%minutes+result
    return result

#program entry point
while True:
    Intro()
    gameOn=False
    solution=0
    bombsCount=0
    while not gameOn:
        response=input()
        gameOn=True
        if response=='B':
            bombsCount=10
            solution=MakeGame(response,8,8,bombsCount)
        elif response=='I':
            bombsCount=40
            solution=MakeGame(response,16,16,bombsCount)
        elif response=='A':
            bombsCount=99
            solution=MakeGame(response,16,30,bombsCount)
        elif response=='C':
            print('Please indicate the number of mines in the game (a number between 1 and 200 inclusive, the floor integer will be taken if a float number is entered)')
            bombsCount=int(input())
            while bombsCount<1 or bombsCount>200:
                print('Please enter a number within the range of 1 and 200 inclusive')
                bombsCount=input()
            solution=MakeGame(response,24,30,bombsCount)
        elif response=='Q':
            gameOn=False
            print('You have selected to quit the game, hope to see you again!')
            break
        else:
            gameOn=False
            print('Please enter a valid option')
    if gameOn==False: #quit 
        break
    gameBoard=np.full_like(solution.copy(),MASKED)
    startTime=time.time()
    while gameOn:
        PrintBoard(gameBoard)
        print('Mines left: %d\n' %bombsCount)
        PrintInstructions()
        command=input()
        if command=='S':
            PrintSolution(solution)
            print('Time used: %s' %TimeUsed(time.time()-startTime))
            break
        elif command=='Q': #quit game
            gameOn=False
            print('You have selected to quit the game, hope to see you again!')
            break
        elif command=='R': #restart game
            print('Restarting the game ...')
            gameBoard=np.full_like(solution.copy(),MASKED)
        elif command=='N': #start a new game
            break
        elif command=='U' or command=='F' or command=='L':
            rowIndex=SelectCell('row',gameBoard)
            colIndex=SelectCell('column',gameBoard)
            if command=='U':
                if gameBoard[rowIndex,colIndex]==FLAG:
                    print('Cannot uncover a flagged mine, please unflag it first if you wish to uncover')
                elif gameBoard[rowIndex,colIndex]==MASKED:
                    gameBoard=UncoverMine(rowIndex,colIndex,gameBoard.copy(),solution)
                else:
                    print('The cell you have selected ar row %s, column %s has already been uncovered, please select an undiscovered cell' %(str(rowIndex),str(colIndex)))
            elif command=='F':
                tempBoard=FlagMine(rowIndex,colIndex,gameBoard.copy())
                if not np.array_equal(tempBoard,gameBoard):
                    gameBoard=tempBoard
                    bombsCount=bombsCount-1
            else:
                tempBoard=UnflagMine(rowIndex,colIndex,gameBoard.copy())
                if not np.array_equal(tempBoard,gameBoard):
                    gameBoard=tempBoard
                    bombsCount=bombsCount+1
        else:
            print('Please input a valid command')
            
        if BOMB in gameBoard: #game lost if a bomb is revealed
            print('You\'ve hit a bomb! Game over\n')
            #indicate wrong flags
            flags=np.where(gameBoard==FLAG)
            for row,col in zip(flags[0],flags[1]):
                gameBoard[row,col]=WRONG if solution[row,col]==BLANK else BOMB
            #indicate remaining bombs
            remains=np.where(solution==BOMB)
            for row,col in zip(remains[0],remains[1]):
                gameBoard[row,col]=BOMB if solution[row,col]==BOMB else gameBoard[row,col]
            PrintSolution(gameBoard)
            print('Time used: %s' %TimeUsed(time.time()-startTime))
            break
        elif np.all(gameBoard[solution==BLANK]!=MASKED) and np.all(gameBoard[solution==BLANK]!=FLAG):
            #game win if all non-bomb cells are uncovered
            print('Congratulations on winning the game!\n')
            print('Time used: %s' %TimeUsed(time.time()-startTime))
            break
        print('Time used since last input: %s' %TimeUsed(time.time()-startTime))
    if gameOn==False: #quit 
        break