from rich.text import Text


class LevelResources(Text):
    """Creates meta objects that create level"""

    def __init__(self, symbol: str = '', style: str = ''):
        super().__init__(symbol, style=style)

    def __str__(self):
        """Returns display as a Text object"""
        return str(self.text)
