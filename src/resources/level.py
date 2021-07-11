from rich.text import Text
from random import choice


class Level:
    """Generates and contains a level"""

    def __init__(self, width: int, length: int, children: list, files: list) -> None:
        self.board = []
        self.width = width
        self.length = length
        self.doors = len(children)
        self.generate_level(length, width)

    def generate_level(self, x: int, y: int) -> None:
        """Generates level"""
        for j in range(y):
            row = []
            for i in range(x):
                text = Text("'", style="bold magenta")
                row.append(text)
            self.board.append(row)

    def add_doors(self) -> None:
        """Add doors to level"""
        distribution_of_doors = {'left': 0, 'bottom': 0, 'right': 0}
        for i in range(self.doors):
            distribution_of_doors[choice(list(distribution_of_doors.keys()))] += 1

        self.doors = distribution_of_doors


    def to_string(self) -> Text:
        """Convert map to string"""
        string_map = Text()
        for row in self.board:
            for col in row:
                string_map += col
            string_map += "\n"
        return string_map


level = Level(20, 20, [1,2,3,4,5], [])
print(level.board)