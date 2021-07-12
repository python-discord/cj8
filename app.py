from time import sleep

from blessed import Terminal
from rich.live import Live
from rich.panel import Panel

from src.resources.character import Character
from src.resources.level import Level

# Used to get player input
term = Terminal()


def run_game(panel: Panel) -> Panel:
    """
    This function in in charge of running the game. It will call update and draw for each game object.

    Layout: Layout  Holds all the rich rederables for the game. Updated with a new panel each tick.
    """
    player.draw(level.board)
    panel = Panel(level.to_string())
    sleep(0.1)
    return panel


# This a temporary home for these game objects. they should be moved to a better place.
level = Level(11, 10, [1, 2, 3, 4], [])
player = Character(2, 2, "$")

game_panel = Panel(level.to_string())

with Live(game_panel, refresh_per_second=10, screen=True):
    while True:
        run_game(game_panel)
