from blessed import Terminal

from library import Board

term = Terminal()
board = Board()

# python 3.10 feature, but it works in python 3.9
with (term.fullscreen(), term.cbreak()):
    print(term.on_grey(board.display(term)), end="")

    while (val := term.inkey()) != "q":
        if val in ("1", "2", "3", "4", "5", "6", "7", "8", "9"):
            # map the numpad to array indexes
            # fmt: off
            value = [
                "7", "8", "9",
                "4", "5", "6",
                "1", "2", "3",
            ].index(val)
            # fmt: on
            board.handle_input(value)

        print(term.clear() + term.on_grey(board.display(term)), end="")
