from .AbstractDungeonEntity import AbstractDungeonEntity


class Item(AbstractDungeonEntity):
    """Creates an item"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.collected = False
        self.entity_type = "item"

    def collisions_with_player(self, x: int, y: int) -> bool:
        """Checks if player collided with enemy"""
        return (self.x, self.y) == (x, y)

    def collect_item(self) -> None:
        """Set the status of the item to collected"""
        self.collected = True
