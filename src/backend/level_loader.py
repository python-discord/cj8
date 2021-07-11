from pathlib import Path
from typing import List, Tuple

from PIL import Image

from src.backend.core import BoardCollection
from src.backend.tiles import (
    BallTile,
    BaseTile,
    GoalTile,
    PathTile,
    RedirectorTile,
    WallTile,
)


class CoreLevelLoader:
    """
    Load a map from an image file

    The image should be a png file within the levels folder.

    The color codes just below correspond to the different types of tiles.
    (R,G,B)
    """

    LEVELS_DIR = Path("levels").absolute()
    PATH = "(255, 255, 255)"
    WALL = "(0, 0, 0)"
    BALL = "(237, 28, 36)"
    GOAL = "(34, 177, 76)"
    REDIRECTOR = "(0, 162, 232)"

    color_dispatcher = {
        PATH: PathTile,
        WALL: WallTile,
        BALL: BallTile,
        GOAL: GoalTile,
        REDIRECTOR: RedirectorTile,
    }

    def __init__(self) -> None:
        self._raw_pixel_list = None
        self.level = None
        self.size = None

    def load(self, level_name: str) -> None:
        """Load the map into memory"""
        level_path = self.LEVELS_DIR / level_name
        if not level_path.is_file():
            raise AssertionError(f"No file found for {level_path}")

        raw_image = Image.open(level_path)
        self.size = raw_image.size
        self._raw_pixel_list = list(raw_image.getdata())

        all_tiles, ball = self._gen_map_repr()

        self.level = BoardCollection.from_file(all_tiles, ball, self.size)

    def _gen_map_repr(self) -> Tuple[List[List[BaseTile]], BallTile]:
        width, height = self.size
        ball = None
        all_tiles = []
        for y in range(height):
            row = []
            for x in range(width):
                tile_color_str = str(self._pixel(x, y))
                tile = self.color_dispatcher[tile_color_str](pos=(x, y))
                row.append(tile)

                if tile_color_str == self.BALL:
                    ball = tile
            all_tiles.append(row)
        return all_tiles, ball

    def _pixel(self, x: int, y: int) -> Tuple[int, int, int]:
        width, _ = self.size
        return self._raw_pixel_list[width * y + x]


if __name__ == "__main__":
    test = CoreLevelLoader()
    test.load("lvl1.png")
