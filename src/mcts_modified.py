from sys import _current_frames
from mcts_node import MCTSNode
from random import choice
from math import e, sqrt, log

import p2_t3

num_nodes = 1000
explore_faction = 2.

# Allowed Interface:
# -   board.legal_actions(state)→ returns the moves available in state.
# -   board.next_state(state, action)→ returns a new state constructed by applying action in state.
# -   board.is_ended(state)→ returns True if the game has ended in state and False otherwise.
# -   board.current_player(state)→ returns the index of the current player in state.
# -   board.points_values(state)→ returns a dictionary of the score for each player 
#       (eg {1:-1,2:1} for a second-player win). Will return None if the game is not ended.
# -   board.owned_boxes(state)→ returns a dict with (Row,Column) keys; values indicate for 
#        each box whether player 1, 2, or 0 (neither) owns that box
# -   board.display(state, action)→ returns a string representation of the board state.
# -   board.display_action(action)→ returns a string representation of the game action.

# ----- IAN'S CODE -----
# def traverse_nodes(node, board, state, identity):
#     """ Traverses the tree until the end criterion are met.

#     Args:
#         node:       A tree node from which the search is traversing.
#         board:      The game setup.
#         state:      The state of the game.
#         identity:   The bot's identity, either 'red' or 'blue'.

#     Returns:        A node from which the next stage of the search can proceed.

#     """
#     current_node = node
#     if len(node.child_nodes) != 0:
#         max_uct_value = float('-inf')
#         best_child = None
#         best_action = ()
#         for key_action, child_node in node.child_nodes.items():
#             if child_node.visits == 0:
#                 return child_node
#             else:
#                 # ---- RED 'X' and BLUE 'O' UCT ---- 
#                 # Upper Confidence Bounds for Trees (UCT)
#                 # w_i / n_i + c * sqrt( ln(t)/ n_i )
#                 # or ( 1 - UCT )
#                 print("Current Player:", board.current_player(state))
#                 if board.current_player(state) is identity:
#                     uct_value = ( child_node.wins/child_node.visits ) + explore_faction * (sqrt( log(node.visits, e)/ child_node.visits))
#                 else:
#                     uct_value = (1 - ( child_node.wins/child_node.visits ) + explore_faction * (sqrt( log(node.visits, e)/ child_node.visits)))
#             if uct_value > max_uct_value:
#                 max_uct_value = uct_value
#                 best_child = child_node
#                 best_action = key_action
#         # Sets best child to current node
#         current_node = best_child
#         # Changes state of the board accordingly
#         state = board.next_state(state, best_action)
#     return current_node
#     # Hint: return leaf_node

