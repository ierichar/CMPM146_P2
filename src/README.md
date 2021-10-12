Ian Richardson and Ethan Erh

For mcts_modified, we implemented a light-weight check in rollout that checks
the current board state and analyzes where there is a position to win a board
(i.e. three in a row) or block the opponents winning move. The helper functions
find_wins() and find_blocks() are intended to return positions on the board
that can return a win or block on the current board.