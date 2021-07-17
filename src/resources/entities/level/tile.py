from .levelresources import LevelResources


class Tile(LevelResources):
    """Creates a Door object"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ENTITY_TYPE = "tile"