def traverse_nodes(node, board, state, identity):
    """ Traverses the tree until the end criterion are met.

    Args:
        node:       A tree node from which the search is traversing.
        board:      The game setup.
        state:      The state of the game.
        identity:   The bot's identity, either 'red' or 'blue'.

    Returns:        A node from which the next stage of the search can proceed.
    # Hint: return leaf_node

    """
    # Testing Purposes ==================================================
    # print('Running Traverse: (node, board, state, identity)')
    # print('Node: ', node, '\n')
    # print('Board: ', board, '\n')
    # print('State: ', state, '\n')
    # print('Identity: ', identity, '\n')
    # END ===============================================================

    # Stack is used to keep track of children needed to check
    stack = []
    stack.append((node, 0)) # (Node, Tree depth) Starts with 0/root
    
    # Modifier is used for min/maxing the UTC value
    # Later -1 is raised to the power of depth + modifier
    # This way, one will prioritize the least amount of loss from their persepctive
    modifier = None
    if (identity == board.current_player(state)): # Is player turn
        modifier = 0
    else: # Is opponent turn
        modifier = 1

    while (len(stack) > 0):
        # Loop Updating
        package = stack.pop() # (Node, Tree depth)
        current = package[0] 

        # EXIT CONDITION
        # Checking if there are untried moves, then returns the current node if there are
        if len(current.untried_actions) > 0:
            return current
        
        # If all actions are tried, push the nodes onto the stack in utc order
        # Getting utc of all items
        utc_list = []
        for key in current.child_nodes.keys():
            # Referencing child node
            child = current.child_nodes[key]
            
            # Obtaining UTC
            utc = (child.wins / child.visits) + (explore_faction* (sqrt(log(current.visits)/child.visits)))
            #print('UTC before min/max: ', utc)
            # Obtaining min/max modifier
            minmax = pow(-1, modifier + package[1])
            # Applying modifier
            utc *= minmax
            #print('UTC after min/max: ', utc)
            #print('min/max: ', minmax)
            """
            Maybe a way to minimize/maximize the utc?
            This way the loss is prioritized if its the opponent's move
            if (its not player's turn):
                utc *= -1
            """
            # Adding utc with its key to the utc list for sorting
            utc_list.append((key, utc))
        #print('\n', 'Getting all utcs completed', '\n')

        # Pushing to stack in utc order
        while (len(utc_list) > 0):
            # Obtaining best utc (index, utc)
            best = (0, utc_list[0][1])
            for num in range(len(utc_list) - 1):
                index = num + 1
                #print(utc_list[index])
                #print(best)
                if (best[0] < utc_list[index][1]):
                    best = (index, utc_list[index][1])
            
            # Obtaining node information from key
            best = utc_list.pop(best[0]) # Best (index, utc) -> (key, utc)
            best = current.child_nodes[best[0]] # Best (key, utc) -> (node)
            # Adding to stack
            stack.append((best, package[1] + 1))

        #print('\n', 'Pushing to stack completed', '\n')

    # Return None here as finishing the loop means no leafs remain.
    return None

# ----- Ian's Code ------
# def expand_leaf(node, board, state):
#     """ Adds a new leaf to the tree by creating a new child node for the given node.

#     Args:
#         node:   The node for which a child will be added.
#         board:  The game setup.
#         state:  The state of the game.

#     Returns:    The added child node.

#     """
#     # Select a random_action from untried_actions
#     random_action = choice(board.legal_actions(state))
#     state = board.next_state(state, random_action)
#     new_node = MCTSNode(parent=node, parent_action=random_action, action_list=board.legal_actions(state))
#     node.child_nodes[random_action] = new_node

#     return new_node
#     # Hint: return new_node

def expand_leaf(node, board, state):
    """ Adds a new leaf to the tree by creating a new child node for the given node.

    Args:
        node:   The node for which a child will be added.
        board:  The game setup.
        state:  The state of the game.

    Returns:    The added child node.
    # Hint: return new_node

    """
    # Testing Purposes ==================================================
    #print('Running Expand: (node, board, state)')
    # print('Node: ', node, '\n')
    # print('Board: ', board, '\n')
    # print('State: ', state, '\n')
    # END ===============================================================

    # Obtaining a random action from the given node
    made_action = node.untried_actions.pop()

    # Creating new state based off of action
    new_state = board.next_state(state, made_action)
    
    # Creating a new node object
    new_node = MCTSNode(parent=node, parent_action=made_action, action_list=board.legal_actions(new_state))
    
    # Linking node to tree
    node.child_nodes[made_action] = new_node

    # Return the new node
    return new_node


def rollout(board, state):
    """ Given the state of the game, the rollout plays out the remainder randomly.
        Example Heuristics for modified:
            -   Always connect third X/0 if possible
            -   Always block third X/0 if possible
    Args:
        board:  The game setup.
        state:  The state of the game.

    """
    #print("rolling out")
    while not board.is_ended(state):

        # Finding heuristics
        wins = (find_wins(board, state))
        blocks = (find_blocks(board, state))

        # Determining action
        action = choice(board.legal_actions(state))
        action_list = list(action)
        if wins is not None:
            action_list[2] = wins[0]
            action_list[3] = wins[1]
            action = tuple(action_list)
            #print("found winning action:", action)
        elif blocks is not None:
            action_list[2] = blocks[0]
            action_list[3] = blocks[1]
            action = tuple(action_list)
            #print("found blocking action:", action)
        #print("legal actions:", board.legal_actions(state))
        if action not in board.legal_actions(state):
            action = action = choice(board.legal_actions(state))
        #print("eventual action:", action)

        state = board.next_state(state, action)
    return board.points_values(state)


