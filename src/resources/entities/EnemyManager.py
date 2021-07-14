from random import randint

from ..Level import Level
from .Enemy import Enemy


class EnemyManager:
    """Manager class to add, update, and draw enemy"""

    def __init__(self, level: Level):
        self.enemy_list = []
        self.level = level

    def spawn_random_enemies(self, x_player: int, y_player: int, num: int) -> None:
        """Spawns a new enemies randomly"""
        while num > 0:
            y = randint(2, self.level.height-2)
            x = randint(2, self.level.width-2)
            disallowed_spaces = {'x': (x_player - 1, x_player + 1), 'y': (y_player - 1, y_player + 1)}

            if str(self.level.board[y][x]) == "'" and \
                    x not in disallowed_spaces['x'] and y not in disallowed_spaces['y']:
                num -= 1
                enemy = Enemy(level=self.level, x=x, y=y, symbol='^')
                self.enemy_list.append(enemy)

    def update(self, x: int, y: int) -> None:
        """Update each enemy in enemy list"""
        for enemy in self.enemy_list:
            enemy.update(x, y)

    def collisions_with_player(self, x: int, y: int) -> bool:
        """Checks if player collided with enemy"""
        return any([(enemy.x, enemy.y) == (x, y) for enemy in self.enemy_list])

    def draw(self) -> None:
        """Draw each enemy in enemy list"""
        for enemy in self.enemy_list:
            enemy.draw()
