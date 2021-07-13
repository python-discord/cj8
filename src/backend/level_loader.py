import random
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Tuple

from PIL import Image

from src.backend.tiles import (
    BallTile,
    BaseTile,
    GoalTile,
    PathTile,
    RedirectorTile,
    StoryTile,
    WallTile,
)
from src.file_logging import logger


class BoardCollection:
    """Representation of the game board"""

    class Size:
        x_max = 0
        y_max = 0

    def __init__(self):
        self.all_tiles: List[List[BaseTile]] = []
        self._ball = None
        self.under_ball = None
        self.size = None
        self.level_path: Optional[Path] = None

    @classmethod
    def from_file(
        cls,
        all_tiles: List[List[BaseTile]],
        ball: BallTile,
        size: Tuple[int, int],
        level_path: Path,
    ):
        """Build the representation from a image file"""
        board = cls()
        board.all_tiles = all_tiles
        board._ball = ball
        board.size = size
        board.level_path = level_path
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

    @property
    def level_name(self) -> str:
        """Return the name of the current level."""
        return self.level_path.stem

    def pprint(self) -> None:
        """Display the map for testing"""
        for row in self.all_tiles:
            row_str = ""
            for tile in row:
                row_str += str(tile)
            print(row_str)


class CoreLevelLoader:
    """
    Load a map from an image file

    The image should be a png file within the levels folder.

    The color codes just below correspond to the different types of tiles.
    (R,G,B)
    """

    LEVELS_DIR = Path(__file__).absolute().parent / "levels"
    PATH = "(255, 255, 255)"
    WALL = "(0, 0, 0)"
    BALL = "(237, 28, 36)"
    GOAL = "(34, 177, 76)"
    STORY_TILE = "(163, 73, 164)"

    color_dispatcher = {
        PATH: PathTile,
        WALL: WallTile,
        BALL: BallTile,
        GOAL: GoalTile,
        STORY_TILE: StoryTile,
    }

    def __init__(self) -> None:
        self._raw_pixel_list = None
        self.level = None
        self.size = None

        self.logger = logger

    @classmethod
    def load(cls, level_name: str) -> BoardCollection:
        """Load the map into memory"""
        loader = cls()
        level_path = loader.LEVELS_DIR / level_name

        start = datetime.now()
        logger.info(f"Loading level: {level_name} from file {level_path}")

        if not level_path.is_file():
            raise AssertionError(f"No file found for {level_path}")

        raw_image = Image.open(level_path)
        loader.size = raw_image.size
        loader._raw_pixel_list = list(raw_image.getdata())

        all_tiles, ball = loader._gen_map_repr()

        end = datetime.now()
        logger.info(f"Loading took: {(end - start).microseconds / 1000:03}ms")

        return BoardCollection.from_file(all_tiles, ball, loader.size, level_path)

    @staticmethod
    def random_level() -> BoardCollection:
        """Load a random level."""
        levels = list(CoreLevelLoader.LEVELS_DIR.iterdir())
        return CoreLevelLoader.load(random.choice(levels))

    def _gen_map_repr(self) -> Tuple[List[List[BaseTile]], BallTile]:
        width, height = self.size
        ball = None
        all_tiles = []
        for y in range(height):
            row = []
            for x in range(width):
                tile_color_str = str(self._pixel(x, y))
                # Default the tile to redirector if tile colour does match
                if tile_color_str not in self.color_dispatcher:
                    tile = RedirectorTile(pos=(x, y), color=self._pixel(x, y))
                else:
                    # Look up the type of tile that matches the color tuple
                    tile = self.color_dispatcher[tile_color_str](
                        pos=(x, y), color=self._pixel(x, y)
                    )
                row.append(tile)

                if tile_color_str == self.BALL:
                    ball = tile
            all_tiles.append(row)
        return all_tiles, ball

    def _pixel(self, x: int, y: int) -> Tuple[int, int, int]:
        width, _ = self.size
        return self._raw_pixel_list[width * y + x]


if __name__ == "__main__":
    board = CoreLevelLoader.load("lvl1.png")
    board = CoreLevelLoader.random_level()