def backpropagate(node, won):
    """ Navigates the tree from a leaf node to the root, updating the win and visit count of each node along the path.
        Backpropagate recursively
    Args:
        node:   A leaf node.
        won:    An indicator of whether the bot won or lost the game.

    """
    node.wins += won
    node.visits += 1
    if node.parent is None:
        return
    backpropagate(node.parent, won)



def think(board, state):
    """ Performs MCTS by sampling games and calling the appropriate functions to construct the game tree.

    Args:
        board:  The game setup.
        state:  The state of the game.

    Returns:    The action to be taken.

    """
    identity_of_bot = board.current_player(state)
    root_node = MCTSNode(parent=None, parent_action=None, action_list=board.legal_actions(state))
    #print('Action selection list', root_node.untried_actions)

    value_dictionary = {}
    for step in range(num_nodes):
        #print("step:", step)
        # Copy the game for sampling a playthrough
        sampled_game = state

        # Start at root
        node = root_node

        # Do MCTS - This is all you!
        # Selection
        node = traverse_nodes(node, board, sampled_game, identity_of_bot)
        # Expansion
        if node is None:
            break
        actions_to_leaf = return_from_node(node, board, sampled_game)
        actions_to_leaf.reverse()
        leaf = expand_leaf(node, board, sampled_game)
        actions_to_leaf.append(leaf.parent_action)
        #print(board.display(sampled_game, leaf.parent_action))
        #print(actions_to_leaf)
        # Simulation
        won = rollout(board, get_state_from_path(board, sampled_game, actions_to_leaf))
        # Backpropagation
        backpropagate(leaf, won[identity_of_bot])

        value_dictionary[node] = node.wins
        max_value_action = max(value_dictionary, key=value_dictionary.get)

        #print(max_value_action.parent_action)

    # Return an action, typically the most frequently used action (from the root) or the action with the best
    # estimated win rate.

    # Selecting the best action
    best = None # (node)
    for key in root_node.child_nodes.keys():
        # Getting action data
        next_node = root_node.child_nodes[key]

        # Comparing values and assigned new best if applicable
        if not best:
            best = next_node
        elif (best.wins < next_node.wins):
            best = next_node
        elif ((best.wins == next_node.wins) and (best.visits < next_node.visits)):
            best = next_node

    #print("Modified bot is picking...", best.parent_action)
    return best.parent_action


def return_from_node(node, board, state):
    # Helper function: returns a list of nodes to get to current leaf
    if node.parent is None:
        return []
    return return_from_node(node.parent, board, state) + [node.parent_action]

def get_state_from_path(board, state, path_list):
    # Helper function: returns the state at the leaf node
    # takes a list of actions on the board to get to the leaf node
    # The current state based off of the path_list
    final_state = state
    while len(path_list) > 0:
        action = path_list.pop(len(path_list) - 1)
        final_state = board.next_state(final_state, action)

    return final_state

