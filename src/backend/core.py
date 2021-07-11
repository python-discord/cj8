from enum import Enum
from typing import List, Tuple, Union

from src.backend.tiles import BallTile, BaseTile


class DebugMixin:
    """Debugging mixin methods for the backend module"""


class CardinalDirection(Enum):
    """Cardinal directions"""

    up = "up"
    down = "down"
    left = "left"
    right = "right"


class BoardCollection:
    """Representation of the game board"""

    class Size:
        x_max = 0
        y_max = 0

    def __init__(self):
        self.all_tiles: List[List[BaseTile]] = []
        self._ball = None
        self.size = None

    @classmethod
    def from_file(
        cls, all_tiles: List[List[BaseTile]], ball: BallTile, size: Tuple[int, int]
    ):
        """Build the representation from a image file"""
        board = cls()
        board.all_tiles = all_tiles
        board._ball = ball
        board.size = size
        board.link_adjacents()
        return board

    def link_adjacents(self) -> None:
        """
        Link the tiles to their neighbors

        Iterate over all the tiles that make up the make and link them in their cardinal
        directions. This will be used for pathing and generating wall segments
        """
        x, y = self.size
        for y_idx, row in enumerate(self.all_tiles):
            for x_idx, tile in enumerate(row):
                tile: BaseTile
                # Link tile below if exists
                if y_idx < y - 1:
                    tile.adjacent_tiles.down = self.all_tiles[y_idx + 1][x_idx]
                # Link tile above if exists
                if y_idx > 0:
                    tile.adjacent_tiles.up = self.all_tiles[y_idx - 1][x_idx]
                # Link tile to the right if exists
                if x_idx < x - 1:
                    tile.adjacent_tiles.right = self.all_tiles[y_idx][x_idx + 1]
                # Link tile to the left if exists
                if x_idx > 0:
                    tile.adjacent_tiles.left = self.all_tiles[y_idx][x_idx - 1]

    @property
    def ball(self) -> BallTile:
        """Return the ball tile"""
        return self._ball

    def pprint(self) -> None:
        """Display the map for testing"""
        for row in self.all_tiles:
            row_str = ""
            for tile in row:
                row_str += str(tile)
            print(row_str)


class CoreBackend(DebugMixin):
    """
    Backend Module

    Responsible for storing the state of the game as well as update the state once
    action have taken place.

    Should return the tile object which represents the ball as well and any tiles
    within a certain distance from the ball.

    Should generate a random board that is solvable.

    Should return the position of the box at the end.

    Should list mutators as well as being able to apply and remove these mutators.

    Should keep track of elapsed time and current score.
    """

    def get_ball(self, surrounding_radius: float) -> Tuple[BaseTile, List[BaseTile]]:
        """
        Gets the ball tile

        Retrieves the ball tile as well as any tiles within an area with a radius of
        surrounding_radius.

        """

    def key_press(self, key: Union[str, None]) -> None:
        """
        Let the backend know when a key press has happened.

        This will trigger any actions that need to happen on the tiles.

        :param key: keyboard character that was pressed

        If the action is none then just move to the next frame with no input. This would
        be to advance the game by one step.
        """
