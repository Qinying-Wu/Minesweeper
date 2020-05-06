#Jessica Qinying Wu
#This is Minesweeper 1.0 - a recreation of the classic Minewsweeper game programmed using python
#Project start date: May 5th, 2020
import numpy as np
import random
import warnings
#constants used in this project
BLANK=0
BOMB=-1
MASKING=-2
FLAG=-3


#function to print the intro for user input prompt
def Intro():
    print('\n\n\nWelcome to Minesweeper 1.0\n\n')
    print('Please select a difficulty level by entering the corresponding command as stated inside the parenthesis')
    print(' (B) - Beginner (10 mines)\n (I) - Intermediate (40 mines)\n (A) - Advanced (99 mines)\n (C) - Custom')
    print('\n (Q) - Quit the game')
#functions to print the instructions for the input commands to play the game
def PrintInstructions():
    print('COMMAND INPUT INSTRUCTIONS:')
    print('\n (U) - Uncover a mine\n (F) - Flag a mine as a bomb\n (R) - Restart the game\n (Q) - Quit the game\n' )
    print('Prompts will appear after a valid command input')

#function that determines the location of a cell based on the type of information requested
#parameter type is the position whereabout of the cell (either row or column)
#parameter gameBoard is the current minesweeper game board
#returns the index of the the requested type (i.e. row index or column index) beginning at 0
def SelectCell(type,gameBoard):
    index=0
    print('Please indicate the %s index of the mine to uncover (indicated inside the square brackets)' %type)
    while index==0:
        index=input()
        if index <1 or (type=='row' and index>len(gameBoard.shape[0])) or (type=='column' and index>len(gameBoard.shape[1])):
            warnings.warn('Please select a valid index',Warning)
    return index-1

#function that handles the user command inputs
#parameter command is the command shortcut that the player has entered
#paarameter gameBoard is the current minesweeper game board
def CommandUserPrompts(command,gameBoard):
    if command=='U': #uncover a mine
        rowIndex=SelectCell('row')
        colIndex=SelectCell('column')
        #detect if there are any bombs surrounding the selected cell

        gameBoard[rowIndex,colIndex]

#function to uncover mines based on the position of the mine selected
#parameter rowIndex is the row index of the mine beginning at 0
#parameter colIndex is the column index of the mine beginning at 0
#returns true if a bomb is not yet being uncovered, else false
def UncoverMine(rowIndex,colIndex,gameBoard):
    #case 1: the selected mine position is a bomb ->end the game
    if gameBoard[rowIndex,colIndex]==BOMB:
        print('Game over')


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


def DisplayBoard(gameBoard):
    print('\n\n')
    for row in range(gameBoard.shape[0]):#matrix row iteration
        for col in range(gameBoard.shape[1]):
            print('-' if gameBoard[row,col]==MASKING else str(gameBoard[row,col]),end=' ' if col<gameBoard.shape[1]-1 else '\n')
#program entry point
while True:
    Intro()
    response=input()
    gameOn=False
    solution=0
    while not gameOn:
        gameOn=True
        if response=='B':
            solution=MakeGame(response,8,8,10)
        elif response=='I':
            solution=MakeGame(response,16,16,40)
        elif response=='A':
            solution=MakeGame(response,16,30,99)
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
    gameBoard=np.full_like(solution.copy(),MASKING)
    DisplayBoard(gameBoard)
    PrintInstructions()
    command=input()
    #while gameOn:
    #    if command=='E': #expose a mine


