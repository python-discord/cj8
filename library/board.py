import typing

import blessed
import numpy as np


class Board:
    """Represents the board that the game of tic-tac-toe is played on."""

    contents: np.array = np.full((9, 9), ".")  # type: ignore
    player1_turn: bool
    game_over: bool

    def __init__(self) -> None:
        self.contents = np.full((9, 9), ".")
        self.player1_turn = True
        self.game_over = False
        self.turn_one = True

    # def select_subgrid(
    #     self, number: typing.Literal[0, 1, 2, 3, 4, 5, 6, 7, 8]
    # ) -> np.array:
    #     """Choose subgrid game to play."""
    #     pass

    def draw_board(self, term: blessed.Terminal) -> None:
        """Rudimentary attempt to draw a game board."""
        # clear the screen
        print(term.clear)
        # print the game board
        print(
            " "
            + f" {term.bold}{term.green}┃{term.normal} ".join(
                f". {term.dim}{term.green}│{term.normal} . {term.dim}{term.green}│{term.normal} ."
                for _ in range(3)
            )
        )
        print(
            f"{term.green}"
            + f"{term.bold}┃{term.normal}{term.green}".join(
                "┼".join("─" * 3 for _ in range(3)) for _ in range(3)
            )
            + term.normal
        )
        print(
            " "
            + f" {term.bold}{term.green}┃{term.normal} ".join(
                f". {term.dim}{term.green}│{term.normal} . {term.dim}{term.green}│{term.normal} ."
                for _ in range(3)
            )
        )
        print(
            f"{term.green}"
            + f"{term.bold}┃{term.normal}{term.green}".join(
                "┼".join("─" * 3 for _ in range(3)) for _ in range(3)
            )
            + term.normal
        )
        print(
            " "
            + f" {term.bold}{term.green}┃{term.normal} ".join(
                f". {term.dim}{term.green}│{term.normal} . {term.dim}{term.green}│{term.normal} ."
                for _ in range(3)
            )
        )
        print(
            f"{term.bold}{term.green}"
            + "╋".join("━" * 11 for _ in range(3))
            + term.normal
        )
        print(
            " "
            + f" {term.bold}{term.green}┃{term.normal} ".join(
                f". {term.dim}{term.green}│{term.normal} . {term.dim}{term.green}│{term.normal} ."
                for _ in range(3)
            )
        )
        print(
            f"{term.green}"
            + f"{term.bold}┃{term.normal}{term.green}".join(
                "┼".join("─" * 3 for _ in range(3)) for _ in range(3)
            )
            + term.normal
        )
        print(
            " "
            + f" {term.bold}{term.green}┃{term.normal} ".join(
                f". {term.dim}{term.green}│{term.normal} . {term.dim}{term.green}│{term.normal} ."
                for _ in range(3)
            )
        )
        print(
            f"{term.green}"
            + f"{term.bold}┃{term.normal}{term.green}".join(
                "┼".join("─" * 3 for _ in range(3)) for _ in range(3)
            )
            + term.normal
        )
        print(
            " "
            + f" {term.bold}{term.green}┃{term.normal} ".join(
                f". {term.dim}{term.green}│{term.normal} . {term.dim}{term.green}│{term.normal} ."
                for _ in range(3)
            )
        )
        print(
            f"{term.bold}{term.green}"
            + "╋".join("━" * 11 for _ in range(3))
            + term.normal
        )
        print(
            " "
            + f" {term.bold}{term.green}┃{term.normal} ".join(
                f". {term.dim}{term.green}│{term.normal} . {term.dim}{term.green}│{term.normal} ."
                for _ in range(3)
            )
        )
        print(
            f"{term.green}"
            + f"{term.bold}┃{term.normal}{term.green}".join(
                "┼".join("─" * 3 for _ in range(3)) for _ in range(3)
            )
            + term.normal
        )
        print(
            " "
            + f" {term.bold}{term.green}┃{term.normal} ".join(
                f". {term.dim}{term.green}│{term.normal} . {term.dim}{term.green}│{term.normal} ."
                for _ in range(3)
            )
        )
        print(
            f"{term.green}"
            + f"{term.bold}┃{term.normal}{term.green}".join(
                "┼".join("─" * 3 for _ in range(3)) for _ in range(3)
            )
            + term.normal
        )
        print(
            " "
            + f" {term.bold}{term.green}┃{term.normal} ".join(
                f". {term.dim}{term.green}│{term.normal} . {term.dim}{term.green}│{term.normal} ."
                for _ in range(3)
            )
        )
        print()

    def redraw_gamestate(
        self,
        term: blessed.Terminal,
        subgrid: typing.Any,
        start_coords: typing.Tuple[int, int],
    ) -> None:
        """Takes a subgrid numpy array and draws the current state of the game on that board"""
        x, y = start_coords
        x += 1
        for row in subgrid:
            for entry in row:
                print(term.move_xy(x, y) + f"{entry}")
                x += 4
                if x > start_coords[0] + 12:
                    y += 2
                    x = start_coords[0] + 1

    def redraw_subgrid(
        self, term: blessed.Terminal, subgrid: typing.Any, number: str
    ) -> None:
        """Takes the subgrid number range(0,9) and redraws that grid based on the subgrid"""
        # Set Start Coordinates based on subgrid number
        start_coords = {
            "0": (0, 13),
            "1": (12, 13),
            "2": (24, 13),
            "3": (0, 7),
            "4": (12, 7),
            "5": (24, 7),
            "6": (0, 1),
            "7": (12, 1),
            "8": (24, 1),
        }
        self.redraw_gamestate(term, subgrid, start_coords[number])
        # Can also write functions to redraw grid
