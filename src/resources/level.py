from random import choice, randint

from rich.text import Text


class Level:
    """Generates and contains a level"""

    def __init__(self, width: int, height: int, children: list, files: list) -> None:
        self.board = []
        self.width = width
        self.height = height
        self.door_symbol = Text("#", style="bold green")
        self.generate_level(width, height)
        self.set_border()
        self.add_doors(len(children))

    def generate_level(self, x: int, y: int) -> None:
        """Generates level"""
        for j in range(y):
            row = []
            for i in range(x):
                text = Text("'", style="bold magenta")
                row.append(text)
            self.board.append(row)

    def add_doors(self, doors: list) -> None:
        """Add doors to level"""
        door_direction = ['right', 'bottom', 'left']
        while doors > 0:
            direction: str = choice(door_direction)
            x: int = 0
            y: int = 0
            if direction == 'right':
                y = randint(0, self.height - 1)
                x = self.width - 1
            if direction == 'bottom':
                x = randint(0, self.width - 1)
                y = self.height - 1
            if direction == 'left':
                y = randint(0, self.height - 1)
                x = 0

            if self.board[y][x] != self.door_symbol:
                self.board[y][x] = self.door_symbol
                doors -= 1

    def set_border(self) -> None:
        """Creates a walls around the level"""
        for i in range(self.width):
            self.board[0][i] = Text("═", style="bold white")
            self.board[self.height-1][i] = Text("═", style="bold white")
        for i in range(self.height):
            self.board[i][0] = Text("║", style="bold white")
            self.board[i][self.width-1] = Text("║", style="bold white")
        self.board[0][0] = Text("╔", style="bold white")
        self.board[self.height-1][0] = Text("╚", style="bold white")
        self.board[0][self.width-1] = Text("╗", style="bold white")
        self.board[self.height-1][self.width-1] = Text("╝", style="bold white")

    def to_string(self) -> Text:
        """Convert map to string"""
        string_map = Text()
        for row in self.board:
            for col in row:
                string_map += col
            string_map += "\n"
        return string_map
