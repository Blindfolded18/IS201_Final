# Coding convention:
# - in the file or module except `main.py`, prefix everything (classes, fields, etc.)
# that you don't want others to see with `_` (underscore)
import dataclasses

from game import Game, Side, Player


@dataclasses.dataclass
class TestPlayer(Player):
    current: int

    def decide_move(self, board_view: list[bool | None]) -> int:
        move = self.current
        self.current += 1
        return move


def main():
    g = Game(TestPlayer(0), TestPlayer(3), Side.X)

    g.next_turn()

    g.next_turn()

    outcome = g.next_turn()
    print(outcome)

    g.next_turn()

    outcome = g.next_turn()
    print(outcome)


if __name__ == "__main__":
    main()
