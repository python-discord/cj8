import dataclasses
from textwrap import dedent


@dataclasses.dataclass()
class UserTermState:
    """Reset machine for next turn"""

    subgrid_select: bool = True
    space_select: bool = True

    user_confirm: bool = True
    start_of_turn: bool = True
    end_of_turn: bool = False

    user_select_subgrid: int = 0
    user_select_space: int = 0


def starting_user_section() -> str:
    """Starting Terminal"""
    output = dedent(
        """
        ┌─term────────────────────────────┐
        │                                 │
        │      shall we play a game?      │
        │             (y/n?)              │
        │                                 │
        └(Enter to confirm)───('q' to esc)┘
    """
    ).strip()

    return output


def update_user_section(infoToBeAdded: list[str]) -> list[str]:
    """To add your information to the terminal you have 3 lines with 31 spaces"""
    output: list[str] = []

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
