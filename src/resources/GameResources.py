from ..LevelSelector import LevelSelector
from .entities.AbstractDungeonEntity import AbstractDungeonEntity
from .entities.character import Character
from .entities.ColorChanger import ColorChanger
from .entities.EnemyManager import EnemyManager


class GameResources:
    """Holds objects that are used for during game runtime"""

    def __init__(self, testing: bool, bless: bool):
        self.level_selector = LevelSelector()

        self.level = self.level_selector.create_level()
        self.player = Character(symbol="$", x=self.level.width // 2, y=self.level.height // 2)

        if bless:
            self.player.start()

        self.test_color_changer = ColorChanger(x=2, y=2, symbol="@")
        self.enemy_manager = EnemyManager(self.level)

        self.enemy_manager.spawn_random_enemies(self.player.x, self.player.y, 2)
        self.testing = testing

    def update_entity(self, entity: AbstractDungeonEntity) -> None:
        """Updates the position of a single entity"""
        x = entity.new_positions["x"]
        y = entity.new_positions["y"]
        try:
            if str(self.level.board[entity.y + y][entity.x + x]) in ("'", "$", "@") or \
                    (entity.__class__.__name__ != 'Enemy' and str(
                        self.level.board[entity.y + y][entity.x + x]) == '#'):
                self.level.board[entity.y][entity.x] = entity.ground_symbol
                if entity.x + x > 0 and entity.y + y > 0:
                    entity.x += x
                    entity.y += y
                else:
                    entity.x -= x
                    entity.y -= y
                entity.ground_symbol = self.level.board[entity.y][entity.x]
                entity.new_positions = {"x": 0, "y": 0}
        except IndexError:
            pass

    def draw_entity(self, entity: AbstractDungeonEntity) -> None:
        """Draws a single entity onto the level"""
        self.level.board[entity.y][entity.x] = entity.symbol

    def update(self, bless: bool) -> None:
        """Updates all game objects"""
        if bless:
            self.player.update()
        else:
            self.player.keyboard_input()

        self.update_entity(self.player)

        # if player walks on door generate new level
        if str(self.level.board[self.player.y][self.player.x]) == "#":
            self.level = self.level_selector.create_level((self.player.y, self.player.x))
            self.player.x = self.level.entrance[1]
            self.player.y = self.level.entrance[0]

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
        if self.enemy_manager.collisions_with_player(self.player.x, self.player.y):
            self.player.playing = False
        else:
            for enemy in self.enemy_manager.enemy_list:
                self.draw_entity(enemy)
            self.draw_entity(self.test_color_changer)

        self.draw_entity(self.player)

    def overlaps(self, first_entity: AbstractDungeonEntity, second_entity: AbstractDungeonEntity) -> bool:
        """Checks if two entities overlap"""
        return first_entity.x == second_entity.x and first_entity.x == second_entity.y
