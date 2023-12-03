import dataclasses
from typing import TextIO

from game import Player, BoardView, Side


@dataclasses.dataclass(frozen=True)
class FilePlayerLogger(Player):
    """
    A decorator that will log the move of the wrapped player
    """

    player: Player
    """
    Player to be logged
    """

    file: TextIO
    """
    Destination file
    """

    def decide_move(self, board_view: BoardView, current_side: Side) -> int:
        move = self.player.decide_move(board_view, current_side)
        self.file.write(f"{current_side.value}: {move + 1}\n")
        self.file.flush()
        return move
