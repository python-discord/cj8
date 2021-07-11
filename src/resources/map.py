from rich.text import Text


class Level:
    """Generates and contains a level"""

    def __init__(self, x: int = 0, y: int = 0):
        self.board = []
        self.generate_level(x, y)

    def generate_level(self, x: int, y: int) -> None:
        """Generates level"""
        for j in range(y):
            row = []
            for i in range(x):
                text = Text("'", style="bold magenta")
                row.append(text)
            self.board.append(row)

    def to_string(self) -> Text:
        """Convert map to string"""
        string_map = Text()
        for row in self.board:
            for col in row:
                string_map += col
            string_map += "\n"
        return string_map
