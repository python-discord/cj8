# std libraries
import time

# external libraries
from blessed import Terminal

# custom libraries
from library.board import Board
from library.userTerm import UserTermState, starting_user_section, update_user_section

term = Terminal()
board = Board()

with term.fullscreen(), term.cbreak(), term.hidden_cursor():
    board.draw_board(term)

    # origin of user term
    print(term.move_xy(0, 18))

    # State
    state = UserTermState()
    player_active = 1
    wait_for_ready = True

    val = ""
    term_info = [""] * 3

    user_section = starting_user_section()
    print("".join(user_section))

    while (val := term.inkey()) != "q":
        with term.location():

            if wait_for_ready:
                if val == "y":
                    wait_for_ready = False
                else:
                    continue

            if state.start_of_turn:
                # reset player terminal
                term_info = [""] * 3
                term_info[0] = f"Player {player_active} Active"
                state.start_of_turn = False

            if state.subgrid_select_bool:
                term_info[1] = "Select SubGrid by entering 1-9"
                if val in ("1", "2", "3", "4", "5", "6", "7", "8", "9"):
                    state.user_select_subgrid = int(val)
                    term_info[
                        2
                    ] = f"Current: SubGrid {state.user_select_subgrid} | Space {state.user_select_space}"

                print(term.move_up(7))
                user_section = update_user_section(term_info)
                print("".join(user_section))

            elif state.space_select_bool:
                term_info[1] = "Select Space by entering 1-9"
                if val in ("1", "2", "3", "4", "5", "6", "7", "8", "9"):
                    state.user_select_space = int(val)
                    term_info[
                        2
                    ] = f"Current: SubGrid {state.user_select_subgrid} | Space {state.user_select_space}"

                print(term.move_up(7))
                user_section = update_user_section(term_info)
                print("".join(user_section))

            if val.is_sequence and val.name == "KEY_ENTER":
                if state.subgrid_select_bool and state.user_select_subgrid != 0:
                    state.subgrid_select_bool = False
                    term_info[1] = "Select Space by entering 1-9"
                elif state.space_select_bool and state.user_select_space != 0:
                    state.space_select_bool = False
                    term_info[1] = "Confirm Selection?"
                elif (
                    state.user_confirm_bool
                    and state.user_select_subgrid != 0
                    and state.user_select_space != 0
                ):
                    state.user_confirm_bool = False
                    # execute game logic here
                    # update_arrays()
                    #

                    # update the game board here

                    # show confirmation
                    term_info[0] = " "
                    term_info[1] = f"Player{player_active} selected:"
                    term_info[
                        2
                    ] = f"SubGrid {state.user_select_subgrid} | Space {state.user_select_space}"

                    # confirm end of turn
                    state.end_of_turn = True

                print(term.move_up(7))
                user_section = update_user_section(term_info)
                print("".join(user_section))

            if state.end_of_turn:
                # delay for user to read confirmation
                time.sleep(1)

                # reset state
                state = UserTermState()
                if player_active == 1:
                    player_active = 2
                elif player_active == 2:
                    player_active = 1

                term_info = [""] * 3
                term_info[0] = f"Player {player_active} Active"
                term_info[1] = "Ready? press y"

                print(term.move_up(7))
                user_section = update_user_section(term_info)
                print("".join(user_section))

                wait_for_ready = True

    print(term.clear)
