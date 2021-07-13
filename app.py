from time import sleep

from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel

from src.resources.GameResources import GameResources


def run_game(layout: Layout, game_resources: GameResources) -> Panel:
    """
    This function in in charge of running the game. It will call update and draw for each game object.

    Layout: Layout  Holds all the rich renderables for the game. Updated with a new panel each tick.
    """
    game_resources.player.keyboard_input()
    game_resources.draw()
    panel = Panel(game_resources.level.to_string())
    layout.update(panel)
    sleep(0.1)


def main() -> None:
    """Main function that sets up game and runs main game loop"""
    game_resources = GameResources()
    game_panel = Panel(game_resources.level.to_string())
    layout = Layout(game_panel)

    with Live(layout, refresh_per_second=10, screen=True):
        while game_resources.player.playing:
            run_game(layout, game_resources)


if __name__ == "__main__":
    main()
