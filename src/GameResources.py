from .fstree.FileStructureTree import FileStructureTree
from .LevelSelector import LevelSelector
from .resources.entities.AbstractDungeonEntity import AbstractDungeonEntity
from .resources.entities.character import Character
from .resources.entities.EnemyManager import EnemyManager


class GameResources:
    """Holds objects that are used for during game runtime"""

    def __init__(self, testing: bool, bless: bool):
        self.tree = FileStructureTree('.')
        self.node = self.tree.root
        self.level_selector = LevelSelector(self.tree)

        self.level = self.level_selector.create_level()
        self.player = Character(symbol="$", x=self.level.width // 2, y=self.level.height // 2, color="bold white")

        if bless:
            self.player.start()

        self.enemy_manager = EnemyManager(self.level)

        self.enemy_manager.spawn_random_enemies(self.player.x, self.player.y, 0)
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
                if entity.entity_type == "enemy":
                    if entity.x + x > 0 and entity.y + y > 0:
                        entity.x += x
                        entity.y += y
                    else:
                        entity.x -= x
                        entity.y -= y
                else:
                    entity.x += x
                    entity.y += y
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
            # self.level_selector.cur is used for storing the current node,
            # which would be the current level that the game is working off of
            self.node = self.level_selector.cur
            self.player.x = self.level.entrance[1]
            self.player.y = self.level.entrance[0]

        for enemy in self.enemy_manager.enemy_list:
            if enemy.is_in_radius(self.player.x, self.player.y):
                enemy.follow(self.testing)
            else:
                enemy.mill()

            self.update_entity(enemy)

        for color_changer in self.level.color_changers:
            overlapping = self.overlaps(color_changer, self.player)
            if overlapping:
                self.player.symbol.stylize(color_changer.color)

    def draw(self) -> bool:
        """
        Function to draw entities in game resources class.

        The last drawn entities will appear on top of ones before it.
        """
        self.draw_entity(self.player)

        result = self.enemy_manager.collisions_with_player(self.player)
        if isinstance(result, Character):
            self.player.playing = False
            return False

        else:
            if str(result) != 'draw':
                self.enemy_manager.remove_enemy(result)
            for enemy in self.enemy_manager.enemy_list:
                self.draw_entity(enemy)
            for color_changer in self.level.color_changers:
                self.draw_entity(color_changer)

        self.draw_entity(self.player)

    def overlaps(self, first_entity: AbstractDungeonEntity, second_entity: AbstractDungeonEntity) -> bool:
        """Checks if two entities overlap"""
        return (first_entity.y, first_entity.x) == (second_entity.y, second_entity.x)
