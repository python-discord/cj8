# std libraries

# external libraries
from blessed import Terminal

# custom libraries
from library.board import Board
from library.game_state import GameState

term = Terminal()
board = Board()

with term.fullscreen(), term.cbreak(), term.hidden_cursor():
    board.draw_board(term)

    # origin of user term
    print(term.move_xy(0, 24))

    state = GameState(term)

    val = ""

    while (val := term.inkey()) != "q":

        if val.is_sequence:
            state.user_input = val.name
        else:
            state.user_input = val

        state.driver(term)
