from .fstree.FileStructureTree import FileStructureTree
from .LevelSelector import LevelSelector
from .resources.entities.AbstractDungeonEntity import AbstractDungeonEntity
from .resources.entities.character import Character
from .resources.entities.ColorChanger import ColorChanger
from .resources.entities.EnemyManager import EnemyManager
from .resources.entities.Item import Item


class GameResources:
    """Holds objects that are used for during game runtime"""

    def __init__(self, testing: bool, bless: bool):
        self.tree = FileStructureTree('.')
        self.node = self.tree.root
        self.level_selector = LevelSelector(self.tree)

        self.level = self.level_selector.create_level()
        self.won_game = False
        self.player = Character(symbol="$", x=self.level.width // 2, y=self.level.height // 2, color="bold white")

        if bless:
            self.player.start()

        self.test_color_changer = ColorChanger(x=2, y=2, symbol="@")
        self.test_item = Item(symbol='k', x=self.level.width // 2+1, y=self.level.height // 2+1)
        self.collected_items = []

        self.enemy_manager = EnemyManager(self.level)
        self.enemy_manager.spawn_random_enemies(self.player.x, self.player.y, 5)
        self.testing = testing

    def update(self, bless: bool) -> None:
        """Updates all game objects"""
        self.update_player(bless)
        self.enter_door_check()
        self.won_game = self.level.cur_node.depth == self.tree.depth

        self.update_enemies()
        self.update_color_changer()
        self.update_items()

    def draw(self) -> bool:
        """
        Function to draw entities in game resources class.

        The last drawn entities will appear on top of ones before it.
        """
        self.draw_enemies()
        self.draw_color_changers()
        self.draw_items()
        self.draw_entity(self.player)

    def update_player(self, bless: bool) -> None:
        """Gets players position and updates location"""
        if self.player.health <= 0:
            self.player.playing = False
        if bless:
            self.player.update()
        else:
            self.player.keyboard_input()
        self.update_entity(self.player)

    def enter_door_check(self) -> None:
        """If player walks on door generate new level or return existing level"""
        if str(self.level.board[self.player.y][self.player.x]) == "#":
            self.level = self.level_selector.create_level((self.player.y, self.player.x))
            # self.level_selector.cur is used for storing the current node,
            # which would be the current level that the game is working off of
            self.node = self.level_selector.cur
            self.player.x = self.level.entrance[1]
            self.player.y = self.level.entrance[0]

    def update_enemies(self) -> None:
        """
        Iterates through all the enemies and calls their updates and changes their position

        Checks if enemies collide with player end game.
        """
        for enemy in self.enemy_manager.enemy_list:
            if enemy.is_in_radius(self.player.x, self.player.y):
                if self.player.color == "bold white":
                    enemy.follow(self.testing)
                elif enemy > self.player:
                    enemy.follow(self.testing)
                elif enemy < self.player:
                    enemy.flee(self.testing)
                else:
                    enemy.mill()
            else:
                enemy.mill()

            if not self.is_adjacent(enemy, self.player):
                self.update_entity(enemy)

            if self.is_adjacent(self.player, enemy):
                result = self.get_combat_result(self.player, enemy)
                if result == "win":
                    self.enemy_manager.remove_enemy(enemy)
                elif result == "loose":
                    self.player.health -= 10
                else:
                    pass

    def update_color_changer(self) -> None:
        """Checks all the color changers, if the player is on that spot change player color"""
        for color_changer in self.level.color_changers:
            overlapping = self.overlaps(color_changer, self.player)
            if overlapping:
                self.player.color = color_changer.color
                self.player.symbol.stylize(color_changer.color)

    def update_items(self) -> None:
        """Iterates through items and check if the player is on that spot. If so collects them."""
        for item in self.level.items:
            if item.collisions_with_player(self.player.x, self.player.y):
                self.collected_items.append(item.symbol._text[0])
                self.level.remove_item(item)

    def draw_enemies(self) -> None:
        """Iterates through enemies and draws them"""
        for enemy in self.enemy_manager.enemy_list:
            self.draw_entity(enemy)

    def draw_color_changers(self) -> None:
        """Iterates through color changers and draws them"""
        for color_changer in self.level.color_changers:
            self.draw_entity(color_changer)

    def draw_items(self) -> None:
        """Iterates through items and draws them"""
        for item in self.level.items:
            self.draw_entity(item)

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
            if str(self.level.board[entity.y + y][entity.x + x]) in ("k"):
                self.level.board[entity.y][entity.x] = entity.ground_symbol
                entity.x += x
                entity.y += y
                entity.new_positions = {"x": 0, "y": 0}

        except IndexError:
            pass

    def draw_entity(self, entity: AbstractDungeonEntity) -> None:
        """Draws a single entity onto the level"""
        self.level.board[entity.y][entity.x] = entity.symbol

    def is_adjacent(self, first_entity: AbstractDungeonEntity, second_entity: AbstractDungeonEntity) -> bool:
        """Returns true if player is next to enemy"""
        if first_entity.x + 1 == second_entity.x and first_entity.y == second_entity.y:
            return True
        if first_entity.x - 1 == second_entity.x and first_entity.y == second_entity.y:
            return True
        if first_entity.y + 1 == second_entity.y and first_entity.x == second_entity.x:
            return True
        if first_entity.y - 1 == second_entity.y and first_entity.x == second_entity.x:
            return True
        return False

    def overlaps(self, first_entity: AbstractDungeonEntity, second_entity: AbstractDungeonEntity) -> bool:
        """Checks if two entities overlap"""
        return (first_entity.y, first_entity.x) == (second_entity.y, second_entity.x)

    def get_combat_result(self, player: Character, enemy: AbstractDungeonEntity) -> str:
        """Checks if player collided with enemy, returns losing object"""
        if enemy < player:
            return "win"
        elif enemy > player or player.color == "bold white":
            return "loose"
        return 'draw'
