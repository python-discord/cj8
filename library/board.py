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

    # def select_subgrid(
    #     self, number: typing.Literal[0, 1, 2, 3, 4, 5, 6, 7, 8]
    # ) -> np.array:
    #     """Choose subgrid game to play."""
    #     pass

    def draw_board(self, term: blessed.Terminal) -> None:
        """Rudimentary attempt to draw a game board."""
        verticals = f"           {term.bold}{term.green}┃{term.normal}           {term.bold}{term.green}┃{term.normal}"
        crosses = (
            f"{term.bold}{term.green}━━━━━━━━━━━╋━━━━━━━━━━━╋━━━━━━━━━━━{term.normal}"
        )
        # clear the screen
        print(term.clear)
        # print the game board
        print(verticals)
        print(verticals)
        print(verticals)
        print(verticals)
        print(verticals)
        print(crosses)
        print(verticals)
        print(verticals)
        print(verticals)
        print(verticals)
        print(verticals)
        print(crosses)
        print(verticals)
        print(verticals)
        print(verticals)
        print(verticals)
        print(verticals)
        print()

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
    ) -> None:
        """Takes a subgrid numpy array and draws the current state of the game on that board"""
        x, y = start_coords
        term.move_xy(x, y)
        verticals = f"   {term.dim}{term.green}│{term.normal}   │{term.normal}"
        crosses = f"{term.dim}{term.green}───┼───┼───{term.normal}"
        for i in range(5):
            if i % 2 == 0:
                print(term.move_down + verticals)

            else:
                print(term.move_xy(x, y) + crosses)

    def redraw_subgrid(
        self, term: blessed.Terminal, subgrid: npt.NDArray[np.str_], number: str
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
