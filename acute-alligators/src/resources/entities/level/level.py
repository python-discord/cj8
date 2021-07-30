import math
from random import choice, randint, shuffle

from rich.console import Console
from rich.text import Text

from src.fstree.node import Node
from src.resources.constants import COLOR_CHANGER_CHOICES, TILE
from src.resources.entities.colorchanger import ColorChanger
from src.resources.entities.item import Item

from ..enemy import Enemy
from .door import Door
from .tile import Tile
from .wall import Wall


class Level:
    """Generates and contains a level"""

    def __init__(self, width: int, height: int, cur_node: Node) -> None:
        self.console = Console()
        self.entrance = (0, 0)
        self.parent_door = (0, 0)
        self.board = []
        self.width = width
        self.height = height
        self.cur_node = cur_node
        self.doors = {}
        self.color_changers = []
        self.items = {}
        self.enemies = {}

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
                tile = Tile(text=TILE, style="bold grey39")
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

    def spawn_random_changers(self, num: int = 3) -> None:
        """Spawns color changers randomly"""
        shuffle(COLOR_CHANGER_CHOICES)
        new_list = COLOR_CHANGER_CHOICES.copy()
        while num > 0:
            y = randint(2, self.height-2)
            x = randint(2, self.width-2)

            if str(self.board[y][x]) == TILE:
                num -= 1
                color = choice(new_list)
                new_list.pop(new_list.index(color))
                color_changer = ColorChanger(x=x, y=y, symbol='@', color=color)
                self.color_changers.append(color_changer)

    def spawn_dungeon_items(self, num: int) -> None:
        """Creates Dungeon items in random locations"""
        while num > 0:
            y = randint(2, self.height-2)
            x = randint(2, self.width-2)

            if str(self.board[y][x]) == TILE:
                item = Item(symbol=chr(0xA2), x=x, y=y, color="bold #afa208")
                item_entry = {id(item): item}
                self.items.update(item_entry)
                num -= 1

    def spawn_random_enemies(self, files: list) -> None:
        """Spawns a new enemies randomly"""
        num = len(files)
        left = math.floor(self.width * .33)
        right = self.width - left
        bottom = math.floor(self.height * .33)
        top = self.height - bottom
        while num > 0:
            enemy_type = randint(0, 10)
            enemy_symbol = "^"
            agro = 3
            if enemy_type > 7:
                enemy_symbol = "!"
                agro = 5
            y = randint(bottom, top)
            x = randint(left, right)
            if str(self.board[y][x]) == TILE:
                num -= 1
                enemy = Enemy(aggro_radius=agro, x=x, y=y, symbol=enemy_symbol, file=files[num-1])
                enemy_entry = {id(enemy): enemy}
                self.enemies.update(enemy_entry)

    def remove_enemy(self, enemy: Enemy) -> None:
        """Removes an enemy and replaces level symbol"""
        enemy_id = id(enemy)
        if enemy_id in self.enemies.keys():
            self.enemies.pop(enemy_id)
        self.board[enemy.y][enemy.x] = enemy.ground_symbol

    def remove_item(self, item: Item) -> None:
        """Removes item and replaces level symbol"""
        item_id = id(item)
        if item_id in self.items.keys():
            self.items.pop(item_id)
        self.board[item.y][item.x] = item.ground_symbol

    def to_string(self) -> Text:
        """Convert map to string"""
        top_buffer = (math.floor(self.console.height * .66) - self.height) // 2
        top_buffer = " \n" * top_buffer
        left_buffer = (math.floor(self.console.width * .66) - self.width) // 2
        left_buffer = " " * left_buffer
        string_map = Text(left_buffer)
        for row in self.board:
            for col in row:
                string_map += col
            string_map += "\n" + left_buffer

        return Text(top_buffer) + string_map
