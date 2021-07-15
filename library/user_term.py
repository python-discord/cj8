import blessed


def convert_to_space_location(space_num: int) -> list[int]:
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


def update_user_section(term: blessed.Terminal, updated_info: list[str]) -> None:
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

    item: list[str] = [""] * 6
    item[0] = "┌─term────────────────────────────┐"
    item += "\n│ " + "".join(updated_info[0]).ljust(31) + " │"
    item += "\n│ " + "".join(updated_info[1]).ljust(31) + " │"
    item += "\n│ " + "".join(updated_info[2]).ljust(31) + " │"
    item += "\n│ " + "".join(updated_info[3]).ljust(31) + " │"
    item += "\n└(Enter to confirm)───('q' to esc)┘"

    print("".join(item))
