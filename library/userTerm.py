import dataclasses


@dataclasses.dataclass()
class UserTermState:
    """Reset machine for next turn"""

    subgrid_select_bool: bool = True
    space_select_bool: bool = True

    user_confirm_bool: bool = True
    start_of_turn: bool = True
    end_of_turn: bool = False

    user_select_subgrid: int = 0
    user_select_space: int = 0


def starting_user_section() -> list:
    """Starting Terminal"""
    output = []
    output += "┌─term────────────────────────────┐"
    output += "\n│                                 │"
    output += "\n│      shall we play a game?      │"
    output += "\n│             (y/n?)              │"
    output += "\n│                                 │"
    output += "\n└(Enter to confirm)───('q' to esc)┘"

    return output


def update_user_section(infoToBeAdded: list) -> list:
    """To add your information to the terminal you have 3 lines with 31 spaces"""
    output = []

    for i in infoToBeAdded:
        if len(i) > 31:
            raise NameError("Terminal contents too big")

    # theres a better way to do this im just too dumb to think of it atm
    if len(infoToBeAdded) == 1:
        infoToBeAdded += " "
        infoToBeAdded += " "
        infoToBeAdded += " "
    elif len(infoToBeAdded) == 2:
        infoToBeAdded += " "
        infoToBeAdded += " "
    elif len(infoToBeAdded) == 3:
        infoToBeAdded += " "

    output += "┌─term────────────────────────────┐"
    output += "\n│ " + "".join(infoToBeAdded[0]).ljust(31) + " │"
    output += "\n│ " + "".join(infoToBeAdded[1]).ljust(31) + " │"
    output += "\n│ " + "".join(infoToBeAdded[2]).ljust(31) + " │"
    output += "\n│ " + "".join(infoToBeAdded[3]).ljust(31) + " │"
    output += "\n└(Enter to confirm)───('q' to esc)┘"

    return output
