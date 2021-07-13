from .entities.character import Character
from .entities.enemy import Enemy
from .level import Level


class GameResources:
    """holds objects that are used for during game runtime"""

    def __init__(self):
        self.level = Level(10, 10, [1, 2, 3, 4], [])
        self.player = Character(self.level, "$")
        self.player.start()
        self.test_enemy = Enemy(self.level)

    def draw(self) -> None:
        """
        Function to draw eneties in game resources class.

        The last drawn entites will appear on top of ones before it.
        """
        self.test_enemy.draw()
        self.player.draw()
