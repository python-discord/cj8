import typing

import blessed
import numpy as np
import numpy.typing as npt


class Board:
    """Represents the board that the game of tic-tac-toe is played on."""

    contents: npt.NDArray[np.str_]
    player1_turn: bool
    game_over: bool
    turn_one: bool

    def __init__(self) -> None:
        self.contents = np.full((9, 9), "·")
        self.player1_turn = True
        self.game_over = False
        self.turn_one = True

    def collect_subgrid(self, number: str) -> npt.NDArray[np.str_]:
        """
        Takes a subgrid choice and returns that np.ndarray and the choice str

        The subgrids are laid out as so:
            7 8 9
            4 5 6
            1 2 3
        """
        first = slice(3)
        second = slice(3, 6)
        third = slice(6, 9)
        subgrid_map = {
            "1": (third, first),
            "2": (third, second),
            "3": (third, third),
            "4": (second, first),
            "5": (second, second),
            "6": (second, third),
            "7": (first, first),
            "8": (first, second),
            "9": (first, third),
        }

        return self.contents[subgrid_map[number]]

    def draw_board(self, term: blessed.Terminal) -> None:
        """Rudimentary attempt to draw a game board."""
        nonant_size = 11
        verticals = (
            f"{term.bold}{term.green}{' '*nonant_size}┃{' '*nonant_size}┃{term.normal}"
        )
        crosses = (
            f"{term.bold}{term.green}━━━━━━━━━━━╋━━━━━━━━━━━╋━━━━━━━━━━━{term.normal}"
        )
        # clear the screen
        print(term.clear)
        # print the game board
        for i in range(17):
            if i == 5 or i == 11:
                print(crosses)
            else:
                print(verticals)
        print()
        for i in range(1, 10):
            subgrid = self.collect_subgrid(str(i))
            self.redraw_subgrid(term, subgrid, str(i), term.green)

    def redraw_gamestate(
        self,
        term: blessed.Terminal,
        subgrid: npt.NDArray[np.str_],
        start_coords: typing.Tuple[int, int],
    ) -> None:
        """Takes a subgrid numpy array and draws the current state of the game on that board"""
        x, y = start_coords
        x += 1
        # initial_position
        for row in subgrid:
            for entry in row:
                print(term.move_xy(x, y) + f"{entry}")
                x += 4
                if x > start_coords[0] + 12:
                    y += 2
                    x = start_coords[0] + 1

    def redraw_gridlines(
        self,
        term: blessed.Terminal,
        start_coords: typing.Tuple[int, int],
        color: str,
    ) -> None:
        """Takes a subgrid numpy array and draws the current state of the game on that board"""
        x, y = start_coords
        verticals = (
            f"   {term.dim}{color}│{term.normal}   {term.dim}{color}│{term.normal}"
        )
        crosses = f"{term.dim}{color}───┼───┼───{term.normal}"
        print(term.move_xy(x, y) + verticals)
        for i in range(1, 5):
            if i % 2 == 0:
                print(term.move_x(x) + verticals)

            else:
                print(term.move_x(x) + crosses)

    def redraw_subgrid(
        self,
        term: blessed.Terminal,
        subgrid: npt.NDArray[np.str_],
        number: str,
        color: str,
    ) -> None:
        """Takes the subgrid number 1-9 and redraws that grid based on the subgrid"""
        # Set Start Coordinates based on subgrid number
        start_coords = {
            "1": (0, 13),
            "2": (12, 13),
            "3": (24, 13),
            "4": (0, 7),
            "5": (12, 7),
            "6": (24, 7),
            "7": (0, 1),
            "8": (12, 1),
            "9": (24, 1),
        }
        self.redraw_gridlines(term, start_coords[number], color)
        self.redraw_gamestate(term, subgrid, start_coords[number])
