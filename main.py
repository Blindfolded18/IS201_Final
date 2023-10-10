# Coding convention:
# - in the file or module except `main.py`, prefix everything (classes, fields, etc.)
# that you don't want others to see with `_` (underscore)

from game import Game, Side


def main():
    g = Game(None, None, Side.X)
    print(g.next_turn())


if __name__ == "__main__":
    main()
