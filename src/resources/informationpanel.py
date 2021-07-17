from rich.panel import Panel
from rich.text import Text

from src.gameresources import GameResources


class Information:
    """Information panel class"""

    def __init__(self, game_resources: GameResources) -> None:
        self._game_resources = game_resources
        self.enemy_list = game_resources.level.enemies.values()
        self.player = game_resources.player
        self.ENEMY_DEFAULT_PANEL = Panel(Text("No enemies have detected you yet.", style="bold green"))

    def get_player_health(self) -> Panel:
        """Sets panel for player health"""
        health = self.player.health
        hearts = Text(f"{'♥' * (health // 10) if health >= 10 else '♥'}   |   You have: {health}HP", style="bold red")
        health_panel = Panel(hearts, title="Your Health")
        return health_panel

    def display_enemy_panel(self) -> Panel:
        """Sets panel displaying all enemies"""
        self.enemy_list = self._game_resources.level.enemies.values()
        enemy_panel_text = Text("")
        for enemy in self.enemy_list:
            if enemy.player_detected:
                enemy_panel_text += Text(f"Enemy {enemy.file.name} detected you | ", style="bold red")
            else:
                enemy_panel_text += Text(f"Enemy {enemy.file.name} | ")

        enemy_panel = Panel(enemy_panel_text, title="Enemies")
        return enemy_panel
