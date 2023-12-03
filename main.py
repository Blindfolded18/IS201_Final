# Coding convention:
# - in the file or module except `main.py`, prefix everything (classes, fields, etc.)
# that you don't want others to see with `_` (underscore)

# 1. Selection of the first player. (e.g. Would you like to play first?)
# 2. Assignment of "O" or "X" for a user. (e.g. Please choose 'O' or 'X' for your turn.)
# 3. Computer selects a position based on either random position.
# 4. If computer can select a position based on an algorithm (e.g. MiniMax algorithm or rule-based) approach, you will
# earn 20 extra points.
# 5. At each run, the program should display the board (3x3) as shown below. Placement is made based on the pre-assigned
# positional number.
# 6. Your program prints appropriate message if there is a winner and then exits.
# 7. Your program saves all the moves between players in a file called tictactoe.txt (X:5 O:2 X:1 O:9 etc...)
# 8. Your program should handle incorrect inputs (e.g. input validation) and continue to play without an error.

from human import display_board
from input_valid import input_till_correct
from game import Side, Game, Outcome
from typing import TextIO


def main():
    with open(file="tictactoe.txt", mode="w") as file:
        the_game, player_side = get_game(file)
        print()

        while (outcome := the_game.next_turn()) is None:
            print()

        print()
        display_board(the_game.board)
        print()

        match outcome, player_side:
            case (Outcome.X_WIN, Side.X) | (Outcome.O_WIN, Side.O):
                print("You win!")
            case Outcome.DRAW, _:
                print("The game ends with a draw!")
            case _:
                print("You lose. Good luck next time!")

        print("Thanks for playing our game!")


def prompt_player_side() -> Side:
    def string_to_side(inp: str) -> Side:
        if inp == Side.X.value or inp == Side.X.value.lower():
            return Side.X

        if inp == Side.O.value or inp == Side.O.value.lower():
            return Side.O

        raise ValueError("Invalid side")

    return input_till_correct(
        "Choose your side (X/O): ",
        "Please enter the valid side (X/O): ",
        string_to_side
    )


def prompt_go_first() -> bool:
    def y_n_to_bool(inp: str) -> bool:
        match inp:
            case "Y" | "y":
                return True
            case "N" | "n":
                return False

        raise ValueError("Invalid Y/N input")

    return input_till_correct(
        "Will you go first (Y/N)? ",
        "Will you go first (Y/N)? ",
        y_n_to_bool
    )


def prompt_difficulty() -> tuple[float, float]:
    def str_to_difficulty(inp: str) -> tuple[float, float]:
        match inp:
            case "1":
                return 0.0, 0.0
            case "2":
                return 0.2, 0.2
            case "3":
                return 0.4, 0.3
            case "4":
                return 0.6, 0.5
            case "5":
                return 1.0, 1.0

        raise ValueError("Invalid difficulty")

    from textwrap import dedent

    return input_till_correct(
        dedent("""\
            1. Braindead
            2. Easy
            3. Medium
            4. Hard
            5. Impossible
            Choose your difficulty (1-5): """),
        "Please choose again (1-5): ",
        str_to_difficulty
    )


def get_game(file: TextIO) -> tuple[Game, Side]:
    from human import HumanPlayer
    from minimax_ai import MinimaxAi
    from file_log import FilePlayerLogger

    human_player = FilePlayerLogger(player=HumanPlayer(), file=file)

    think_chance = prompt_difficulty()
    print()
    ai_player = FilePlayerLogger(player=MinimaxAi(think_chance), file=file)

    player_side = prompt_player_side()
    print()
    player_goes_first = prompt_go_first()

    game: Game
    match player_side, player_goes_first:
        case Side.X, True:
            game = Game(human_player, ai_player, Side.X)
        case Side.X, False:
            game = Game(human_player, ai_player, Side.O)
        case Side.O, True:
            game = Game(ai_player, human_player, Side.O)
        case Side.O, False:
            game = Game(ai_player, human_player, Side.X)
        case _:
            raise AssertionError("unreachable")

    return game, player_side


if __name__ == "__main__":
    main()
