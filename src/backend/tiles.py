import dataclasses
import math
import random
from abc import ABC
from enum import Enum
from typing import Optional, Tuple


@dataclasses.dataclass()
class AdjacentTiles:
    """All the tiles adjacent to a specific tile"""

    up: Optional["BaseTile"] = None
    down: Optional["BaseTile"] = None
    left: Optional["BaseTile"] = None
    right: Optional["BaseTile"] = None


@dataclasses.dataclass()
class Pos:
    """Nicer data class for x and y coords"""

    x: int
    y: int


class CardinalDirection(Enum):
    """Cardinal directions"""

    up = 0
    right = 1
    down = 2
    left = 3


class BaseTile(ABC):
    """
    Base Tile object for the game

    Different types of tiles will subclass this object and implement the specific
    properties of that tile.
    """

    def __init__(self, pos: Tuple[int, int], color: Tuple[int, int, int]):
        self.pos: Pos = Pos(x=pos[0], y=pos[1])
        self.color = color

        self.tile_char: str = "   "

        self.adjacent_tiles: AdjacentTiles = AdjacentTiles()

    @property
    def pos_tuple(self) -> Tuple[int, int]:
        """Return a tuple of x and y coords for unpacking"""
        return self.pos.x, self.pos.y

    def calc_distance(self, other_tile: "BaseTile") -> float:
        """
        Distance to other_tile

        Calculate the euclidean distance between this object and the BaseTiles passed
        to the method

        :param other_tile: BaseTile to compare the distance to
        """
        return math.sqrt(
            ((other_tile.pos.x - self.pos.x) ** 2)
            + ((other_tile.pos.y - self.pos.y) ** 2)
        )

    def __str__(self):
        return self.tile_char


class BallTile(BaseTile):
    """The ball tile"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.direction = CardinalDirection.down

    def __str__(self):
        return " ○ "


class GoalTile(BaseTile):
    """Tiles the Goal"""

    def __str__(self):
        return " ■ "


class PathTile(BaseTile):
    """Tiles the ball can travel across"""

    def __str__(self):
        return "   "


class StoryTile(PathTile):
    """Tiles that the ball can travel across and move the story forward"""

    def __init__(self, pos: Tuple[int, int], color: Tuple[int, int, int]):
        super().__init__(pos, color)
        self.visited = False


class BlindTile(BaseTile):
    """Tiles that are outside of vision."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, color=(32, 32, 32))

    def __str__(self):
        return "   "


class PauseTile(BaseTile):
    """Tile to show game pause state."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, color=(255, 255, 255))

    def __str__(self):
        return " ⏸︎ "


class WallTile(BaseTile):
    """
    Tiles demarking impassable tiles

    Uses adjacent tiles to work out how it should be represented on screen
    """

    def __str__(self):
        up = isinstance(self.adjacent_tiles.up, WallTile)
        down = isinstance(self.adjacent_tiles.down, WallTile)
        left = isinstance(self.adjacent_tiles.left, WallTile)
        right = isinstance(self.adjacent_tiles.right, WallTile)

        truth_tuple = (up, down, left, right)

        if truth_tuple == (True, True, False, False):
            return " │ "
        if truth_tuple == (False, False, True, True):
            return "───"
        if truth_tuple == (False, True, False, True):
            return " ┌─"
        if truth_tuple == (False, True, True, False):
            return "─┐ "
        if truth_tuple == (True, False, False, True):
            return " └─"
        if truth_tuple == (True, False, True, False):
            return "─┘ "
        if truth_tuple == (True, True, False, True):
            return " ├─"
        if truth_tuple == (True, True, True, False):
            return "─┤ "
        if truth_tuple == (False, True, True, True):
            return "─┬─"
        if truth_tuple == (True, False, True, True):
            return "─┴─"

        return "─┼─"


class RedirectorTile(BaseTile):
    """Tiles that redirect the balls movement"""

    ORIENTATIONS = {
        CardinalDirection.up: "↑",
        CardinalDirection.right: "→",
        CardinalDirection.down: "↓",
        CardinalDirection.left: "←",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.direction = random.choice(list(CardinalDirection))

    def __str__(self):
        return f" {self.ORIENTATIONS[self.direction]} "

    def rotate(self, clockwise: bool = True) -> None:
        """Rotate redirector tile in direction specified."""
        turn = 1 if clockwise else -1
        self.direction = CardinalDirection((self.direction.value + turn) % 4)
