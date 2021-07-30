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

    def check_board_victory(self) -> typing.Optional[str]:
        """
        Determine if the entire board has been won, and by who.

        This function creates a 3 x 3 array with the current winner of each subgrid.
        The 3 x 3 is arranged like this:

        7 8 9
        4 5 6
        1 2 3
        """
        grid_states = np.full((3, 3), "·")
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
        for i in range(1, 10):
            y, x = grid_map[i]
            grid_states[y, x] = self.check_subboard_victory(str(i))

        return self.check_grid_victory(grid_states)

    def check_subboard_victory(self, number: str) -> typing.Optional[str]:
        """Determine if a given subgrid by number has been won, and by who."""
        subgrid = self.collect_subgrid(number)
        return self.check_grid_victory(subgrid)

    @staticmethod
    def check_grid_victory(grid: npt.NDArray[np.str_]) -> typing.Optional[str]:
        """Determine if a given 3x3 grid has been won, and by who."""
        for player in ("X", "O"):
            # this turns our grid of ["X", "O", "•"] into [True, False, False] by applying the condition to every spot
            ticks = grid == player
            # Summing over True treats True as 1, False as 0. 3 Trues = 3, so "won" rows are 3.
            # Because this is a 3x3 board, this results in a list of 3 True/False
            # indicating whether each row was won by this player
            horizontals = ticks.sum(axis=0) == 3
            if horizontals.any():
                return player
            verticals = ticks.sum(axis=1) == 3
            if verticals.any():
                return player

            # .diagonal() gets us a single diagonal list,
            # so these two rows are just True/False whether a diagonal is won
            diagonal_r = ticks.diagonal().sum() == 3
            diagonal_l = np.fliplr(ticks).diagonal().sum() == 3  # type: ignore [no-untyped-call]
            if diagonal_l or diagonal_r:
                return player

        return None

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

        # At the moment, numpy.array's __getitem__ is typed as returning a `typing.Any`:
        # https://github.com/numpy/numpy/blob/89c80ba606f4346f8df2a31cfcc0e967045a68ed/numpy/__init__.pyi#L1202-L1203
        return self.contents[subgrid_map[number]]  # type: ignore [no-any-return]

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
            self.redraw_subgrid(term, subgrid, str(i), term.green, None)

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
                if entry == "X":
                    entry = f"{term.red}{entry}{term.normal}"
                elif entry == "O":
                    entry = f"{term.blue}{entry}{term.normal}"
                else:
                    entry = "·"

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

    def victory_subgrid(
        self,
        term: blessed.Terminal,
        subgrid: npt.NDArray[np.str_],
        start_coords: typing.Tuple[int, int],
        winner: typing.Optional[typing.Literal["X", "O", "None"]],
    ) -> None:
        """Takes the subgrid and draws a victory symbol over that grid"""
        x, y = start_coords
        if winner == "None":
            return None
        if winner == "X":
            print(
                term.move_xy(x + 1, y)
                + f"{term.on_color_rgb(0, 0, 200)}{subgrid[0, 0]} {term.normal}"
                + term.move_x(x + 9)
                + f"{term.on_color_rgb(0, 0, 200)}{subgrid[0, 2]} {term.normal}"
            )
            print(
                term.move_x(x + 3)
                + f"{term.on_color_rgb(0, 0, 200)}┼─{term.normal}"
                + term.move_x(x + 7)
                + f"{term.on_color_rgb(0, 0, 200)}┼─{term.normal}"
            )
            print(
                term.move_x(x + 5)
                + f"{term.on_color_rgb(0, 0, 200)}{subgrid[1, 1]} {term.normal}"
            )
            print(
                term.move_x(x + 3)
                + f"{term.on_color_rgb(0, 0, 200)}┼─{term.normal}"
                + term.move_x(x + 7)
                + f"{term.on_color_rgb(0, 0, 200)}┼─{term.normal}"
            )
            print(
                term.move_x(x + 1)
                + f"{term.on_color_rgb(0, 0, 200)}{subgrid[2, 0]} {term.normal}"
                + term.move_x(x + 9)
                + f"{term.on_color_rgb(0, 0, 200)}{subgrid[2, 2]} {term.normal}"
            )
        if winner == "O":
            print(
                term.move_xy(x + 3, y)
                + f"{term.on_color_rgb(254, 0, 0)}│ {subgrid[0, 1]} │{term.normal}"
            )
            print(
                term.move_x(x + 2)
                + f"{term.on_color_rgb(254, 0, 0)}─{term.normal}"
                + term.move_x(x + 8)
                + f"{term.on_color_rgb(254, 0, 0)}─{term.normal}"
            )
            print(
                term.move_x(x + 2)
                + f"{term.on_color_rgb(254, 0, 0)} {term.normal}"
                + term.move_x(x + 8)
                + f"{term.on_color_rgb(254, 0, 0)} {term.normal}"
            )
            print(
                term.move_x(x + 2)
                + f"{term.on_color_rgb(254, 0, 0)}─{term.normal}"
                + term.move_x(x + 8)
                + f"{term.on_color_rgb(254, 0, 0)}─{term.normal}"
            )
            print(
                term.move_x(x + 3)
                + f"{term.on_color_rgb(254, 0, 0)}│ {subgrid[0, 1]} │{term.normal}"
            )

    def redraw_subgrid(
        self,
        term: blessed.Terminal,
        subgrid: npt.NDArray[np.str_],
        number: str,
        color: str,
        winner: typing.Optional[typing.Literal["X", "O"]],
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
        self.victory_subgrid(term, subgrid, start_coords[number], winner)
