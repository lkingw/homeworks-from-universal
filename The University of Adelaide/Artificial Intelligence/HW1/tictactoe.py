from random import choice
import sys

XPLAYER = +1
OPLAYER = -1
EMPTY = 0
ENABLE_AB = False
MAX_STEP = 1000000
BEGINING_STEP = 0
LNodes = []
preList = []

board = [[EMPTY, EMPTY, EMPTY],
         [EMPTY, EMPTY, EMPTY],
         [EMPTY, EMPTY, EMPTY]]

GAME_WIN = 1
NOT_COMPLETE = 0
MID_RANGE_WIN = 2
INF = 99
EARLY_TERMINATION = False

def printBoard(brd):
    chars = {XPLAYER: 'x', OPLAYER: 'o', EMPTY: '-'}
    oneline = ''
    for x in brd:
        for y in x:
            ch = chars[y]
            oneline += ch
    print(oneline)

def board2Line(brd):
    oneline = ''
    for x, row in enumerate(brd):
        for y, col in enumerate(row):
            if brd[x][y] == XPLAYER:
                oneline += 'x'
            elif brd[x][y] == OPLAYER:
                oneline += 'o'
            else: oneline += '-'
    return oneline

def printState(brd, cell, player, score, depth):
    global States

    if cell[0] > -1 and cell[1] > -1:
        brd[cell[0]][cell[1]] = player
            
    oneline = board2Line(brd)
    output({'brd': oneline, 'player': player, 'score': score})

def clearBoard(brd):
    for x, row in enumerate(brd):
        for y, col in enumerate(row):
            brd[x][y] = EMPTY


def winningPlayer(brd, player):

    winningStates = [[brd[0][0], brd[0][1], brd[0][2]],
                     [brd[1][0], brd[1][1], brd[1][2]],
                     [brd[2][0], brd[2][1], brd[2][2]],
                     [brd[0][0], brd[1][0], brd[2][0]],
                     [brd[0][1], brd[1][1], brd[2][1]],
                     [brd[0][2], brd[1][2], brd[2][2]],
                     [brd[0][0], brd[1][1], brd[2][2]],
                     [brd[0][2], brd[1][1], brd[2][0]]]

    if [player, player, player] in winningStates:
        return True

    return False


def findNumOfWinConds(brd, player):

    winningStates = [[brd[0][0], brd[0][1], brd[0][2]],
                     [brd[1][0], brd[1][1], brd[1][2]],
                     [brd[2][0], brd[2][1], brd[2][2]],
                     [brd[0][0], brd[1][0], brd[2][0]],
                     [brd[0][1], brd[1][1], brd[2][1]],
                     [brd[0][2], brd[1][2], brd[2][2]],
                     [brd[0][0], brd[1][1], brd[2][2]],
                     [brd[0][2], brd[1][1], brd[2][0]]]

    winNum = 0
    for state in winningStates:
        canWin = True
        for cell in state:
            if cell == -player:
                canWin = False
        
        if canWin:
            winNum += 1

    return winNum


def midRangeHeuristic(brd):
    XWinNum = findNumOfWinConds(brd, XPLAYER)
    OWinNum = findNumOfWinConds(brd, OPLAYER)
    return XWinNum - OWinNum


def gameWon(brd, step):

    isWin = NOT_COMPLETE
    winPlayer = ''
    score = 0

    if step >= MAX_STEP:
        isWin = MID_RANGE_WIN
        score = midRangeHeuristic(brd)
        if score >= 0:
            winPlayer = XPLAYER
        else:
            winPlayer = OPLAYER
    else:
        if winningPlayer(brd, XPLAYER):
            isWin = GAME_WIN
            winPlayer = XPLAYER
            score = midRangeHeuristic(brd)
        elif winningPlayer(brd, OPLAYER):
            isWin = GAME_WIN
            winPlayer = OPLAYER
            score = midRangeHeuristic(brd)

    return isWin, winPlayer, score
        

def emptyCells(brd):
    emptyC = []
    for x, row in enumerate(brd):
        for y, col in enumerate(row):
            if brd[x][y] == EMPTY:
                emptyC.append([x, y])

    return emptyC


