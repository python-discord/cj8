from .AbstractDungeonEntity import AbstractDungeonEntity


class Enemy(AbstractDungeonEntity):
    """Enemy entity and hostile to players"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
