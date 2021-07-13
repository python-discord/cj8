from rich.text import Text

from ..Level import Level


class AbstractDungeonEntity:
    """Base class to set items color and location"""

    def __init__(
        self,
        level: Level,
        ground_symbol: str = "'",
        y: int = 0,
        x: int = 0,
        symbol: str = "$",
        color: str = "white",
    ):
        self.x = x
        self.y = y
        self.symbol = Text(symbol)
        self.ground_symbol = Text(ground_symbol)
        self.ground_symbol.stylize("bold magenta")
        self.level = level
        if color:
            self.symbol.stylize(color)
        self.draw()

    def draw(self) -> None:
        """Places entity on map"""
        self.level.board[self.y][self.x] = self.symbol
