from rich.panel import Panel
from rich.text import Text

from src.GameResources import GameResources


class Information:
    """Information panel class"""

    def __init__(self, game_resources: GameResources) -> None:
        self.enemy_list = game_resources.level.enemies.values()
        self.player = game_resources.player
        self.enemy_default_panel = Panel(Text("No enemies have detected you yet.", style="bold green"))

    def get_player_health(self) -> Panel:
        """Sets panel for player health"""
        health = self.player.health
        hearts = Text(f"{'♥' * (health // 10) if health >= 10 else '♥'}   |   You have: {health}HP", style="bold red")
        health_panel = Panel(hearts, title="Your Health")
        return health_panel
