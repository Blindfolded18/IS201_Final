import random

from game import Player, Side, BoardView, has_won


class MinimaxAi(Player):
    """
    An AI of the game
    """

    def decide_move(self, board_view: BoardView, current_side: Side) -> int:
        # it saves a lot of runtime cost
        if all(tile is None for tile in board_view):
            return random.randrange(0, 9)

        board = list(board_view)

        move_scores = _move_scores(board, current_side, True)
        best_move, max_score = next(move_scores)
        best_move = [best_move]
        for move, score in move_scores:
            if score > max_score:
                max_score = score
                best_move = [move]
            elif score == max_score:
                best_move.append(move)

        return random.choice(best_move)


def _minimax(board: list[Side | None], current_side: Side, is_maximizing: bool) -> int:
    if not is_maximizing and has_won(board, current_side):
        return 1
    elif is_maximizing and has_won(board, current_side.swap_side()):
        return -1
    elif None not in board:
        return 0

    scores = (score for move, score in _move_scores(board, current_side, is_maximizing))
    return max(scores) if is_maximizing else min(scores)


def _move_scores(board: list[Side | None], current_side: Side, is_maximizing: bool):
    for i in (i for i in range(len(board)) if board[i] is None):
        board[i] = current_side if is_maximizing else current_side.swap_side()
        yield i, _minimax(board, current_side, not is_maximizing)
        board[i] = None
