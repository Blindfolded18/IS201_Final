from unittest import TestCase

from game import Game, Side, _Board, Outcome, Player
from minimax_ai import MinimaxAi


class TestMinimaxAi(TestCase):

    def test_next_move_must_win(self):
        custom_board = [
            Side.O, Side.X, Side.O,
            Side.O, Side.X, Side.X,
            None, None, None
        ]
        the_game = _game_with_custom_board(MinimaxAi(), MinimaxAi(), Side.X, custom_board)
        # print(the_game._board._tiles)
        outcome = the_game.next_turn()
        self.assertIs(outcome, Outcome.X_WIN)

    def test_next_move_must_block(self):
        custom_board = [
            None, None, None,
            Side.X, Side.O, None,
            Side.X, None, None,
        ]
        the_game = _game_with_custom_board(MinimaxAi(), MinimaxAi(), Side.O, custom_board)
        # print(the_game._board._tiles)
        outcome = the_game.next_turn()
        self.assertIs(outcome, None)
        self.assertIs(the_game._board[0], Side.O)


def _game_with_custom_board(p_x: Player, p_o: Player, start_side: Side, tiles: list[Side | None]) -> Game:
    the_game = Game(p_x, p_o, start_side)
    board = _Board()
    board._tiles = tiles
    the_game._board = board
    return the_game
