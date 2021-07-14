import dataclasses


@dataclasses.dataclass()
class UserTermState:
    """Reset machine for next turn"""

    subgrid_select_bool: bool = True
    space_select_bool: bool = True

    wait_for_ready: bool = True
    user_confirm_bool: bool = True
    start_of_turn: bool = True
    end_of_turn: bool = False
    save_subgrid: bool = True

    user_select_subgrid: int = 0
    user_select_space: int = 0


def starting_user_section() -> str:
    """Starting Terminal"""
    item: list[str] = []
    item.append("┌─term────────────────────────────┐")
    item.append("\n│                                 │")
    item.append("\n│      shall we play a game?      │")
    item.append("\n│             (y/n?)              │")
    item.append("\n│                                 │")
    item.append("\n└(Enter to confirm)───('q' to esc)┘")

    output = "".join(update_user_section(item))

    return output


def update_user_section(updated_info: list[str]) -> list[str]:
    """To add your information to the terminal you have 3 lines with 31 spaces"""
    item: list[str] = []

    for i in updated_info:
        if len(i) > 31:
            raise NameError("Terminal contents too big")

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

    item += "┌─term────────────────────────────┐"
    item += "\n│ " + "".join(updated_info[0]).ljust(31) + " │"
    item += "\n│ " + "".join(updated_info[1]).ljust(31) + " │"
    item += "\n│ " + "".join(updated_info[2]).ljust(31) + " │"
    item += "\n│ " + "".join(updated_info[3]).ljust(31) + " │"
    item += "\n└(Enter to confirm)───('q' to esc)┘"

    output = "".join(update_user_section(item))

    return output
