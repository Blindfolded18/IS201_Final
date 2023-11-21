from game import Player, BoardView, Side


class HumanPlayer(Player):
    """
    Player that uses user input as the move
    """

    def decide_move(self, board_view: BoardView, current_side: Side) -> int:
        # TODO: display the board, then prompt the move
        pass


def _display_board(board) -> None:
    """
    Print the board
    :param board: the board
    """

    print('-------------')
    for i in range(9):
        print(f'| {i + 1 if board[i] is None else board[i].value} ', end='')
        # we reach the end of the row
        if i % 3 >= 2:
            print('|\n-------------')


if __name__ == '__main__':
    _display_board([
        None, None, None,
        Side.X, None, None,
        None, None, None,
    ])
