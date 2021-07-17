from random import randint

from src.resources.entities.level import Level

from .Enemy import Enemy


class EnemyManager:
    """Manager class to add, update, and draw enemy"""

    def __init__(self, level: Level):
        self.enemy_list = []
        self.level = level
        self.enemies_down = 0

    def spawn_random_enemies(self, x_player: int, y_player: int, num: int) -> None:
        """Spawns a new enemies randomly"""
        while num > 0:
            y = randint(2, self.level.height-2)
            x = randint(2, self.level.width-2)
            disallowed_spaces = {'x': (x_player - 1, x_player + 1), 'y': (y_player - 1, y_player + 1)}
            if str(self.level.board[y][x]) == "'" and \
                    x not in disallowed_spaces['x'] and y not in disallowed_spaces['y']:
                num -= 1
                enemy = Enemy(aggro_radius=3, x=x, y=y, symbol='^')
                self.enemy_list.append(enemy)

    def remove_enemy(self, enemy: type) -> None:
        """Replace enemy with symbol"""
        self.enemies_down += 1
        self.enemy_list.remove(enemy)
        self.level.board[enemy.y][enemy.x] = enemy.ground_symbol
