from rich.text import Text


class Character:
    """This describes a character"""

    def __init__(self, x: int = 0, y: int = 0, symbol: str = "$"):
        self.x = x
        self.y = y
        self.symbol = Text(symbol)

    def update(self, direction: ()) -> None:
        """Takes a direction and updates the player position"""
        if direction:
            # this positon check needs to be refactored.
            if self.x + direction[0] <= 9 and self.x + direction[0] >= 0:
                self.x += direction[0]
            if self.y + direction[1] <= 9 and self.y + direction[1] >= 0:
                self.y += direction[1]

    def draw(self, level: list) -> None:
        """Places player on map"""
        level[self.x][self.y] = self.symbol
        return level
