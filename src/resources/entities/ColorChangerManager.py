from random import choice, randint, shuffle

from src.resources.constants import COLOR_CHANGER_CHOICES
from src.resources.entities import level
from src.resources.entities.character import Character

from .ColorChanger import ColorChanger


class ColorChangerManager:
    """Manager class to spawn color changers"""

    def __init__(self, level: level) -> None:
        self.color_changer_list = []
        self.selected_colors = []
        self.level = level

    def spawn_random_changers(self, x_player: int, y_player: int, num: int = 3) -> None:
        """Spawns color changers randomly"""
        shuffle(COLOR_CHANGER_CHOICES)
        new_list = COLOR_CHANGER_CHOICES.copy()
        while num > 0:
            y = randint(2, self.level.height-2)
            x = randint(2, self.level.width-2)
            disallowed_spaces = {'x': (x_player - 1, x_player + 1), 'y': (y_player - 1, y_player + 1)}
            if str(self.level.board[y][x]) == "'" and \
                    x not in disallowed_spaces['x'] and y not in disallowed_spaces['y']:
                num -= 1

                color = choice(new_list)
                new_list.pop(new_list.index(color))
                color_changer = ColorChanger(x=x, y=y, symbol='@', color=color)
                self.color_changer_list.append(color_changer)
                color = ''

    def collisions_with_player(self, x: int, y: int) -> bool:
        """Determines which color changer collides with player and returns new color"""
        for color_changer in self.color_changer_list:
            if (color_changer.x, color_changer.y) == (x, y):
                return color_changer.color
        return False

    def change_color(self, player: Character, color: str) -> None:
        """Will change color of player instance"""
        player.color = color
        player.symbol.stylize(color)
