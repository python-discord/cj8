from rich.text import Text


class Level:

    def __init__(self, x=0, y=0):
        self.board = []
        self.generate_level(x, y)

    def generate_level(self, x, y):
        for j in range(y):
            row = []
            for i in range(x):
                text = Text("'", style="bold magenta")
                row.append(text)
            self.board.append(row)

    def to_string(self) -> Text:
        string_map = Text()
        for row in self.board:
            for col in row:
                string_map += col
            string_map += '\n'
        return string_map
