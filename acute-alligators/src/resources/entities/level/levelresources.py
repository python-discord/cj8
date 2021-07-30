from ..entity import Entity


class LevelResources(Entity):
    """Creates meta objects that create level"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ENTITY_TYPE = ""
