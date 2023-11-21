# Coding convention:
# - in the file or module except `main.py`, prefix everything (classes, fields, etc.)
# that you don't want others to see with `_` (underscore)

import input_valid
from game import Side, Game


def main():
    pass


if __name__ == "__main__":
    main()


def prompt_player_side() -> Side:
    def string_to_side(inp: str) -> Side:
        match inp:
            case Side.X.value | Side.X.value.lower():
                return Side.X
            case Side.O.value | Side.O.value.lower():
                return Side.O

        raise ValueError("Invalid side")

    return input_valid.input_till_correct(
        "Choose side (X/O): ",
        "Invalid side. Please enter the correct side (X/O): ",
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

    return input_valid.input_till_correct(
        "Will you go first (Y/N)? ",
        "Invalid input. Will you go first (Y/N)? ",
        y_n_to_bool
    )


def get_game() -> Game:
    import human, minimax_ai

    human_player = human.HumanPlayer()
    # TODO: choose difficulty also
    ai_player = minimax_ai.MinimaxAi(0.5)

    match prompt_player_side(), prompt_go_first():
        case Side.X, True:
            return Game(human_player, ai_player, Side.X)
        case Side.X, False:
            return Game(human_player, ai_player, Side.O)
        case Side.O, True:
            return Game(ai_player, human_player, Side.O)
        case Side.O, False:
            return Game(ai_player, human_player, Side.X)
