from rich.text import Text


class Entity(Text):
    """Abstract class for all objects"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
