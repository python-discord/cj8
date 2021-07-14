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
        """Determine if the entire board has been won, and by who."""
        grid_states = np.array(
            (self.check_subboard_victory(i) for i in "789456123"), dtype=np.str_
        )
        # This might have off ordering, TODO on testing it
        grid_states.reshape((3, 3))
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
            diagonal_l = ticks.fliplr().diagonal().sum() == 3
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

        # Mypy cannot penetrate the slicing behavior here, so we assert that it is correct
        return self.contents[subgrid_map[number]]  # type: ignore

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
