import sys
import numpy as np
import random
random.seed(1)

# HYPER-PARAMETERS
N = 4
START = -0.1
MAX_EPISODES = 100000
EPISODE_COUNT = 1

# learning rate
ALPHA = 0.3 
# how much we weight future rewards as opposed to immediate rewards
GAMMA = 0.1 
# the balance between exploration and exploitation
EPSILON = 0.5
og_parameters = [ALPHA, GAMMA, EPSILON]

START_INDEX = 2

# main function
def create_board(goal_a, goal_b, forbid, wall):

    N = 4
    reward = -0.1
    prize = 100.0

    board = np.ones((17), dtype=int)*reward

    # set the forbid position
    board[forbid] = -prize
    # set the goal position
    board[goal_a] = prize
    board[goal_b] = prize

    return board


# auxiliary function, prints the Q table in a fancy way
def print_special_q(board, q_table, index):
    val = q_table[index] 

    moves = ["up","right","down","left"]
    for i in [0,1,2,3]:
        print(moves[i] + ' ' + str(round(val[i], 4)))

# auxiliary function, prints the Q table in a fancy way
def print_q_table(board, q_table): 

    start_state = START_INDEX
    goal_states = [GOAL_A, GOAL_B]
 
    moves = ["up","right","down","left"]
    state_update_rule = {0: +N, 1: +1, 2: -N, 3: -1}

    for index in range(1, 17):

        if index in goal_states:
            print(str(index) + ' ' + 'goal')
        elif index == WALL_INDEX:
            print(str(index) + ' ' + 'wall-square')
        elif index == FORBID_INDEX:
            print(str(index) + ' ' + 'forbid')
        else:
            max_q = -10000
            max_index = 0
            val = q_table[index]
            for jdx,jv in enumerate(val):
                if index + state_update_rule[jdx] != WALL_INDEX:
                    if jv > max_q:
                        max_q = jv
                        max_index = jdx
            print(str(index) + ' ' + moves[max_index])
            

# main function, applies the Q-Learning algorithm on the given board
def q_learning(board, OAL_A, GOAL_B, FORBID_INDEX, WALL_INDEX): 

    global EPISODE_COUNT

    # the 4 actions are: LEFT, UP, RIGHT, DOWN
    q_table = np.full((17, 4), 0.0) 

    statu_table = np.full((17, 4), None) 
    cell_counter = 0
    for i in range(17):
        if(i not in [13, 14, 15, 16]): statu_table[cell_counter][0] = 0
        if(i not in [16, 12, 8, 4]): statu_table[cell_counter][1] = 0
        if(i not in [1, 2, 3, 4]): statu_table[cell_counter][2] = 0
        if(i not in [1, 5, 9, 13]): statu_table[cell_counter][3] = 0
        cell_counter += 1

    # get the start and finish states
    start_state = START_INDEX
    end_states = [GOAL_A, GOAL_B, FORBID_INDEX]

    state_update_rule = {0: +N, 1: +1, 2: -N, 3: -1}

    # APPLY THE Q-LEARNING ALGORITHM
    while(EPISODE_COUNT<MAX_EPISODES):
        current_state = start_state

        # get to the end of the board
        while(True):
             
            # select every possible action
            possible_actions = [j for j in range(len(statu_table[current_state])) if(not (statu_table[current_state][j] is None))]
            random_number = random.random()

            if(random_number<EPSILON): # we explore
                action = random.randint(0,3)
                
            else: # we exploit

                # get the action that maximizes our rewards
                aux = -sys.maxsize
                action = 0
                for i in [0, 1, 2, 3]:
                    # if better, save this action
                    if(q_table[current_state][i]>aux): 
                        action = i
                        aux = q_table[current_state][i]

          
            if action not in possible_actions:

                # compute the immediate reward
                immediate_reward = -0.1
                # compute the approximation of future rewards
                future_reward = max(q_table[current_state])
                q_table[current_state][action] += ALPHA * (immediate_reward + (GAMMA * future_reward) - q_table[current_state][action])
                continue
    
            # move to the next state, compute immediate and future rewards
            # carry out the chosen action
            new_state = current_state + state_update_rule[action]
    
            # compute the immediate reward
            immediate_reward = board[new_state]

            # compute the approximation of future rewards
            future_reward = max(q_table[new_state])
            if new_state == WALL_INDEX:
                future_reward = max([i for i in q_table[current_state] if(not (i is None))])

            # update the Q table
            q_table[current_state][action] += ALPHA * (immediate_reward + (GAMMA * future_reward) - q_table[current_state][action])
            #print(q_table[start_state])

            # move to the chosen state
            if new_state != WALL_INDEX:
                current_state = new_state

            # we have reached the end state, we can stop
            if new_state in end_states: break

        EPISODE_COUNT += 1
    
    return(q_table)


if __name__ == "__main__":

    # user input parse

    nums = input ()
    args = nums.split(' ')
    goal_a = int(args[0])
    goal_b = int(args[1])
    forbid = int(args[2])
    wall = int(args[3])
    pclass = args[4]
    index = 1

    if len(args) > 5:
        index = int(args[5])

    GOAL_A = goal_a
    GOAL_B = goal_b
    FORBID_INDEX = forbid
    WALL_INDEX = wall

    # create a NxN board
    board = create_board(GOAL_A, GOAL_B, FORBID_INDEX, WALL_INDEX)

    # build the Q table
    q_table = q_learning(board, GOAL_A, GOAL_B, FORBID_INDEX, WALL_INDEX)

    # print the Q table
    if pclass == 'p':
        print_q_table(board, q_table)
    else:
        print_special_q(board, q_table, index)
