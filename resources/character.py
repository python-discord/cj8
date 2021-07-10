from rich.text import Text

class Character:

    def __init__(self, x=0, y=0, symbol='$'):
        self.x = x
        self.y = y
        self.symbol = Text(symbol)

    def update(self, direction=()):
        if direction:
            if self.x + direction[0] <= 9 and self.x + direction[0] >= 0:
                self.x += direction[0]
            if self.y + direction[1] <= 9 and self.y + direction[1] >= 0:
                self.y += direction[1]

    def draw(self, level: list):
        level[self.x][self.y] = self.symbol
        return level
