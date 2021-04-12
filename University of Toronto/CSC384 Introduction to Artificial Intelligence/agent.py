#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
An AI player for Othello. 
"""

import sys
import math
from heapq import heappush
from tkinter.constants import TRUE

# You can use the functions in othello_shared to write your AI

from othello_shared import find_lines, get_possible_moves, get_score, \
    play_move

cached_states = {}
BLACK_COLOR = 1
WHITE_COLOR = 2

def eprint(*args, **kwargs): #you can use this for debugging, as it will print to sterr and not stdout
    print(*args, file=sys.stderr, **kwargs)

# Method to compute util value of terminal state

def compute_utility(board, color):

    # IMPLEMENT

    util = 0
    score = get_score(board)
    if color == BLACK_COLOR:
        util = score[0] - score[1]
    else:
        util = score[1] - score[0]

    return util


# Better heuristic value of board

def compute_heuristic(board, color):  # not implemented, optional

    # IMPLEMENT

    return 0  # change this!


############ MINIMAX ###############################

def minimax_min_node(board, color, limit, caching=0):

    # IMPLEMENT (and replace the line below)

    if caching == 1:
        if board in cached_states:
            return cached_states[board]

    next_color = WHITE_COLOR if color == BLACK_COLOR else BLACK_COLOR

    moves = get_possible_moves(board, next_color)
    # print(all_moves)

    if len(moves) == 0 or limit == 0:
        return None, compute_utility(board, color)
    else:
        mini_val = float('inf')
        mini_move = None

        a = 0
        while a < len(moves):
            (move, util) = minimax_max_node(play_move(board, next_color, moves[a][0], moves[a][1]), color, limit - 1)

            if caching == 1:
                cached_states[play_move(board, next_color, moves[a][0], moves[a][1])] = (move, util)

            if util < mini_val:
                mini_val = util
                mini_move = moves[a]

            a += 1

    return (mini_move, mini_val)


def minimax_max_node(board, color, limit, caching=0):  # returns highest possible util

    # IMPLEMENT (and replace the line below)

    next_color = WHITE_COLOR if color == BLACK_COLOR else BLACK_COLOR

    moves = get_possible_moves(board, next_color)
    # print(all_moves)

    if len(moves) == 0 or limit == 0:
        return None, compute_utility(board, color)
    else:
        mini_val = float('inf')
        mini_move = None

        a = 0
        while a < len(moves):
            (move, util) = minimax_max_node(play_move(board, next_color, moves[a][0], moves[a][1]), color, limit - 1)

            if caching == 1:
                cached_states[play_move(board, next_color, moves[a][0], moves[a][1])] = (move, util)

            if util < mini_val:
                mini_val = util
                mini_move = moves[a]

            a += 1

    return (mini_move, mini_val)


def select_move_minimax(board, color, limit, caching=0):
    """
    Given a board and a player color, decide on a move. 
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.  

    Note that other parameters are accepted by this function:
    If limit is a positive integer, your code should enfoce a depth limit that is equal to the value of the parameter.
    Search only to nodes at a depth-limit equal to the limit.  If nodes at this level are non-terminal return a heuristic 
    value (see compute_utility)
    If caching is ON (i.e. 1), use state caching to reduce the number of state evaluations.
    If caching is OFF (i.e. 0), do NOT use state caching to reduce the number of state evaluations.    
    """

    # IMPLEMENT (and replace the line below)

    moves = get_possible_moves(board, color)

    if len(moves) == 0 or limit == 0:
        return (None, compute_utility(board, color))

    return minimax_max_node(board, color, limit, caching)[0]

############ ALPHA-BETA PRUNING #####################

def alphabeta_min_node(
    board,
    color,
    alpha,
    beta,
    limit,
    caching=0,
    ordering=0,
    ):

    # IMPLEMENT (and replace the line below)

    if caching == 1:
        if (board, color) in cached_states:
            return cached_states[(board, color)]

    next_color = WHITE_COLOR if color == BLACK_COLOR else BLACK_COLOR

    moves = get_possible_moves(board, next_color)

    if len(moves) == 0 or limit == 0:
        return (None, compute_utility(board, color))
    else:
        ab_min = float('inf')
        ab_move = None

        move_list = [(i, play_move(board, next_color, i[0], i[1])) for i in moves]

        if ordering == 1:
            move_list.sort(key=lambda x: compute_utility(x[1], color))

        a = 0
       
        while a < len(move_list):
            (move, util) = alphabeta_max_node(move_list[a][1], color, alpha, beta, limit - 1)

            if caching == 1:
                cached_states[move_list[a][1]] = (move, util)

            if util < ab_min:
                ab_min = util
                ab_move = move_list[a][0]

            if ab_min <= alpha:
                return ab_move, ab_min

            if ab_min < beta:
                beta = ab_min
                if beta <= alpha:
                    break
            a += 1

        return ab_move, ab_min


def alphabeta_max_node(
    board,
    color,
    alpha,
    beta,
    limit,
    caching=0,
    ordering=0,
    ):

    #if level >= limit:
    #    return compute_utility(board, color)

    moves = get_possible_moves(board, color)

    if len(moves) == 0 or limit == 0:
        return (None, compute_utility(board, color))
    else:
        ab_max = float('-inf')
        ab_move = None

        move_list = [(i, play_move(board, color, i[0], i[1])) for i in moves]

        if ordering == 1:
            move_list.sort(key=lambda utilities: compute_utility(utilities[1], color), reverse=True)
      
        a = 0
        while a < len(move_list):
            # print(move_list[a])
            (move, util) = alphabeta_min_node(move_list[a][1], color, alpha, beta, limit - 1)

            if caching == 1:
                cached_states[move_list[a][1]] = (move, util)

            if util > ab_max:
                ab_max = util
                ab_move = move_list[a][0]

            if ab_max >= beta:
                return ab_move, ab_max

            if ab_max > alpha:
                alpha = ab_max
                if beta <= alpha:
                    break
            a += 1

        return (ab_move, ab_max)


def select_move_alphabeta(
    board,
    color,
    limit,
    caching=0,
    ordering=0,
    ):
    """
    Given a board and a player color, decide on a move. 
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.  

    Note that other parameters are accepted by this function:
    If limit is a positive integer, your code should enfoce a depth limit that is equal to the value of the parameter.
    Search only to nodes at a depth-limit equal to the limit.  If nodes at this level are non-terminal return a heuristic 
    value (see compute_utility)
    If caching is ON (i.e. 1), use state caching to reduce the number of state evaluations.
    If caching is OFF (i.e. 0), do NOT use state caching to reduce the number of state evaluations.    
    If ordering is ON (i.e. 1), use node ordering to expedite pruning and reduce the number of state evaluations. 
    If ordering is OFF (i.e. 0), do NOT use node ordering to expedite pruning and reduce the number of state evaluations. 
    """

    moves = get_possible_moves(board, color)

    alpha = float('-inf')
    beta = float('inf')

    bestmove = None

    if limit == 0 or len(moves) == 0:
        return compute_utility(board, color)

    i = 0
    while i < len(moves):
        next_board = play_move(board, color, moves[i][0], moves[i][1])
        util = alphabeta_min_node(next_board, color, alpha, beta, limit - 1, caching, ordering)[1]
        if util > alpha:
            alpha = util
            bestmove = moves[i]
        i += 1
    return bestmove


####################################################

def run_ai():
    """
    This function establishes communication with the game manager.
    It first introduces itself and receives its color.
    Then it repeatedly receives the current score and current board state
    until the game is over.
    """

    print('Othello AI')  # First line is the name of this AI
    arguments = input().split(',')

    color = int(arguments[0])  # Player color: 1 for dark (goes first), 2 for light.
    limit = int(arguments[1])  # Depth limit
    minimax = int(arguments[2])  # Minimax or alpha beta
    caching = int(arguments[3])  # Caching
    ordering = int(arguments[4])  # Node-ordering (for alpha-beta only)
    #global cached_states
    #cached_states = {}

    if minimax == 1:
        eprint('Running MINIMAX')
    else:
        eprint('Running ALPHA-BETA')

    if caching == 1:
        eprint('State Caching is ON')
    else:
        eprint('State Caching is OFF')

    if ordering == 1:
        eprint('Node Ordering is ON')
    else:
        eprint('Node Ordering is OFF')

    if limit == -1:
        eprint('Depth Limit is OFF')
    else:
        eprint('Depth Limit is ', limit)

    if minimax == 1 and ordering == 1:
        eprint('Node Ordering should have no impact on Minimax')

    while True:  # This is the main loop

        # Read in the current game status, for example:
        # "SCORE 2 2" or "FINAL 33 31" if the game is over.
        # The first number is the score for player 1 (dark), the second for player 2 (light)

        next_input = input()
        (status, dark_score_s, light_score_s) = \
            next_input.strip().split()

        # dark_score = int(dark_score_s)
        # light_score = int(light_score_s)

        if status == 'FINAL':  # Game is over.
            print
        else:
            board = eval(input())  # Read in the input and turn it into a Python

                                  # object. The format is a list of rows. The
                                  # squares in each row are represented by
                                  # 0 : empty square
                                  # 1 : dark disk (player 1)
                                  # 2 : light disk (player 2)

            # Select the move and send it to the manager

            if minimax == 1:  # run this if the minimax flag is given
                (movei, movej) = select_move_minimax(board, color, limit,
                        caching)
            else:

                  # else run alphabeta

                (movei, movej) = select_move_alphabeta(board, color, limit,
                        caching, ordering)

            print ('{} {}'.format(movei, movej))


if __name__ == '__main__':
    run_ai()
