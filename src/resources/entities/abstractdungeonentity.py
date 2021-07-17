import random

from rich.text import Text

from src.resources.constants import (
    COLOR_CHANGER_CHOICES, PLAYER_COLOR_CHOICES, TILE
)

from .level.levelresources import LevelResources
from .level.tile import Tile


class AbstractDungeonEntity:
    """Base class to set items color and location"""

    def __init__(
        self,
        ground_symbol: str = TILE,
        y: int = 0,
        x: int = 0,
        symbol: str = "$",
        color: str = None,
    ):
        super().__init__()
        self.x = x
        self.y = y
        self.symbol = Text(symbol)
        self.ground_symbol: LevelResources = Tile(text=ground_symbol, style="bold grey39")

        self.new_positions: dict = {"x": 0, "y": 0}
        self.color = self.set_color(color)

    def __gt__(self, obj: type) -> bool:
        """Return True if current object is greater than"""
        if self.color == "bold red" and obj.color == "bold green":
            state = True
        elif self.color == "bold green" and obj.color == "bold blue":
            state = True
        elif self.color == "bold blue" and obj.color == "bold red":
            state = True
        else:
            state = False
        return state

    def __lt__(self, obj: type) -> bool:
        """Returns True if current object is less than"""
        if self.color == "bold green" and obj.color == "bold red":
            state = True
        elif self.color == "bold blue" and obj.color == "bold green":
            state = True
        elif self.color == "bold red" and obj.color == "bold blue":
            state = True
        else:
            state = False
        return state

    def __eq__(self, obj: type) -> bool:
        """Compares AbstractEntityObjects for equality"""
        return self.color == obj.color

    def __ne__(self, obj: type) -> bool:
        """Compare AbstractEntityObjects for inequaulity"""
        return self.color != obj.color

    def set_color(self, color: str) -> str:
        """Determines if color can be set or called by random"""
        if not color:
            color = self._choose_random_color()
        self.symbol.stylize(color)
        return color

    def _choose_random_color(self) -> None:
        """Selects random color based on instantiated class"""
        if self.__class__.__name__ in ['Enemy', 'Character']:
            color = random.choice(PLAYER_COLOR_CHOICES)
        else:
            color = random.choice(COLOR_CHANGER_CHOICES)
        return color
