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


def convert_to_space_location(space_num: int) -> list:
    """Convert int to grid location"""
    grid_map = {
        1: [2, 0],
        2: [2, 1],
        3: [2, 2],
        4: [1, 0],
        5: [1, 1],
        6: [1, 2],
        7: [0, 0],
        8: [0, 1],
        9: [0, 2],
    }

    return grid_map[space_num]


def update_user_section(updated_info: list[str]) -> str:
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


if __name__ == "__main__":
    print(convert_to_space_location(1))
