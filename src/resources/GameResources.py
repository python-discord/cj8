from .entities.AbstractDungeonEntity import AbstractDungeonEntity
from .entities.character import Character
from .entities.ColorChanger import ColorChanger
from .entities.EnemyManager import EnemyManager
from .entities.level.Level import Level


class GameResources:
    """Holds objects that are used for during game runtime"""

    def __init__(self):
        self.level = Level(10, 10, [1, 2, 3, 4], [])
        self.player = Character(symbol="$", x=self.level.width // 2, y=self.level.height // 2)
        self.test_color_changer = ColorChanger(x=2, y=2, symbol="@", color="orange")
        self.enemy_manager = EnemyManager(self.level)
        self.enemy_manager.spawn_random_enemies(self.player.x, self.player.y, 0)

    def update_entity(self, entity: AbstractDungeonEntity) -> None:
        """Updates the position of a single entity"""
        x = entity.new_positions["x"]
        y = entity.new_positions["y"]
        try:
            if self.level.board[entity.y + y][entity.x + x].entity_type == "tile":
                self.level.board[entity.y][entity.x] = entity.ground_symbol
                entity.x += x
                entity.y += y
                entity.ground_symbol = self.level.board[entity.y][entity.x]
                entity.new_positions = {"x": 0, "y": 0}
        except AttributeError:
            pass

    def draw_entity(self, entity: AbstractDungeonEntity) -> None:
        """Draws a single entity onto the level"""
        self.level.board[entity.y][entity.x] = entity.symbol

    def update(self) -> None:
        """Updates all game objects"""
        self.player.keyboard_input()
        self.update_entity(self.player)

        self.enemy_manager.update(self.player.x, self.player.y)

        # TODO use this instead of enmey manager draw
        # for enemy in self.enemy_manager.enemy_list:
        #     self.update_entity(enemy)
        #     enemy.check collision -> pass this enemy and player position
        #     if enemy.checktarger is not None
        #          based on this mill or follow

        # color changer
        #   if collides with player -> compare color change pos and player position
        #      change player color

    def draw(self) -> bool:
        """
        Function to draw entities in game resources class.

        The last drawn entities will appear on top of ones before it.
        """
        self.draw_entity(self.player)

        if self.enemy_manager.collisions_with_player(self.player.x, self.player.y):
            self.player.playing = False
        else:
            for enemy in self.enemy_manager.enemy_list:
                self.draw_entity(enemy)
            self.draw_entity(self.test_color_changer)
            return True
