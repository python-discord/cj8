from .levelresources import LevelResources


class Wall(LevelResources):
    """Creates a Door object"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
