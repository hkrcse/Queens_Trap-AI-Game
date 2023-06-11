import random

import pygame, sys
import numpy as np
from queue import PriorityQueue

# initialize pygame
pygame.init()


# CONSTANTS
li = [3, 5, 7]
r = random.choice(li)

WIDTH = r * 160
HEIGHT = WIDTH
LINE_WIDTH = 5
BOARD_ROWS = r
BOARD_COLS = BOARD_ROWS
SQUARE_SIZE = WIDTH/BOARD_ROWS

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BG_COLOR = (255, 206, 158)

LINE_COLOR = (211, 138, 71)
WHITE = (239, 231, 200)
WHITE_HORSE = pygame.image.load("white_queen.png")
WHITE_HORSE = pygame.transform.scale(WHITE_HORSE, (150,150))
BLACK_HORSE = pygame.image.load("black_queen.png")
BLACK_HORSE = pygame.transform.scale(BLACK_HORSE, (150,150))
GRAY_HORSE = pygame.image.load("block_square.png")
GRAY_HORSE = pygame.transform.scale(GRAY_HORSE, (155,155))
GAME_OVER = pygame.image.load("game_over.png")
GAME_OVER = pygame.transform.scale(GAME_OVER, (160,160))
RED_HORSE = pygame.image.load("red_queen.png")
RED_HORSE = pygame.transform.scale(RED_HORSE, (150,150))
LOSE = pygame.image.load("lose.png")
LOSE = pygame.transform.scale(LOSE, (120, 120))
WIN = pygame.image.load("win.png")
WIN = pygame.transform.scale(WIN, (140, 140))


# VARIABLES
player = 1
game_over = False
losePlayer = 0


# SCREEN
screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
pygame.display.set_caption( 'Isolation Game' )
screen.fill( BG_COLOR )


# CONSOLE BOARD
board = np.zeros((BOARD_ROWS, BOARD_COLS))



# Player Current Possition
playerOneCurrentRow = -1
playerOneCurrentCol = -1
playerTwoCurrentRow = -1
playerTwoCurrentCol = -1


# FUNCTIONS
def draw_lines():

    for i in range(1,BOARD_ROWS):
        # horizontal
        pygame.draw.line( screen, LINE_COLOR, (0, SQUARE_SIZE*i), (WIDTH, SQUARE_SIZE*i), LINE_WIDTH )

    for i in range(1,BOARD_COLS):
        # vertical
        pygame.draw.line( screen, LINE_COLOR, (i * SQUARE_SIZE, 0), (i * SQUARE_SIZE, HEIGHT), LINE_WIDTH )


