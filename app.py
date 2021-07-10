from time import sleep

from blessed import Terminal
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel

from src.resources.character import Character
from src.resources.map import Level

# Used to get player input
term = Terminal()


def run_game(layout: Layout) -> None:
    """
    This function in in charge of running the game. It will call update and draw for each game object.

    Layout: Layout  Holds all the rich rederables for the game. Updated with a new panel each tick.
    """
    player.draw(level.board)
    panel = Panel(level.to_string(), width=14, height=12)
    layout.update(panel)
    sleep(0.1)


# This a temporary home for these game objects. they should be moved to a better place.
level = Level(10, 10)
player = Character(2, 2, "$")

panel = Panel(level.to_string(), width=14, height=12)
main_layout = Layout(panel)

with Live(main_layout, refresh_per_second=10, screen=True):
    while True:
        run_game(main_layout)
