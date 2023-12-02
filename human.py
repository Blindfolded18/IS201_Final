from game import Player, BoardView, Side
from input_valid import input_till_correct


class HumanPlayer(Player):
    """
    Player that uses user input as the move
    """

    def decide_move(self, board_view: BoardView, current_side: Side) -> int:
        display_board(board_view)
        return _prompt_move(board_view, current_side)


def display_board(board) -> None:
    """
    Print the board.

    This is intended to be a public API, used to print the board in the final stage
    :param board: the board
    """

    print('    Board          Indices')
    print('-------------   -------------')
    for i in range(3):
        for pos in range(i * 3, i * 3 + 3):
            print(f"| {' ' if board[pos] is None else board[pos].value} ", end='')

        print("|   ", end='')
        for pos in range(i * 3 + 1, i * 3 + 4):
            print(f"| {pos} ", end='')

        print('|\n-------------   -------------')


def _prompt_move(board_view, current_side: Side) -> int:
    def string_to_move(inp: str) -> int:
        move: int
        try:
            move = int(inp)
        except ValueError:
            raise ValueError("Expected a number, got a string")

        if 1 <= move <= 9 and board_view[move - 1] is None:
            return move - 1

        raise ValueError("Invalid move")

    return input_till_correct(
        f"Your side: {current_side.value}. Enter your move (1-9): ",
        f"Your side: {current_side.value}. Enter your move again (1-9): ",
        string_to_move
    )


if __name__ == '__main__':
    display_board([
        None, None, None,
        Side.X, None, None,
        None, None, None,
    ])
