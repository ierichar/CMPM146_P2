
from mcts_node import MCTSNode
from random import choice
from math import sqrt, log

num_nodes = 1000
explore_faction = 2.

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
    print('Running Traverse: (bode, board, state, identity)')
    # print('Node: ', node, '\n')
    print('Board: ', board, '\n')
    print('State: ', state, '\n')
    print('Identity: ', identity, '\n')
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
            print('UTC before min/max: ', utc)
            # Obtaining min/max modifier
            minmax = pow(-1, modifier + package[1])
            # Applying modifier
            utc *= minmax
            print('UTC after min/max: ', utc)
            print('min/max: ', minmax)
            """
            Maybe a way to minimize/maximize the utc?
            This way the loss is prioritized if its the opponent's move
            if (its not player's turn):
                utc *= -1
            """
            # Adding utc with its key to the utc list for sorting
            utc_list.append((key, utc))
        print('\n', 'Getting all utcs completed', '\n')

        # Pushing to stack in utc order
        while (len(utc_list) > 0):
            # Obtaining best utc (index, utc)
            best = (0, utc_list[0][1])
            for num in range(len(utc_list) - 1):
                index = num + 1
                print(utc_list[index])
                print(best)
                if (best[0] < utc_list[index][1]):
                    best = (index, utc_list[index][1])
            
            # Obtaining node information from key
            best = utc_list.pop(best[0]) # Best (index, utc) -> (key, utc)
            best = current.child_nodes[best[0]] # Best (key, utc) -> (node)
            # Adding to stack
            stack.append(best, package[1] + 1)

        print('\n', 'Pushing to stack completed', '\n')

    # Return None here as finishing the loop means no leafs remain.
    # return None
    pass



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
    print('Running Expand: (node, board, state)')
    # print('Node: ', node, '\n')
    print('Board: ', board, '\n')
    print('State: ', state, '\n')
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

    Args:
        board:  The game setup.
        state:  The state of the game.

    """
    # Testing Purposes ==================================================
    print('Running rollout: (board, state)')
    print('Board: ', board, '\n')
    print('State: ', state, '\n')
    # END ===============================================================

    # Localizing state data
    curr_state = state
    starter_player = board.current_player(state)
    
    # Looping from the current state of the game all the way until a win condition
    while not (board.is_ended(curr_state)):
        #print('Current Player: ', board.current_player(curr_state))
        #print('Current state: ', curr_state)
        action = board.legal_actions(curr_state).pop()
        #print('Action: ', action, '\n')
        new_state = board.next_state(curr_state, action)
        curr_state = new_state
        #print('New state: ', new_state)
    
    stats = board.points_values(curr_state)
    print('Game has ended. Statistics: ', stats)
    print('From perspective: Player ', starter_player)
    
    return board


def backpropagate(node, won):
    """ Navigates the tree from a leaf node to the root, updating the win and visit count of each node along the path.

    Args:
        node:   A leaf node.
        won:    An indicator of whether the bot won or lost the game.

    """
    # Testing Purposes ==================================================
    print('Running Traverse: (node, won)')
    print('Node: ', node, '\n')
    print('Won: ', won, '\n')
    # END ===============================================================

    # Loop from the given node to the root node
    current = node
    while not (current.parent is None):
        # Updating node variables
        current.visits += 1
        current.wins += won

        # Traversing to next node in the sequence
        current = current.parent
    
    # Returns true for successful traversal
    return True


def think(board, state):
    """ Performs MCTS by sampling games and calling the appropriate functions to construct the game tree.

    Args:
        board:  The game setup.
        state:  The state of the game.

    Returns:    The action to be taken.

    """
    # GIVEN
    identity_of_bot = board.current_player(state)
    root_node = MCTSNode(parent=None, parent_action=None, action_list=board.legal_actions(state))

    # Testing Purposes ==================================================
    print('Running Think (board, state)')
    print('Board: ', board, '\n')
    print('State: ', state, '\n')
    # print('Board.Current_Player: ',board.current_player(state))
    print('Board.Legal_Actions', board.legal_actions(state))
    # print('Board.Display', board.display(state)) DOESNT WORK
    # print('Board.points_values', board.points_values(state))
    # print('Root_Node Variable: ', str(root_node))
    # END ===============================================================

    # for step in range(num_nodes):
    for step in range(1): # Testing purposes
        print('Step: ', step, '/', num_nodes)
        # Copy the game for sampling a playthrough
        sampled_game = state

        # Start at root
        node = root_node

        # Do MCTS - This is all you!

        # Getting leaf_node
        leaf_node = traverse_nodes(node, board, sampled_game, identity_of_bot)
        #print('traversal results parent: ', leaf_node.parent_action)

        # Adding to leaf_node
        new_node = expand_leaf(leaf_node, board, sampled_game)
        #print('exapansion results parent: ', new_node.parent_action)

        # Playing out game from the leaf node
        rollout(board, state)

        # Backtracking from the terminal node to the root node
        # backpropagate(node, won)

    # Selecting the best action
    best = None # (node)
    for key in node.child_nodes.keys():
        # Getting action data
        next_state = node.child_nodes[key]
        print(key)

        # Comparing values and assigned new best if applicable
        if not best:
            best = next_state
        elif (best.wins < next_state.wins):
            best = next_state
        elif ((best.wins == next_state.wins) and (best.visits < next_state.visits)):
            best = next_state
    # Return an action, typically the most frequently used action (from the root) or the action with the best
    # estimated win rate.
    return best

def get_state_from_path(board, state, path_list):
    # The current state based off of the path_list
    final_state = state
    while len(path_list) > 0:
        action = path_list.pop(len(path_list) - 1)
        final_state = board.next_state(final_state, action)

    return final_state