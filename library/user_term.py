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


def update_user_section(infoToBeAdded: list[str]) -> str:
    """To add your information to the terminal you have 3 lines with 31 spaces"""
    for i in infoToBeAdded:
        if len(i) > 31:
            raise NameError("Terminal contents too big")

    # Ensure we always have enough rows written out to overwrite the last frame
    spacing_rows = 4 - len(infoToBeAdded)
    infoToBeAdded.extend([""] * spacing_rows)

    output = "\n".join(
        [
            "┌─term────────────────────────────┐",
            *("│ " + "".join(i).ljust(31) + " │" for i in infoToBeAdded),
            "└(Enter to confirm)───('q' to esc)┘",
        ]
    )

    return output
