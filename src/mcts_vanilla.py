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
    max_uct_value = None
    leaf_found = False
    for child_node in node.child_nodes and leaf_found == False:
        if not child_node.child_nodes:
            leaf_found = True
        else:
            # Upper Confidence Bounds for Trees (UCT)
            # w_i / n_i + c * sqrt( ln(t)/ n_i )
            uct_value = ( child_node.wins/child_node.visits ) + explore_faction * (sqrt( log(node.visits, e)/ child_node.visits))
            
            # Find the maximum UCT value amongst current node's children
            if max_uct_value == None:
                uct_value = max_uct_value
            else:
                if uct_value > max_uct_value:
                    max_uct_value = uct_value


    return child_node
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
    while not board.is_ended(state):
        random_action = choice(board.legal_actions(state))
        board.next_state(state, random_action)
    return board.win_values(state)



def backpropagate(node, won):
    """ Navigates the tree from a leaf node to the root, updating the win and visit count of each node along the path.
        Backpropagate recursively
    Args:
        node:   A leaf node.
        won:    An indicator of whether the bot won or lost the game.

    """
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



    # Return an action, typically the most frequently used action (from the root) or the action with the best
    # estimated win rate.
    return None
