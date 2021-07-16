# std libraries

# external libraries
from blessed import Terminal

# custom libraries
from library.board import Board
from library.game_state import GameState
from library.user_term import convert_to_space_location

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
            state.user_input = str(val.name)
        else:
            state.user_input = str(val)

        state.driver(term, board)

        if state.update_board:
            working_space_location = convert_to_space_location(state.user_select_space)
            if state.player_active == 1:
                board.collect_subgrid(str(state.user_select_subgrid - 1))[
                    working_space_location[0], working_space_location[1]
                ] = "X"
            elif state.player_active == 2:
                board.collect_subgrid(str(state.user_select_subgrid - 1))[
                    working_space_location[0], working_space_location[1]
                ] = "0"

            state.change_player()
            board.draw_board(term)

            state.update_board = False
            # TODO handle logic for next grid below is a placeholder *this may be good enough
            state.save_subgrid_bool = True

            if state.save_subgrid_bool:
                state.user_select_subgrid = state.user_select_space
                state.user_select_space = 0
                state.term_info[2] = (
                    f"Current: SubGrid {state.user_select_subgrid} "
                    f"| Space {state.user_select_space}"
                )
            else:
                state.user_select_subgrid = 0
            state.redraw_user_term(term)
