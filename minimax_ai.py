import random

from game import Player, Side, BoardView, has_won


class MinimaxAi(Player):
    """
    An AI of the game
    """

    def __init__(self, think_chance: float = 1.0):
        """
        Initializes an AI
        :param think_chance: the chance that it gives up to think and decide to move randomly instead.
        Note that it will still block obvious about-to-win and decide a move leading to a win
        """
        self._think_chance = think_chance

    def decide_move(self, board_view: BoardView, current_side: Side) -> int:
        # it saves a lot of runtime cost
        # it is guaranteed that all the tiles in the empty board have equal chances of winning
        if all(tile is None for tile in board_view):
            return random.randrange(0, 9)

        # it applies for both "smart" case and "stupid" case
        match _find_win_move(board_view, current_side):
            case None: pass
            case at: return at

        # stupid moment
        if random.random() >= self._think_chance:
            # but still don't be so stupid! You have to check for the possible block
            match _find_win_move(board_view, current_side.swap_side()):
                case None:
                    avail_moves = [i for i, tile in enumerate(board_view) if tile is None]
                    return random.choice(avail_moves)
                case at: return at

        # if the AI decides to be a try hard, let it "minimax" you
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


def _find_win_move(board, side: Side) -> int | None:
    """
    Find a spot that leads to a win of a given side
    :param board: the board
    :param side: the given side
    :return: that winning move, or `None` if there is not
    """
    to_checks = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]  # Diagonals
    ]

    for to_check in to_checks:
        count = 0
        at = None
        for i in to_check:
            if board[i] is None:
                at = i
            elif board[i] is side:
                count += 1

        if count == 2 and at is not None:
            return at

    return None