def boardFull(brd):
    if len(emptyCells(brd)) == 0:
        return True
    return False


def setMove(brd, x, y, player):
    brd[x][y] = player


def getScore(brd):
    if winningPlayer(brd, XPLAYER):
        return 1
    elif winningPlayer(brd, OPLAYER):
        return -1
    else:
        return 0


def MiniMaxAB(brd, depth, alpha, beta, player):
    row = -1
    col = -1
    curStep = 9 - BEGINING_STEP - depth
    winState, winner, midScore = gameWon(brd, curStep)
    
    if EARLY_TERMINATION:
        if depth == 0 or winState == GAME_WIN:
            LNodes.append({'brd': board2Line(brd), 'score': midScore})
            return [row, col, midScore]
        elif winState == MID_RANGE_WIN:
            LNodes.append({'brd': board2Line(brd), 'score': midScore})
            return [row, col, midScore]
    else:
        if depth == 0 or winState == GAME_WIN:
            LNodes.append({'brd': board2Line(brd), 'score': getScore(brd)})
            return [row, col, getScore(brd)]

    if depth != 0 and winState == NOT_COMPLETE:
        for cell in emptyCells(brd):
            
            setMove(brd, cell[0], cell[1], player)
            score = MiniMaxAB(brd, depth - 1, alpha, beta, -player)
            printState(brd, cell, player, score[2], depth)
        
            if player == XPLAYER:
                # X is always the max player
                if score[2] > alpha:
                    alpha = score[2]
                    row = cell[0]
                    col = cell[1]
                
            else:
                if score[2] < beta:
                    beta = score[2]
                    row = cell[0]
                    col = cell[1]

            setMove(brd, cell[0], cell[1], EMPTY)

            if ENABLE_AB is True:
                if alpha >= beta:
                    break

        if player == XPLAYER:
            return [row, col, alpha]
        else:
            return [row, col, beta]


def AIMove(play, brd):
    result = MiniMaxAB(brd, len(emptyCells(brd)), -INF, INF, play)
    setMove(brd, result[0], result[1], play)
    printBoard(brd)


def setBoard(boardString):

    global BEGINING_STEP

    xNum = 0
    oNum = 0

    for i in range(len(boardString)):
        ch = boardString[i]
        col = i % 3
        row = int(i / 3)
        if ch == 'x':
            xNum += 1
            board[row][col] = XPLAYER
        elif ch == 'o':
            oNum += 1
            board[row][col] = OPLAYER
        else: board[row][col] = EMPTY

    BEGINING_STEP = xNum + oNum

    if xNum < oNum:
        return XPLAYER
    elif xNum > oNum:
        return OPLAYER
    else:
        return XPLAYER

def calScoreByTree(state, player):

    scores = []

    for i in range(len(LNodes)):

        diff = 0
        empty_num_a = 0
        empty_num_b = 0 
        for j in range(len(LNodes[i]['brd'])):

            if LNodes[i]['brd'][j] == '-':
                empty_num_a += 1
            if state[j] == '-':
                empty_num_b += 1

            if LNodes[i]['brd'][j] != state[j]:
                diff += 1
        
        if diff == 1 and empty_num_b > empty_num_a:
            scores.append(LNodes[i]['score'])
        if diff == 0:
            return LNodes[i]['score']

    if len(scores) > 0:

        if player == XPLAYER:
            final_score = min(scores)
        else:
            final_score = max(scores)

        LNodes.append({'brd': state, 'score': final_score})

        return final_score


def output(state):
    score = calScoreByTree(state['brd'], state['player'])
    preList.append(str(state['brd']) + ' ' + str(score))
    
def main():

    global ENABLE_AB
    global MAX_STEP
    global EARLY_TERMINATION

    args = (sys.argv)

    boardString = args[1]

    player = setBoard(boardString)

    if len(args) > 3:
        if args[3] == 'prune':
            ENABLE_AB = True

    if len(args) > 4:
        EARLY_TERMINATION = True
        MAX_STEP = int(args[4])

    AIMove(player, board)

    if len(args) > 2:
        filePath = args[2]
        visited_file = open(filePath, 'w')

        for line in preList:
            visited_file.write(line + '\n')

if __name__ == '__main__':
    main()