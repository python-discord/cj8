import blessed


def update_user_section(term: blessed.Terminal, updated_info: list[str]) -> list[str]:
    """To add your information to the terminal you have 3 lines with 31 spaces"""
    for i in updated_info:
        if len(i) > 31:
            raise NameError("Terminal contents too big")

    print(term.move_xy(0, 18))

    # theres a better way to do this im just too dumb to think of it atm
    if len(updated_info) == 1:
        updated_info += " "
        updated_info += " "
        updated_info += " "
    elif len(updated_info) == 2:
        updated_info += " "
        updated_info += " "
    elif len(updated_info) == 3:
        updated_info += " "

    item: list = [""] * 6
    item[0] = "┌─term────────────────────────────┐"
    item += "\n│ " + "".join(updated_info[0]).ljust(31) + " │"
    item += "\n│ " + "".join(updated_info[1]).ljust(31) + " │"
    item += "\n│ " + "".join(updated_info[2]).ljust(31) + " │"
    item += "\n│ " + "".join(updated_info[3]).ljust(31) + " │"
    item += "\n└(Enter to confirm)───('q' to esc)┘"

    print("".join(item))


class GameState:
    """Main code for managing the game state"""

    current: int
    next: int
    good_move: bool

    save_subgrid_bool: bool
    player_active: int
    term_info: list

    user_select_subgrid: int
    subgrid_saved: int
    user_select_space: int
    user_input: str

    def __init__(self, term: blessed.Terminal):
        self.current: int = 0
        self.good_move = False
        self.save_subgrid_bool: bool = False
        self.player_active: int = 0
        self.term_info: list = [""] * 3
        self.user_select_subgrid: int = 0
        self.user_select_space: int = 0
        self.user_input: str = ""

        self.term_info[1] = "shall we play a game?"
        self.term_info[2] = "(y/n?)"
        self.redraw_user_term(term)
        self.next: int = 10

    def driver(self, term: blessed.Terminal) -> None:
        """Main State Machine"""
        if self.next == 10:
            self.wait_for_ready(term)
        elif self.next == 20:
            self.update_subgrid_select(term)
        elif self.next == 30:
            self.update_space_select(term)
        elif self.next == 40:
            self.end_of_turn(term)
        else:
            pass

    def redraw_user_term(self, term: blessed.Terminal) -> None:
        """Redraws User Term"""
        print(term.move_up(7))
        print(update_user_section(term, self.term_info))

    def wait_for_ready(self, term: blessed.Terminal) -> None:
        """Wait for the player to start turn"""
        self.current = 10
        self.player_active = 1 if self.player_active == 2 else 2

        if self.user_input == "y":
            self.term_info[0] = f"Player {self.player_active} Active"

            if self.save_subgrid_bool:
                self.next = 30  # skip to space select
                self.term_info[1] = "Select Space by entering 1-9"
            else:
                self.next = 20  # go to subgrid select
                self.term_info[1] = "Select SubGrid by entering 1-9"

            self.term_info[2] = ""
            self.redraw_user_term(term)

        else:
            self.next = 10

        self.redraw_user_term(term)

    def update_subgrid_select(self, term: blessed.Terminal) -> None:
        """Update the user selected subgrid"""
        self.current = 20

        if self.user_input in ("1", "2", "3", "4", "5", "6", "7", "8", "9"):
            self.user_select_subgrid = int(self.user_input)
            self.term_info[2] = (
                f"Current: SubGrid {self.user_select_subgrid} "
                f"| Space {self.user_select_space}"
            )
        elif self.user_input == "KEY_ENTER":
            self.term_info[1] = "Select Space by entering 1-9"
            self.confirm_entry(term)
            self.next = 30

        self.redraw_user_term(term)

    def update_space_select(self, term: blessed.Terminal) -> None:
        """Update the user selected space"""
        self.current = 30

        if self.user_input in ("1", "2", "3", "4", "5", "6", "7", "8", "9"):
            self.user_select_space = int(self.user_input)
            self.term_info[2] = (
                f"Current: SubGrid {self.user_select_subgrid} "
                f"| Space {self.user_select_space}"
            )
        elif self.user_input == "KEY_ENTER":
            self.confirm_entry(term)
            if self.confirm_good_move():
                self.next = 40  # go to exectue move
            else:
                self.next = 50  # go to error handling and reset values

        self.redraw_user_term(term)

    def confirm_entry(self, term: blessed.Terminal) -> None:
        """Confirm user pressed enter"""
        if self.user_select_subgrid != 0:
            self.term_info[1] = "Select Space by entering 1-9"
        elif self.user_select_space != 0:
            self.term_info[1] = "Confirm Selection?"
        else:
            # show confirmation
            self.term_info[0] = " "
            self.term_info[1] = f"Player{self.player_active} selected:"
            self.term_info[2] = (
                f"Current: SubGrid {self.user_select_subgrid} "
                f"| Space {self.user_select_space}"
            )

        self.redraw_user_term(term)

    def end_of_turn(self, term: blessed.Terminal) -> None:
        """End of Turn"""
        self.current = 40

        # update board

        # reset state
        # TODO check if subgrid needs to be reset
        _saved_space_selection = self.user_select_space

        term_info = [""] * 3
        term_info[0] = f"Player {self.player_active} Active"
        term_info[1] = "Ready? press y"
        self.redraw_user_term(term)

        self.__init__

        # TODO handle logic for next grid below is a placeholder *this may be good enough
        self.user_select_subgrid = _saved_space_selection

    def confirm_good_move(self) -> bool:
        """Handle the entry of a bad move"""
        self.good_move = False

        return self.good_move
