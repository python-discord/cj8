from rich.text import Text

from .level.LevelResources import LevelResources
from .level.Tile import Tile


class AbstractDungeonEntity:
    """Base class to set items color and location"""

    def __init__(
        self,
        ground_symbol: str = "'",
        y: int = 0,
        x: int = 0,
        symbol: str = "$",
        color: str = "white",
    ):
        super().__init__()
        self.x = x
        self.y = y
        self.symbol = Text(symbol)
        self.ground_symbol: LevelResources = Tile(text=ground_symbol, style="bold magenta")

        self.new_positions: dict = {"x": 0, "y": 0}

        if color:
            self.symbol.stylize(color)
