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
    """To add your information to the terminal you have 4 lines with 31 spaces"""
    print(term.move_xy(0, 18))

    updated_info += [" "] * (4 - len(updated_info))

    item = "\n".join(
        [
            f"┌─{term.blue}term{term.normal}────────────────────────────┐",
            *("│ " + "".join(i).ljust(31) + " │" for i in updated_info),
            f"└{term.green}(Enter to confirm){term.normal}───{term.red}('q' to esc){term.normal}┘",
        ]
    )

    print("".join(item))
