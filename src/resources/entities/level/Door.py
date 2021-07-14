from .LevelResources import LevelResources


class Door(LevelResources):
    """Creates a Door object"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
