from .abstractdungeonentity import AbstractDungeonEntity


class Item(AbstractDungeonEntity):
    """Creates an item"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.collected = False
        self.ENTITY_TYPE = "item"

    def collisions_with_player(self, x: int, y: int) -> bool:
        """Checks if player collided with enemy"""
        return (self.x, self.y) == (x, y)
