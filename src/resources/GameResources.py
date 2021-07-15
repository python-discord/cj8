from .entities.AbstractDungeonEntity import AbstractDungeonEntity
from .entities.character import Character
from .entities.ColorChanger import ColorChanger
from .entities.EnemyManager import EnemyManager
from .entities.level.Level import Level


class GameResources:
    """Holds objects that are used for during game runtime"""

    def __init__(self, testing: bool):
        self.level = Level(20, 15, [1, 2, 3, 4], [])
        self.player = Character(symbol="$", x=self.level.width // 2, y=self.level.height // 2)
        self.test_color_changer = ColorChanger(x=2, y=2, symbol="@")
        self.enemy_manager = EnemyManager(self.level)
        self.enemy_manager.spawn_random_enemies(self.player.x, self.player.y, 6)
        self.testing = testing

    def update_entity(self, entity: AbstractDungeonEntity) -> None:
        """Updates the position of a single entity"""
        x = entity.new_positions["x"]
        y = entity.new_positions["y"]
        try:
            if str(self.level.board[entity.y + y][entity.x + x]) in ("'", "@", "$"):
                self.level.board[entity.y][entity.x] = entity.ground_symbol
                entity.x += x
                entity.y += y
                entity.ground_symbol = self.level.board[entity.y][entity.x]
                entity.new_positions = {"x": 0, "y": 0}
        except IndexError:
            pass

    def draw_entity(self, entity: AbstractDungeonEntity) -> None:
        """Draws a single entity onto the level"""
        self.level.board[entity.y][entity.x] = entity.symbol

    def update(self) -> None:
        """Updates all game objects"""
        self.player.keyboard_input()
        self.update_entity(self.player)

        # self.enemy_manager.update(self.player.x, self.player.y)

        for enemy in self.enemy_manager.enemy_list:
            if enemy.is_in_radius(self.player.x, self.player.y):
                enemy.follow(self.testing)
            else:
                enemy.mill()

            self.update_entity(enemy)

        if self.test_color_changer.collisions_with_player(self.player.x, self.player.y):
            self.test_color_changer.change_color(self.player)

    def draw(self) -> bool:
        """
        Function to draw entities in game resources class.

        The last drawn entities will appear on top of ones before it.
        """
        self.draw_entity(self.player)

        if self.enemy_manager.collisions_with_player(self.player.x, self.player.y):
            self.player.playing = False
            return False
        else:
            for enemy in self.enemy_manager.enemy_list:
                self.draw_entity(enemy)
            self.draw_entity(self.test_color_changer)
            return True
