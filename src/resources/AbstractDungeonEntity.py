from rich.text import Text


class AbstractDungeonEntity:
    """Base class to set items color and location"""

    def __init__(self, ground_symbol: str = "'", x: int = 0, y: int = 0, symbol: str = "$", color: str = '', ):
        self.x = x
        self.y = y
        self.symbol = Text(symbol)
        self.ground_symbol = ground_symbol
        if color:
            self.symbol.stylize(color)

    def draw(self, level: list) -> None:
        """Places object on map"""
        level[self.x][self.y] = self.symbol
        return level
