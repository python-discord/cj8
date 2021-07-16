from random import randint

from rich.text import Text

from src.fstree.Node import Node

from .Door import Door
from .Tile import Tile
from .Wall import Wall


class Level:
    """Generates and contains a level"""

    def __init__(self, width: int, height: int, cur_node: Node) -> None:
        self.entrance = (0, 0)
        self.parent_door = (0, 0)
        self.board = []
        self.width = width
        self.height = height
        self.cur_node = cur_node
        self.doors = {}

    def create_doors(self, entrance: (int, int)) -> None:
        """Creates a door given an entrance or generates a random door on the first iteration"""
        self.entrance = entrance

        if entrance != (0, 0):
            parent_pos = self.generate_entrance(entrance)
            door = {parent_pos: self.cur_node.parent}
            self.doors.update(door)

        for node in self.cur_node.children:
            door = {self.generate_random_door(): node}
            self.doors.update(door)

    def generate_level(self) -> None:
        """Generates level"""
        for j in range(self.height):
            row = []
            for i in range(self.width):
                tile = Tile(text="'", style="bold magenta")
                row.append(tile)
            self.board.append(row)
        self.set_border()

    def generate_random_door(self) -> (int, int):
        """Creates a door randomly around the edge"""
        x: int = 0
        y: int = 0
        adding_door = True

        while adding_door:
            direction: int = randint(0, 2)
            if direction == 2:
                y = randint(1, self.height - 2)
                x = self.width - 1
            if direction == 1:
                x = randint(1, self.width - 2)
                y = self.height - 1
            if direction == 0:
                y = randint(1, self.height - 2)
                x = 0

            if str(self.board[y][x]) != "#":
                door = Door(text="#", style="bold green")
                door.pos = (y, x)
                self.board[y][x] = door
                adding_door = False

        return y, x

    def generate_entrance(self, first_door: (int, int)) -> (int, int):
        """Given a door generates the entrance on the other side of the level"""
        door = Door(text="#", style="bold green")
        y, x = first_door
        if first_door[0] == 0:
            y = self.height - 1
        if first_door[1] == 0:
            x = self.width - 1
        if first_door[0] == self.height - 1:
            y = 0
        if first_door[1] == self.width - 1:
            x = 0
        self.entrance = (y, x)
        self.board[y][x] = door

        return y, x

    def add_doors(self, first_door: (int, int)) -> None:
        """Add doors to level"""
        door_num = len(self.cur_node.children)

        if first_door != (0, 0):
            self.first_door = first_door
            door = Door(text="#", style="bold green")
            y, x = first_door
            if first_door[0] == 0:
                y = self.height - 1
            if first_door[1] == 0:
                x = self.width - 1
            if first_door[0] == self.height - 1:
                y = 0
            if first_door[1] == self.width - 1:
                x = 0
            self.entrance = (y, x)
            self.board[y][x] = door
            door_num -= 1

        while door_num:
            direction: int = randint(0, door_num) % 3
            x: int = 0
            y: int = 0
            if direction == 2:
                y = randint(1, self.height - 2)
                x = self.width - 1
            if direction == 1:
                x = randint(1, self.width - 2)
                y = self.height - 1
            if direction == 0:
                y = randint(1, self.height - 2)
                x = 0

            if str(self.board[y][x]) != "#":
                door = Door(text="#", style="bold green")
                door.id = door_num
                door.pos = (y, x)
                self.board[y][x] = door
                door_num -= 1

    def set_border(self) -> None:
        """Creates a walls around the level"""
        for i in range(self.width):
            self.board[0][i] = Wall(text="═", style="bold white")
            self.board[self.height - 1][i] = Wall(text="═", style="bold white")
        for i in range(self.height):
            self.board[i][0] = Wall(text="║", style="bold white")
            self.board[i][self.width - 1] = Wall(text="║", style="bold white")
        self.board[0][0] = Wall(text="╔", style="bold white")
        self.board[self.height - 1][0] = Wall(text="╚", style="bold white")
        self.board[0][self.width - 1] = Wall(text="╗", style="bold white")
        self.board[self.height - 1][self.width - 1] = Wall(text="╝", style="bold white")

    def to_string(self) -> Text:
        """Convert map to string"""
        string_map = Text()
        for row in self.board:
            for col in row:
                string_map += col
            string_map += "\n"
        return string_map
