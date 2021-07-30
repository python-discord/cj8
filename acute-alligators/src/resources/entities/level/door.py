from .levelresources import LevelResources


class Door(LevelResources):
    """Creates a Door object"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id: int = 0
        self.pos: (int, int) = (0, 0)
