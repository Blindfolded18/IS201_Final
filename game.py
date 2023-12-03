# I don't want CLI implementation and Player's concrete implementations to be here
# They aren't responsibilities of this module
import copy
from enum import Enum
from abc import abstractmethod


class Side(Enum):
    """
    Side in the game. Either "X" or "O"
    """

    O = 'O'  # noqa: E741
    """
    O side
    """

    X = 'X'
    """
    X side
    """

    def swap_side(self):
        """
        Change to the opposite side
        :return:  the opposite side
        """
        return Side.X if self is Side.O else Side.O


class BoardView:
    """
    The immutable board view
    """

    def __init__(self, board: '_Board'):
        """
        Initialize a view from the actual board
        :param board: the board
        """
        self._board = board.tiles

    def __getitem__(self, index) -> Side | None:
        """
        Gets the tile at `index`
        :param index: desired position
        :return: tile
        """

        return self._board[index]

    def __iter__(self):
        """
        Iterator over the entry of the board.
        :return: iterator over the entry of the board
        """

        return iter(self._board)

    def __contains__(self, tile: Side | None) -> bool:
        """
        Checks if a tile is in the board
        :param tile: the tile
        :return: `True` if so, otherwise `False`
        """

        return tile in self._board


class Player:
    """
    Player of the game, which could be human or AI
    """

    @abstractmethod
    def decide_move(self, board_view: BoardView, current_side: Side) -> int:
        """
        Decide the next move
        :param board_view: the immutable view of the board to prevent direct modification on the board.
        You can index, iterate on, and perform membership test and comprehensions like a normal list
        :param current_side: the current side taking turn.
        :return: the "decision" on the position (0-8) where the next move will be placed
        """
        pass


class Outcome(Enum):
    """
    Game result reported by :meth:`Game.next_turn`.
    """

    O_WIN = -1
    """
    O side wins
    """

    X_WIN = 1
    """
    X side wins
    """

    DRAW = 0
    """
    A draw
    """


class Game:
    """
    The game
    """

    def __init__(self, p_x: Player, p_o: Player, start_side: Side):
        """
        Feeds the two players and the starting side to begin the game
        :param p_x: player of X side
        :param p_o: player of O side
        :param start_side: player's side playing first
        """

        self._board: _Board = _Board()
        """
        the game's board
        """

        self._p_x: Player = p_x
        """
        player playing for X side
        """

        self._p_o: Player = p_o
        """
        player playing for O side
        """

        self._turn: Side = start_side
        """
        the current side who will take the next turn
        """

    def next_turn(self) -> Outcome | None:
        """
        Proceeds the game. The player in current turn will be played only.
        It is advised that this method doesn't drive the game to the completion in one called.
        There's only one move at a time.
        NOTE: do NOT call this method if the game is concluded. That is, do NOT call if the previous call
        didn't return `None`
        :return: the outcome of the game after the move, either a win or a draw, or `None` if the game isn't concluded
        yet
        """

        # Helper function to prevent code duplication
        def make_turn(board: _Board, p: Player, side: Side) -> bool:
            move_at = p.decide_move(BoardView(board), side)
            board[move_at] = side

            return has_won(board, side)

        match self._turn:
            case Side.X:
                if make_turn(self._board, self._p_x, self._turn):
                    return Outcome.X_WIN

                self._turn = Side.O

            case Side.O:
                if make_turn(self._board, self._p_o, self._turn):
                    return Outcome.O_WIN

                self._turn = Side.X

        if self._board.is_full():
            return Outcome.DRAW

        # Cannot determine who wins or whether the game is a draw. Return `None`
        return None

    @property
    def board(self) -> BoardView:
        return BoardView(self._board)


def has_won(board, side: Side) -> bool:
    """
    check if the given side wins on this board.
    This can be used for AI implementation
    :param board: the board. It must be an array-like board with 9 `Side | None` elements (like `list[Side | None]`)
    :param side: side to check for the win
    :return: `True` if the given side has won, `False` otherwise
    """

    # All possible winning condition
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]  # Diagonals
    ]

    return any(
        all(board[i] is side for i in win_condition)
        for win_condition in win_conditions
    )


# Private. Other modules must NOT interact with this directly
class _Board:
    """
    The 3x3 board of the game. Methods required to be a collection is overloaded so this class can be treated
    as a collection
    """

    def __init__(self):
        """
        Initializes the empty board
        """

        self.tiles: list[Side | None] = [None] * 9
        """
        For each tile, it's either in one of the side, or `None` if empty
        """

    def __getitem__(self, index) -> Side | None:
        """
        Gets the tile at `index`
        :param index: desired position
        :return: tile
        """

        return self.tiles[index]

    def __setitem__(self, index, value: Side | None):
        """
        Sets the tile at `index`
        :param index: desired position
        :param value: new tile
        """

        self.tiles[index] = value

    def __iter__(self):
        """
        Iterator over the entry of the board.
        :return: iterator over the entry of the board
        """

        return iter(self.tiles)

    def __contains__(self, tile: Side | None) -> bool:
        """
        Checks if a tile is in the board
        :param tile: the tile
        :return: `True` if so, otherwise `False`
        """

        return tile in self.tiles

    def is_full(self) -> bool:
        """
        checks whether the board is full. That is, there's no empty tile on the board
        :return: `True` if so, `False` otherwise
        """

        return None not in self
