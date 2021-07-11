import dataclasses
import math
from abc import ABC
from typing import Dict, List, Tuple, Union


@dataclasses.dataclass()
class AdjacentTiles:
    """All the tiles adjacent to a specific tile"""

    up: Union[None, "BaseTile"] = None
    down: Union[None, "BaseTile"] = None
    left: Union[None, "BaseTile"] = None
    right: Union[None, "BaseTile"] = None


class BaseTile(ABC):
    """
    Base Tile object for the game

    Different types of tiles will subclass this object and implement the specific
    properties of that tile.
    """

    def __init__(self, pos: List[int, int]):
        self.pos: List[int, int]
        self.color: Tuple[int, int, int, int]
        self.control_scheme: Dict

        self.tile_char: str

        self.adjacent_tiles: AdjacentTiles = AdjacentTiles()

    def calc_distance(self, other_tile: "BaseTile") -> float:
        """
        Distance to other_tile

        Calculate the euclidean distance between this object and the BaseTiles passed
        to the method

        :param other_tile: BaseTile to compare the distance to
        """
        return math.sqrt(
            ((other_tile.pos[0] - self.pos[0]) ** 2)
            + ((other_tile.pos[1] - self.pos[1]) ** 2)
        )

    def __str__(self):
        return self.tile_char
