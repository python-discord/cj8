from random import choice, randint, shuffle

from rich.text import Text

from src.fstree.Node import Node
from src.resources.constants import COLOR_CHANGER_CHOICES
from src.resources.entities.ColorChanger import ColorChanger
from src.resources.entities.Item import Item

from ..Enemy import Enemy
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

    def spawn_random_changers(self, num: int = 3) -> None:
        """Spawns color changers randomly"""
        shuffle(COLOR_CHANGER_CHOICES)
        new_list = COLOR_CHANGER_CHOICES.copy()
        while num > 0:
            y = randint(2, self.height-2)
            x = randint(2, self.width-2)

            if str(self.board[y][x]) == "'":
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

            if str(self.board[y][x]) == "'":
                item = Item(symbol=chr(0xA2), x=x, y=y, color="bold #afa208")
                item_entry = {id(item): item}
                self.items.update(item_entry)
                num -= 1

    def spawn_random_enemies(self, num: int) -> None:
        """Spawns a new enemies randomly"""
        while num > 0:
            y = randint(2, self.height - 2)
            x = randint(2, self.width - 2)
            disallowed_spaces = {'x': (self.entrance[1] - 1, self.entrance[1] + 1),
                                 'y': (self.entrance[0] - 1, self.entrance[0] + 1)}
            if str(self.board[y][x]) == "'" and \
                    x not in disallowed_spaces['x'] and y not in disallowed_spaces['y']:
                num -= 1
                enemy = Enemy(aggro_radius=3, x=x, y=y, symbol='^')
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