def draw_figures():
    flag = -1
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 1:
                if (row == playerOneCurrentRow and col == playerOneCurrentCol and losePlayer == 1 ):    #player1 lost UI
                    screen.blit(RED_HORSE, (int( col * SQUARE_SIZE ), int( row * SQUARE_SIZE )))
                    #screen.blit(GAME_OVER, ((r//2)*160,(r//2)*160))
                    #screen.blit(LOSE, ((r//2)*160,(r//2)*160))
                    flag = 0
                elif (row == playerOneCurrentRow and col == playerOneCurrentCol):
                    screen.blit(BLACK_HORSE, (int( col * SQUARE_SIZE ), int( row * SQUARE_SIZE )))
                else:
                    screen.blit(GRAY_HORSE, (int( col * SQUARE_SIZE )+3, int( row * SQUARE_SIZE )+3))
            elif board[row][col] == 2:
                if (row == playerTwoCurrentRow and col == playerTwoCurrentCol and losePlayer == 2 ):    #player2 lost UI
                    screen.blit(RED_HORSE, (int( col * SQUARE_SIZE ), int( row * SQUARE_SIZE )))
                    #screen.blit(GAME_OVER, (160,160))
                    #screen.blit(WIN, (160,160))
                    flag = 1
                elif (row == playerTwoCurrentRow and col == playerTwoCurrentCol):
                    screen.blit(WHITE_HORSE, (int( col * SQUARE_SIZE ), int( row * SQUARE_SIZE )))
                else:
                    screen.blit(GRAY_HORSE, (int( col * SQUARE_SIZE )+3, int( row * SQUARE_SIZE )+3))
    if(flag == 1):
        #screen.blit(GAME_OVER, ( (r//2)*160, (r//2)*160))
        screen.blit(WIN, (((r // 2) * 160)+8, ((r // 2) * 160)+8))
    elif(flag == 0):
        screen.blit(LOSE, (((r // 2) * 160)+15, ((r // 2) * 160)+15))


def mark_square(row, col, player):
    board[row][col] = player
    print ("----------------------------------------------------")
    print("Player " + str(player) + " marked square : (" + str(row) + "," + str(col) + ")")
    print(board)
    print ("----------------------------------------------------")


def available_square(row, col, player):
    if(player == 1):
        currentRow = playerOneCurrentRow
        currentCol = playerOneCurrentCol
    else:
        currentRow = playerTwoCurrentRow
        currentCol = playerTwoCurrentCol

    return (board[row][col] == 0 and ( 
        (currentRow == -1 and currentCol==-1) or
        (currentRow-1 == row and currentCol-1 == col)or
        (currentRow-1 == row and currentCol == col)or
        (currentRow-1 == row and currentCol+1 == col)or
        (currentRow == row and currentCol+1 == col)or
        (currentRow+1 == row and currentCol+1 == col)or
        (currentRow+1 == row and currentCol == col)or
        (currentRow+1 == row and currentCol-1 == col)or
        (currentRow == row and currentCol-1 == col)
    ))				
def available_square_list(row, col):
    blockable_square = []
    x = row
    y = col
    if x - 1 >= 0 and y - 1 >= 0 and x - 1 < BOARD_ROWS and y - 1 < BOARD_COLS and board[x - 1][y - 1] == 0:
        blockable_square.append((x - 1, y - 1))
    if x - 1 >= 0 and y >= 0 and x - 1 < BOARD_ROWS and y < BOARD_COLS and board[x - 1][y] == 0:
        blockable_square.append((x - 1, y))
    if x - 1 >= 0 and y + 1 >= 0 and x - 1 < BOARD_ROWS and y + 1 < BOARD_COLS and board[x - 1][y + 1] == 0:
        blockable_square.append((x - 1, y + 1))
    if x >= 0 and y + 1 >= 0 and x < BOARD_ROWS and y + 1 < BOARD_COLS and board[x][y + 1] == 0:
        blockable_square.append((x, y + 1))
    if x + 1 >= 0 and y + 1 >= 0 and x + 1 < BOARD_ROWS and y + 1 < BOARD_COLS and board[x + 1][y + 1] == 0:
        blockable_square.append((x + 1, y + 1))

    if x + 1 >= 0 and y >= 0 and x + 1 < BOARD_ROWS and y < BOARD_COLS and board[x + 1][y] == 0:
        blockable_square.append((x + 1, y))
    if x + 1 >= 0 and y - 1 >= 0 and x + 1 < BOARD_ROWS and y - 1 < BOARD_COLS and board[x + 1][y - 1] == 0:
        blockable_square.append((x + 1, y - 1))
    if x >= 0 and y - 1 >= 0 and x < BOARD_ROWS and y - 1 < BOARD_COLS and board[x][y - 1] == 0:
        blockable_square.append((x, y - 1))

    return blockable_square
def is_board_full():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 0:
                return False

    return True

def check_lose(player):
    if(player == 1):
        currentRow = playerOneCurrentRow
        currentCol = playerOneCurrentCol
    else:
        currentRow = playerTwoCurrentRow
        currentCol = playerTwoCurrentCol


    if(currentRow == -1 or currentCol == -1):
        return False

    return not (
        (-1 < currentRow-1 and currentRow-1 < BOARD_ROWS and -1 < currentCol-1 and currentCol-1 < BOARD_COLS and board[currentRow-1][currentCol-1] == 0 ) or
        (-1 < currentRow-1 and currentRow-1 < BOARD_ROWS and -1 < currentCol and currentCol < BOARD_COLS and board[currentRow-1][currentCol] == 0 ) or
        (-1 < currentRow-1 and currentRow-1 < BOARD_ROWS and -1 < currentCol+1 and currentCol+1 < BOARD_COLS and board[currentRow-1][currentCol+1] == 0 ) or
        (-1 < currentRow and currentRow < BOARD_ROWS and -1 < currentCol+1 and currentCol+1 < BOARD_COLS and board[currentRow][currentCol+1] == 0 ) or
        (-1 < currentRow+1 and currentRow+1 < BOARD_ROWS and -1 < currentCol+1 and currentCol+1 < BOARD_COLS and board[currentRow+1][currentCol+1] == 0 ) or
        (-1 < currentRow+1 and currentRow+1 < BOARD_ROWS and -1 < currentCol and currentCol < BOARD_COLS and board[currentRow+1][currentCol] == 0 ) or
        (-1 < currentRow+1 and currentRow+1 < BOARD_ROWS and -1 < currentCol-1 and currentCol-1 < BOARD_COLS and board[currentRow+1][currentCol-1] == 0 ) or
        (-1 < currentRow and currentRow < BOARD_ROWS and -1 < currentCol-1 and currentCol-1 < BOARD_COLS and board[currentRow][currentCol-1] == 0 )


    )

def restart():
    screen.fill(BG_COLOR)
    draw_lines()
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            board[row][col] = 0



def bestMove(player = 2):
    bestScore = -100000
    move = None

    global playerTwoCurrentCol
    global playerTwoCurrentRow




    if(player == 1):
        currentRow = playerOneCurrentRow
        currentCol = playerOneCurrentCol
    else:
        currentRow = playerTwoCurrentRow
        currentCol = playerTwoCurrentCol


    if(currentRow == -1 or currentCol == -1):
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if(board[row][col] == 0):
                    board[row][col] = 2
                    score = minimax(board,1,playerOneCurrentRow,playerOneCurrentCol,row,col,0,False)
                    board[row][col] = 0

                    if(score>bestScore):
                        bestScore = score
                        move = (row,col)

    if(-1 < currentRow-1 and currentRow-1 < BOARD_ROWS and -1 < currentCol-1 and currentCol-1 < BOARD_COLS and board[currentRow-1][currentCol-1] == 0 ):
        board[currentRow-1][currentCol-1] = 2
        score = minimax(board,1,playerOneCurrentRow,playerOneCurrentCol,currentRow-1 , currentCol-1,0,False)
        board[currentRow-1][currentCol-1] = 0

        if(score>bestScore):
            bestScore = score
            move = (currentRow-1 , currentCol-1)

    if(-1 < currentRow-1 and currentRow-1 < BOARD_ROWS and -1 < currentCol and currentCol < BOARD_COLS and board[currentRow-1][currentCol] == 0 ):
        board[currentRow-1][currentCol] = 2
        score = minimax(board,1,playerOneCurrentRow,playerOneCurrentCol,currentRow-1,currentCol,0,False)
        board[currentRow-1][currentCol] = 0

        if(score>bestScore):
            bestScore = score
            move = (currentRow-1,currentCol)

    if(-1 < currentRow-1 and currentRow-1 < BOARD_ROWS and -1 < currentCol+1 and currentCol+1 < BOARD_COLS and board[currentRow-1][currentCol+1] == 0 ):
        board[currentRow-1][currentCol+1] = 2
        score = minimax(board,1,playerOneCurrentRow,playerOneCurrentCol,currentRow-1,currentCol+1,0,False)
        board[currentRow-1][currentCol+1] = 0

        if(score>bestScore):
            bestScore = score
            move = (currentRow-1,currentCol+1)

    if(-1 < currentRow and currentRow < BOARD_ROWS and -1 < currentCol+1 and currentCol+1 < BOARD_COLS and board[currentRow][currentCol+1] == 0 ):
        board[currentRow][currentCol+1] = 2
        score = minimax(board,1,playerOneCurrentRow,playerOneCurrentCol,currentRow,currentCol+1,0,False)
        board[currentRow][currentCol+1] = 0

        if(score>bestScore):
            bestScore = score
            move = (currentRow,currentCol+1)

    if(-1 < currentRow+1 and currentRow+1 < BOARD_ROWS and -1 < currentCol+1 and currentCol+1 < BOARD_COLS and board[currentRow+1][currentCol+1] == 0 ):
        board[currentRow+1][currentCol+1] = 2
        score = minimax(board,1,playerOneCurrentRow,playerOneCurrentCol,currentRow+1,currentCol+1,0,False)
        board[currentRow+1][currentCol+1] = 0

        if(score>bestScore):
            bestScore = score
            move = (currentRow+1,currentCol+1)

    if(-1 < currentRow+1 and currentRow+1 < BOARD_ROWS and -1 < currentCol and currentCol < BOARD_COLS and board[currentRow+1][currentCol] == 0 ):
        board[currentRow+1][currentCol] = 2
        score = minimax(board,1,playerOneCurrentRow,playerOneCurrentCol,currentRow+1,currentCol,0,False)
        board[currentRow+1][currentCol] = 0

        if(score>bestScore):
            bestScore = score
            move = (currentRow+1,currentCol)

    if(-1 < currentRow+1 and currentRow+1 < BOARD_ROWS and -1 < currentCol-1 and currentCol-1 < BOARD_COLS and board[currentRow+1][currentCol-1] == 0 ):
        board[currentRow+1][currentCol-1] = 2
        score = minimax(board,1,playerOneCurrentRow,playerOneCurrentCol,currentRow+1,currentCol-1,0,False)
        board[currentRow+1][currentCol-1] = 0

        if(score>bestScore):
            bestScore = score
            move = (currentRow+1,currentCol-1)

    if(-1 < currentRow and currentRow < BOARD_ROWS and -1 < currentCol-1 and currentCol-1 < BOARD_COLS and board[currentRow][currentCol-1] == 0 ):
        board[currentRow][currentCol-1] = 2
        score = minimax(board,1,playerOneCurrentRow,playerOneCurrentCol,currentRow,currentCol-1,0,False)
        board[currentRow][currentCol-1] = 0

        if(score>bestScore):
            bestScore = score
            move = (currentRow,currentCol-1)
    

    playerTwoCurrentRow = move[0]
    playerTwoCurrentCol = move[1]
    mark_square( move[0], move[1], 2)
    


    
scores = {
  1: 10,
  2: -10,
  0: 0
}

def minimax(board, player, playerOneCurrentRow, playerOneCurrentCol, playerTwoCurrentRow, playerTwoCurrentCol , depth, isMaximizing):
    result = player if check_lose(player) else 0
    if result is not None:
        return scores[result]


    if(player == 1):
        currentRow = playerOneCurrentRow
        currentCol = playerOneCurrentCol
    else:
        currentRow = playerTwoCurrentRow
        currentCol = playerTwoCurrentCol
    
    if isMaximizing:
        bestScore = -100000


        if(-1 < currentRow-1 and currentRow-1 < BOARD_ROWS and -1 < currentCol-1 and currentCol-1 < BOARD_COLS and board[currentRow-1][currentCol-1] == 0 ):
            board[currentRow-1][currentCol-1] = 2
            score = minimax(board,1,playerOneCurrentRow,playerOneCurrentCol,currentRow-1 , currentCol-1,0,False)
            board[currentRow-1][currentCol-1] = 0

            bestScore = max(score,bestScore)

        if(-1 < currentRow-1 and currentRow-1 < BOARD_ROWS and -1 < currentCol and currentCol < BOARD_COLS and board[currentRow-1][currentCol] == 0 ):
            board[currentRow-1][currentCol] = 2
            score = minimax(board,1,playerOneCurrentRow,playerOneCurrentCol,currentRow-1,currentCol,0,False)
            board[currentRow-1][currentCol] = 0

            bestScore = max(score,bestScore)

        if(-1 < currentRow-1 and currentRow-1 < BOARD_ROWS and -1 < currentCol+1 and currentCol+1 < BOARD_COLS and board[currentRow-1][currentCol+1] == 0 ):
            board[currentRow-1][currentCol+1] = 2
            score = minimax(board,1,playerOneCurrentRow,playerOneCurrentCol,currentRow-1,currentCol+1,0,False)
            board[currentRow-1][currentCol+1] = 0

            bestScore = max(score,bestScore)

        if(-1 < currentRow and currentRow < BOARD_ROWS and -1 < currentCol+1 and currentCol+1 < BOARD_COLS and board[currentRow][currentCol+1] == 0 ):
            board[currentRow][currentCol+1] = 2
            score = minimax(board,1,playerOneCurrentRow,playerOneCurrentCol,currentRow,currentCol+1,0,False)
            board[currentRow][currentCol+1] = 0

            bestScore = max(score,bestScore)

        if(-1 < currentRow+1 and currentRow+1 < BOARD_ROWS and -1 < currentCol+1 and currentCol+1 < BOARD_COLS and board[currentRow+1][currentCol+1] == 0 ):
            board[currentRow+1][currentCol+1] = 2
            score = minimax(board,1,playerOneCurrentRow,playerOneCurrentCol,currentRow+1,currentCol+1,0,False)
            board[currentRow+1][currentCol+1] = 0

            bestScore = max(score,bestScore)

        if(-1 < currentRow+1 and currentRow+1 < BOARD_ROWS and -1 < currentCol and currentCol < BOARD_COLS and board[currentRow+1][currentCol] == 0 ):
            board[currentRow+1][currentCol] = 2
            score = minimax(board,1,playerOneCurrentRow,playerOneCurrentCol,currentRow+1,currentCol,0,False)
            board[currentRow+1][currentCol] = 0

            bestScore = max(score,bestScore)

        if(-1 < currentRow+1 and currentRow+1 < BOARD_ROWS and -1 < currentCol-1 and currentCol-1 < BOARD_COLS and board[currentRow+1][currentCol-1] == 0 ):
            board[currentRow+1][currentCol-1] = 2
            score = minimax(board,1,playerOneCurrentRow,playerOneCurrentCol,currentRow+1,currentCol-1,0,False)
            board[currentRow+1][currentCol-1] = 0

            bestScore = max(score,bestScore)

        if(-1 < currentRow and currentRow < BOARD_ROWS and -1 < currentCol-1 and currentCol-1 < BOARD_COLS and board[currentRow][currentCol-1] == 0 ):
            board[currentRow][currentCol-1] = 2
            score = minimax(board,1,playerOneCurrentRow,playerOneCurrentCol,currentRow,currentCol-1,0,False)
            board[currentRow][currentCol-1] = 0

            bestScore = max(score,bestScore)
        
        print("BEST SCORE MAX = ",bestScore)
        return bestScore

    else:
        bestScore = 100000

        if(-1 < currentRow-1 and currentRow-1 < BOARD_ROWS and -1 < currentCol-1 and currentCol-1 < BOARD_COLS and board[currentRow-1][currentCol-1] == 0 ):
            board[currentRow-1][currentCol-1] = 1
            score = minimax(board,2,playerOneCurrentRow,playerOneCurrentCol,currentRow-1 , currentCol-1,0,True)
            board[currentRow-1][currentCol-1] = 0

            bestScore = min(score,bestScore)

        if(-1 < currentRow-1 and currentRow-1 < BOARD_ROWS and -1 < currentCol and currentCol < BOARD_COLS and board[currentRow-1][currentCol] == 0 ):
            board[currentRow-1][currentCol] = 1
            score = minimax(board,2,playerOneCurrentRow,playerOneCurrentCol,currentRow-1,currentCol,0,True)
            board[currentRow-1][currentCol] = 0

            bestScore = min(score,bestScore)

        if(-1 < currentRow-1 and currentRow-1 < BOARD_ROWS and -1 < currentCol+1 and currentCol+1 < BOARD_COLS and board[currentRow-1][currentCol+1] == 0 ):
            board[currentRow-1][currentCol+1] = 1
            score = minimax(board,2,playerOneCurrentRow,playerOneCurrentCol,currentRow-1,currentCol+1,0,True)
            board[currentRow-1][currentCol+1] = 0

            bestScore = min(score,bestScore)

        if(-1 < currentRow and currentRow < BOARD_ROWS and -1 < currentCol+1 and currentCol+1 < BOARD_COLS and board[currentRow][currentCol+1] == 0 ):
            board[currentRow][currentCol+1] = 1
            score = minimax(board,2,playerOneCurrentRow,playerOneCurrentCol,currentRow,currentCol+1,0,True)
            board[currentRow][currentCol+1] = 0

            bestScore = min(score,bestScore)

        if(-1 < currentRow+1 and currentRow+1 < BOARD_ROWS and -1 < currentCol+1 and currentCol+1 < BOARD_COLS and board[currentRow+1][currentCol+1] == 0 ):
            board[currentRow+1][currentCol+1] = 1
            score = minimax(board,2,playerOneCurrentRow,playerOneCurrentCol,currentRow+1,currentCol+1,0,True)
            board[currentRow+1][currentCol+1] = 0

            bestScore = min(score,bestScore)

        if(-1 < currentRow+1 and currentRow+1 < BOARD_ROWS and -1 < currentCol and currentCol < BOARD_COLS and board[currentRow+1][currentCol] == 0 ):
            board[currentRow+1][currentCol] = 1
            score = minimax(board,2,playerOneCurrentRow,playerOneCurrentCol,currentRow+1,currentCol,0,True)
            board[currentRow+1][currentCol] = 0

            bestScore = min(score,bestScore)

        if(-1 < currentRow+1 and currentRow+1 < BOARD_ROWS and -1 < currentCol-1 and currentCol-1 < BOARD_COLS and board[currentRow+1][currentCol-1] == 0 ):
            board[currentRow+1][currentCol-1] = 1
            score = minimax(board,2,playerOneCurrentRow,playerOneCurrentCol,currentRow+1,currentCol-1,0,True)
            board[currentRow+1][currentCol-1] = 0

            bestScore = min(score,bestScore)

        if(-1 < currentRow and currentRow < BOARD_ROWS and -1 < currentCol-1 and currentCol-1 < BOARD_COLS and board[currentRow][currentCol-1] == 0 ):
            board[currentRow][currentCol-1] = 1
            score = minimax(board,2,playerOneCurrentRow,playerOneCurrentCol,currentRow,currentCol-1,0,True)
            board[currentRow][currentCol-1] = 0

            bestScore = min(score,bestScore)

        print("BEST SCORE MIN= ",bestScore)
        return bestScore




draw_lines()

font = pygame.font.Font(None, 36)
block = -1
# MAINLOOP---------
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and  not game_over and (block == -1 or block == 1):

            print("hi")

            mouseX = event.pos[0] # x
            mouseY = event.pos[1] # y

            clicked_row = int(mouseY // SQUARE_SIZE)
            clicked_col = int(mouseX // SQUARE_SIZE)
            #print('Mouse X position: ' + str(mouseX))
            #print('Mouse Y position: ' + str(mouseY))
            print('Clicked row: ' + str(clicked_row))
            print('Clicked col: ' + str(clicked_col))


            if available_square( clicked_row, clicked_col, 1 ):
                player = 1
                mark_square( clicked_row, clicked_col, player )

                playerOneCurrentRow = clicked_row
                playerOneCurrentCol = clicked_col
                print('Player One Current Row and Col: (',str(playerOneCurrentRow)+','+str(playerOneCurrentCol)+')')


                if check_lose( 2 ):
                    losePlayer = 2
                    game_over = True
                    draw_figures()


                else:

                    player = 2
                    bestMove(player)

                    if check_lose( 1 ):
                        losePlayer = 1
                        game_over = True
                        print("********************************************************")
                        print("Player 1 lost.\nRestarting game : Press -> R")
                        print("Quit game : Press -> Q")
                        print("********************************************************")
                    
                    draw_figures()
            if block == -1:
                block = 1
            else:
                block = 2
            print(playerOneCurrentRow,playerOneCurrentCol," ",playerTwoCurrentRow, playerTwoCurrentCol)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3 and not game_over and block == 2:
            print("hi 2")

            mouseX = event.pos[0]  # x
            mouseY = event.pos[1]  # y

            clicked_row = int(mouseY // SQUARE_SIZE)
            clicked_col = int(mouseX // SQUARE_SIZE)
            # print('Mouse X position: ' + str(mouseX))
            # print('Mouse Y position: ' + str(mouseY))
            print('Clicked row: ' + str(clicked_row))
            print('Clicked col: ' + str(clicked_col))

            if board[clicked_row][clicked_col] == 0:
                mark_square(clicked_row, clicked_col, 1)

            if check_lose(2):
                losePlayer = 2
                game_over = True
                draw_figures()
            else:
                blockable_square_list = available_square_list(playerOneCurrentRow, playerOneCurrentCol)
                # x = playerOneCurrentRow
                # y = playerOneCurrentCol

                # if x - 1 >= 0 and y - 1 >= 0 and x - 1 < BOARD_ROWS and y - 1 < BOARD_COLS and board[x - 1][y - 1] == 0 :
                #     blockable_square_2.append((x-1, y-1))
                # if x - 1 >= 0 and y >= 0 and x - 1 < BOARD_ROWS and y < BOARD_COLS and board[x - 1][y] == 0:
                #     blockable_square_2.append((x-1, y))
                # if x - 1 >= 0 and y + 1 >= 0 and x - 1 < BOARD_ROWS and y + 1 < BOARD_COLS and board[x - 1][y + 1] == 0:
                #     blockable_square_2.append((x-1, y + 1))
                # if x >= 0 and y + 1 >= 0 and x  < BOARD_ROWS and y + 1 < BOARD_COLS and board[x][y + 1] == 0:
                #     blockable_square_2.append((x, y + 1))
                # if x+1 >= 0 and y + 1 >= 0 and x + 1 < BOARD_ROWS and y + 1 < BOARD_COLS and board[x + 1][y + 1] == 0:
                #     blockable_square_2.append((x + 1, y + 1))
                #
                # if x+1 >= 0 and y >= 0 and x + 1 < BOARD_ROWS and y< BOARD_COLS and board[x + 1][y] == 0:
                #     blockable_square_2.append((x + 1, y))
                # if x+1 >= 0 and y - 1 >= 0 and x + 1 < BOARD_ROWS and y - 1 < BOARD_COLS and board[x + 1][y - 1] == 0:
                #     blockable_square_2.append((x + 1, y - 1))
                # if x  >= 0 and y - 1 >= 0 and x < BOARD_ROWS and y - 1 < BOARD_COLS and board[x ][y - 1] == 0:
                #     blockable_square_2.append((x, y - 1))

                print(blockable_square_list,"\n")

                pq = PriorityQueue()
                for (u, v) in blockable_square_list:
                    print(u,v)
                    li = available_square_list(u, v)
                    print(li)
                    pq.put((len(li) * -1, (u, v)))

                xy = pq.get()

                (x, y) = xy[1]
                while not pq.empty():
                    current = pq.get()
                    print(current)

                print(x, y)

                mark_square(x, y, 2)

                if check_lose(1):
                    losePlayer = 1
                    game_over = True
                    draw_figures()
            block = 1

            draw_figures()


        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart()
                player = 1
                game_over = False
                losePlayer = 0
                playerOneCurrentRow = -1
                playerOneCurrentCol = -1
                playerTwoCurrentRow = -1
                playerTwoCurrentCol = -1
                block = -1
            
            elif event.key == pygame.K_q:
                pygame.display.quit()

    pygame.display.update()