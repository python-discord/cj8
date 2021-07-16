from .AbstractDungeonEntity import AbstractDungeonEntity


class ColorChanger(AbstractDungeonEntity):
    """Dungeon Items that change players color if captured"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
