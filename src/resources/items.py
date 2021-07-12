from .AbstractDungeonEntity import AbstractDungeonEntity
from .character import Character


class AbstractColorChangingItem(AbstractDungeonEntity):
    """Dungeon Items that change players color if captured"""

    used_items = []
    unused_items = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def check_for_collision(self, player: Character) -> None:
        """Compares player's location to Dungeon Item"""
        pass

    def reset(self) -> None:
        """Resets symbol to normal game 'tick'"""
        self.used_items.append(self.symbol)
        self.symbol = "'"
        self.symbol.stylize = "magenta"
