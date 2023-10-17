from unittest import TestCase

from game import Player, Side, Game, Outcome
import dataclasses


class TestGame(TestCase):
    def test_next_turn(self):
        @dataclasses.dataclass
        class TestPlayer(Player):
            """
            This player will start the move from the `current` position, and the position is incremented for each move
            """
            current: int

            def decide_move(self, board_view: list[bool | None]) -> int:
                move = self.current
                self.current += 1
                return move

        g = Game(TestPlayer(0), TestPlayer(3), Side.X)
        for i in range(0, 4):
            self.assertIs(g.next_turn(), None)

        # After the loop, the board should look like this, and the current turn is belonged to the "X" side
        # |X|X| |
        # |O|O| |
        # | | | |

        self.assertIs(g.next_turn(), Outcome.X_WIN)

        # And then "X" wins
        # |X|X|X|
        # |O|O| |
        # | | | |
