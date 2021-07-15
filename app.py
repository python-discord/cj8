import sys
from time import sleep

from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.text import Text

from src.resources.GameResources import GameResources
from src.resources.PanelLayout import PanelLayout


def end_screen(layout: Layout) -> None:
    """Displays game over screen"""
    with open('ascii.txt', 'r') as file:
        panel = Panel(Text(''.join(file.readlines()), style="bold red", justify='full'))
        layout["main_game"].update(panel)
        sleep(3)


def run_game(layout: Layout, game_resources: GameResources) -> Panel:
    """
    This function in in charge of running the game. It will call update and draw for each game object.

    Layout: Layout  Holds all the rich renderables for the game. Updated with a new panel each tick.
    """
    game_resources.update(bless)
    game_resources.draw()

    panel = Panel(game_resources.level.to_string())

    # Panels to update
    layout["main_game"].update(panel)
    layout["footer"].update(Panel('footer'))
    layout["tree"].update(Panel('tree'))
    sleep(0.1)


def main() -> None:
    """Main function that sets up game and runs main game loop"""
    game_resources = GameResources(testing, bless)
    game_resources.draw()

    game_panel = Panel(game_resources.level.to_string())
    layout = PanelLayout.make_layout()
    layout["main_game"].update(game_panel)

    # Panels to update
    layout["footer"].update(Panel('footer'))
    layout["tree"].update(Panel('tree'))

    with Live(layout, refresh_per_second=10, screen=True):
        while game_resources.player.playing:
            run_game(layout, game_resources)
        end_screen(layout)


testing = False
bless = False
if __name__ == "__main__":
    if sys.argv[-1] == "--test":
        testing = True
    elif sys.argv[-1] == "--bless":
        bless = True
    main()
