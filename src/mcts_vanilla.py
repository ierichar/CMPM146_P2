from mcts_node import MCTSNode
from random import choice
from math import e, sqrt, log

import p2_t3

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

    """
    # # Go first
    # if identity is 'red':
    #     if node.child_nodes.empty():
    #         return node
    #     else:
    #         for child_node in node.child_nodes:
    #             max_uct_value = None
    #             # Upper Confidence Bounds for Trees (UCT)
    #             # w_i / n_i + c * sqrt( ln(t)/ n_i )
    #             uct_value = ( child_node.wins/child_node.visits ) + explore_faction * (sqrt( log(node.visits, e)/ child_node.visits))
                
    #             # Find the maximum UCT value amongst current node's children
    #             if max_uct_value == None:
    #                 uct_value = max_uct_value
    #             else:
    #                 if uct_value > max_uct_value:
    #                     max_uct_value = uct_value
    # # Go second
    # else:
    #     # Play for minimum
    #     return None

    # Recursive Function
    if len(node.untried_actions) == 0:
        print("node has no untried actions")
        return node
    elif len(node.child_nodes) == 0:
        print("node has no children")
        return node
    else:
        max_uct_value = None
        best_child = None
        for child_node in node.child_nodes:
            # ---- RED 'X' UCT ---- (need a BLUE or 'O' UCT)
            # Upper Confidence Bounds for Trees (UCT)
            # w_i / n_i + c * sqrt( ln(t)/ n_i )
            uct_value = ( child_node.wins/child_node.visits ) + explore_faction * (sqrt( log(node.visits, e)/ child_node.visits))
            
            # Find the maximum UCT value amongst current node's children
            if max_uct_value == None:
                uct_value = max_uct_value
                best_child = child_node
            else:
                if uct_value > max_uct_value:
                    max_uct_value = uct_value
                    best_child = child_node
        print("traversing best node")
        return traverse_nodes(best_child, board, state, identity)

    # Hint: return leaf_node


def expand_leaf(node, board, state):
    """ Adds a new leaf to the tree by creating a new child node for the given node.

    Args:
        node:   The node for which a child will be added.
        board:  The game setup.
        state:  The state of the game.

    Returns:    The added child node.

    """
    # Select a random_action from untried_actions
    print("adding a new node")
    random_action = choice(node.untried_actions)
    new_node = MCTSNode(parent=node, parent_action=random_action, action_list=board.legal_actions(state))
    node.child_nodes[random_action] = new_node
    new_node.parent = node

    return new_node
    # Hint: return new_node


def rollout(board, state):
    """ Given the state of the game, the rollout plays out the remainder randomly.
        Example Heuristics:
            -   Always connect third X/0 if possible
            -   Always block third X/0 if possible
    Args:
        board:  The game setup.
        state:  The state of the game.

    """
    # RED vs BLUE simulation 
    # Current player needs to be accounted for
    print("autobots rollout")
    while not board.is_ended(state):
        random_action = choice(board.legal_actions(state))
        print("action is", random_action)
        board.next_state(state, random_action)

    return board.win_values(state)



def backpropagate(node, won):
    """ Navigates the tree from a leaf node to the root, updating the win and visit count of each node along the path.
        Backpropagate recursively
    Args:
        node:   A leaf node.
        won:    An indicator of whether the bot won or lost the game.

    """
    print("backpropagate")
    if node.parent is None:
        return
    node.wins += won
    node.visit += 1
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

    highest_value = None
    best_action = None
    for step in range(num_nodes):
        # Copy the game for sampling a playthrough
        sampled_game = state

        # Start at root
        node = root_node

        # Do MCTS - This is all you!
        # Selection
        leaf = traverse_nodes(node, board, sampled_game, identity_of_bot)
        # Expansion
        expand_leaf(leaf, board, sampled_game)
        # Simulation
        won = rollout(board, sampled_game)
        # Backpropagation
        backpropagate(leaf, won)

        if highest_value == None:
            highest_value = won
            best_action = leaf
        else:
            if won > highest_value:
                highest_value = won
                best_action = leaf


    # Return an action, typically the most frequently used action (from the root) or the action with the best
    # estimated win rate.
    print("Vanilla bot is picking...")
    return best_action