def find_wins(board, state):
    # args: board, state
    # return: (x, y) tuple -> the position to win the board state
    # if no position that meets criteria, return None
    ownership = board.owned_boxes(state) # [][] -> 1, 2, 0
    my_player = board.current_player(state)
    #print("ownership:", ownership)
    #print("my_player:", my_player)
    box1 = None
    box2 = None
    for a in range(3):
        for b in range(3):
            # potential change to include 1 or 2 in same loop for efficiency
            if (ownership[a, b] == my_player):
                box1 = a, b
                for x in range(3):
                    for y in range(3):
                        # potential change to include 1 or 2 in same loop for efficiency
                        if (ownership[x, y] == my_player):
                            box2 = x, y
                            if box1 is not None and box2 is not None and box1 != box2:
                                # Handle horizontals
                                if box1[0] == box2[0]:
                                    y_sum = box1[1] + box2[1]
                                    if y_sum == 1: 
                                        if ownership[box1[0], 2] == 0: 
                                            return box1[0], 2
                                    if y_sum == 2:
                                        if ownership[box1[0], 1] == 0: 
                                            return box1[0], 1
                                    if y_sum == 3:
                                        if ownership[box1[0], 0] == 0: 
                                            return box1[0], 0
                                # Handle verticals
                                elif box1[1] == box2[1]:
                                    x_sum = box1[0] + box2[0]
                                    if x_sum == 1: 
                                        if ownership[2, box1[1]] == 0: 
                                            return 2, box1[1]
                                    if x_sum == 2: 
                                        if ownership[1, box1[1]] == 0: 
                                            return 1, box1[1]
                                    if x_sum == 3: 
                                        if ownership[0, box1[1]] == 0: 
                                            return 0, box1[1]
                                # Handle diagonals
                                else:
                                    x_y_sum = box1 + box2
                                    if x_y_sum == (3, 3): return 0, 0
                                    if x_y_sum == (2, 2): return 1, 1
                                    if x_y_sum == (1, 1): return 2, 2
                                    if x_y_sum == (1, 3): return 0, 2
                                    if x_y_sum == (3, 1): return 2, 0
    
    return None

    # p1 = []
    # p2 = []
    # blocks = {}
    # # Adds ownership to boxes
    # for x in range(3):
    #     for y in range(3):
    #         if (ownership[x][y] == 1):
    #             p1.append((x, y))
    #         elif (ownership[x][y] == 2):
    #             p2.append((x, y))
            
    # if len(p1) > 1:
    #     for index in range(len(p1) - 2): # (x, y)
    #         box = p1[index]
    #         for index2 in range(len(p1) - 1 - index):
    #             box2 = p1[index + 1]

    # if len(p2) > 1:
    #     for box in p1: # (x, y)
    #         continue

def find_blocks(board, state):
    # args: board, state
    # return: (x, y) tuple -> the position to win the board state
    # if no position that meets criteria, return None
    ownership = board.owned_boxes(state) # [][] -> 1, 2, 0
    my_player = board.current_player(state)
    #print("ownership:", ownership)
    #print("my_player:", my_player)
    box1 = None
    box2 = None
    for a in range(3):
        for b in range(3):
            # potential change to include 1 or 2 in same loop for efficiency
            if (ownership[a, b] != my_player and ownership[a, b] != 0):
                box1 = a, b
                for x in range(3):
                    for y in range(3):
                        # potential change to include 1 or 2 in same loop for efficiency
                        if (ownership[x, y] != my_player and ownership[x, y] != 0):
                            box2 = x, y
                            if box1 is not None and box2 is not None and box1 != box2:
                                # Handle horizontals
                                if box1[0] == box2[0]:
                                    y_sum = box1[1] + box2[1]
                                    if y_sum == 1: 
                                        if ownership[box1[0], 2] == 0: 
                                            return box1[0], 2
                                    if y_sum == 2:
                                        if ownership[box1[0], 1] == 0: 
                                            return box1[0], 1
                                    if y_sum == 3:
                                        if ownership[box1[0], 0] == 0: 
                                            return box1[0], 0
                                # Handle verticals
                                elif box1[1] == box2[1]:
                                    x_sum = box1[0] + box2[0]
                                    if x_sum == 1: 
                                        if ownership[2, box1[1]] == 0: 
                                            return 2, box1[1]
                                    if x_sum == 2: 
                                        if ownership[1, box1[1]] == 0: 
                                            return 1, box1[1]
                                    if x_sum == 3: 
                                        if ownership[0, box1[1]] == 0: 
                                            return 0, box1[1]
                                # Handle diagonals
                                else:
                                    x_y_sum = box1 + box2
                                    if x_y_sum == (3, 3): return 0, 0
                                    if x_y_sum == (2, 2): return 1, 1
                                    if x_y_sum == (1, 1): return 2, 2
                                    if x_y_sum == (1, 3): return 0, 2
                                    if x_y_sum == (3, 1): return 2, 0
    
    return None