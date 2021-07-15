import random

from .AbstractDungeonEntity import AbstractDungeonEntity
from .character import Character


class ColorChanger(AbstractDungeonEntity):
    """Dungeon Items that change players color if captured"""

    _choices = ['blue', 'red', 'yellow']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.color = "bold " + random.choice(self._choices)
        self.symbol.stylize(self.color)

    def collisions_with_player(self, x: int, y: int) -> bool:
        """Checks if player collided with enemy"""
        return (self.x, self.y) == (x, y)

    def change_color(self, player: Character) -> None:
        """Will change color of player instance and reset to normal game tile"""
        player.symbol.stylize(self.color)
