from .entities.character import Character
from .entities.ColorChanger import ColorChanger
from .entities.Enemy import Enemy
from .entities.EnemyManager import EnemyManager
from .Level import Level


class GameResources:
    """holds objects that are used for during game runtime"""

    def __init__(self):
        self.level = Level(15, 10, [1, 2, 3, 4], [])
        self.player = Character(self.level, "$")
        self.test_enemy = Enemy(self.level)
        self.test_color_changer = ColorChanger(level=self.level, x=2, y=2, symbol="@", color="orange")
        self.enemy_manager = EnemyManager(self.level)
        self.enemy_manager.spawn_random_enemies(6)

    def draw(self) -> None:
        """
        Function to draw eneties in game resources class.

        The last drawn entites will appear on top of ones before it.
        """
        self.enemy_manager.draw()
        self.test_color_changer.draw()
        self.player.draw()
