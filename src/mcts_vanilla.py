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

def traverse_nodes(node, board, state, identity):
    """ Traverses the tree until the end criterion are met.

    Args:
        node:       A tree node from which the search is traversing.
        board:      The game setup.
        state:      The state of the game.
        identity:   The bot's identity, either 'red' or 'blue'.

    Returns:        A node from which the next stage of the search can proceed.

    """
    current_node = node
    if len(node.child_nodes) != 0:
        max_uct_value = float('-inf')
        best_child = None
        best_action = ()
        for key_action, child_node in node.child_nodes.items():
            if child_node.visits == 0:
                current_node = child_node
                return current_node
            else:
                # ---- RED 'X' and BLUE 'O' UCT ---- 
                # Upper Confidence Bounds for Trees (UCT)
                # w_i / n_i + c * sqrt( ln(t)/ n_i )
                # or ( 1 - UCT )
                print("Current Player:", board.current_player(state))
                if board.current_player(state) is identity:
                    uct_value = ( child_node.wins/child_node.visits ) + explore_faction * (sqrt( log(node.visits, e)/ child_node.visits))
                else:
                    uct_value = (1 - ( node.child_nodes[child_node].wins/node.child_nodes[child_node].visits ) + explore_faction * (sqrt( log(node.visits, e)/ node.child_nodes[child_node].visits)))
            if uct_value > max_uct_value:
                max_uct_value = uct_value
                best_child = child_node
                best_action = key_action
        # Sets best child to current node
        current_node = best_child
        # Changes state of the board accordingly
        state = board.next_state(state, best_action)
    return current_node
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
    random_action = choice(board.legal_actions(state))
    state = board.next_state(state, random_action)
    new_node = MCTSNode(parent=node, parent_action=random_action, action_list=board.legal_actions(state))
    node.child_nodes[random_action] = new_node

    return new_node
    # Hint: return new_node


def rollout(board, state):
    """ Given the state of the game, the rollout plays out the remainder randomly.
        Example Heuristics for modified:
            -   Always connect third X/0 if possible
            -   Always block third X/0 if possible
    Args:
        board:  The game setup.
        state:  The state of the game.

    """
    while not board.is_ended(state):
        random_action = choice(board.legal_actions(state))
        state = board.next_state(state, random_action)
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

    value_dictionary = {}
    for step in range(num_nodes):
        print("step:", step)
        # Copy the game for sampling a playthrough
        sampled_game = state

        # Start at root
        node = root_node

        # Do MCTS - This is all you!
        # Selection
        node = traverse_nodes(node, board, sampled_game, identity_of_bot)
        # Expansion
        leaf = expand_leaf(node, board, sampled_game)
        sampled_game = board.next_state(sampled_game, leaf.parent_action)
        # Simulation
        won = rollout(board, sampled_game)
        # Backpropagation
        backpropagate(node, won[identity_of_bot])

        value_dictionary[node] = node.wins
        max_value_action = max(value_dictionary, key=value_dictionary.get)

    # Return an action, typically the most frequently used action (from the root) or the action with the best
    # estimated win rate.
    print("Vanilla bot is picking...", max_value_action.wins)
    return max_value_action
