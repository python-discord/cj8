from time import sleep

from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel

from src.fstree.FileStructureTree import FileStructureTree
from src.resources.character import Character
from src.resources.enemy import Enemy
from src.resources.level import Level


def run_game(layout: Layout) -> Panel:
    """
    This function in in charge of running the game. It will call update and draw for each game object.

    Layout: Layout  Holds all the rich renderables for the game. Updated with a new panel each tick.
    """
    player.draw()
    for x in current_node.files:
        globals()[x.name[:-3]].draw()

    panel = Panel(level.to_string())
    layout.update(panel)
    sleep(0.1)


# This a temporary home for these game objects. they should be moved to a better place.
tree = FileStructureTree('.')
current_node = tree.root
level = Level(10, 10, current_node.children, current_node.files)
player = Character(level, "$")
for i in range(len(current_node.files) if len(current_node.files) <= 10 else 10):
    globals()[current_node.files[i].name[:-3]] = Enemy(level, "^")

player.start()

game_panel = Panel(level.to_string())
layout = Layout(game_panel)

with Live(layout, refresh_per_second=10, screen=True):
    while player.playing:
        run_game(layout)
