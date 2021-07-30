import sys
from os import path as ospath
from time import sleep

from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.text import Text

from src.gameresources import GameResources
from src.resources.informationpanel import Information
from src.resources.panellayout import PanelLayout
from src.resources.startscreen import StartScreen


def start_screen() -> None:
    """Start screen of the game, has a guide of how to play"""
    screen = StartScreen()
    layout_screen = screen.layout
    layout_screen.update(
        screen.display_screen()
    )

    with Live(layout_screen, refresh_per_second=10, screen=True):
        while screen.in_start:
            screen.keyboard_input()
            # start screen
            if screen.guide is True:
                layout_screen.update(
                    screen.display_guide()
                )
            else:
                layout_screen.update(
                    screen.display_screen()
                )

    # loading bar once 's' is pressed
    screen.loading_bar()


def end_screen(layout: Layout) -> None:
    """Displays game over screen"""
    with open('ascii.txt', 'r') as file:
        panel = Panel(Text(''.join(file.readlines()), style="bold red", justify='full'))
        layout["main_game"].update(panel)
        sleep(3)


def run_game(layout: Layout, game_resources: GameResources, information: Information) -> Panel:
    """
    This function in in charge of running the game. It will call update and draw for each game object.

    Layout: Layout  Holds all the rich renderables for the game. Updated with a new panel each tick.
    """
    game_resources.update(bless)
    game_resources.draw()

    panel = Panel(game_resources.level.to_string())
    # Panels to update
    layout["main_game"].update(panel)
    layout["tree"].update(
        Panel(game_resources.node.display_node(), title="Map")
    )

    if game_resources.won_game:
        layout["tree"].update(
            Panel("You have reached the bottom")
        )

    inventory = Text("\n".join("{} X {}".format(k, v)for k, v in game_resources.collected_items.items()))
    layout["inventory"].update(Panel(inventory, title="Inventory"))
    layout["player_health"].update(information.get_player_health())
    layout['info'].update(information.display_enemy_panel())


def win_screen(layout: Layout) -> None:
    """Win screen when the player wins"""
    with open('winscreen.txt', 'r') as file:
        panel = Panel(Text(''.join(file.readlines()), style="bold green", justify='full'))
        layout.update(panel)


def main() -> None:
    """Main function that sets up game and runs main game loop"""
    game_resources = GameResources(testing, bless, path)
    information = Information(game_resources)
    game_resources.draw()

    game_panel = Panel(game_resources.level.to_string())
    layout = PanelLayout.make_layout(start=False)
    layout["main_game"].update(game_panel)

    # Panels to update
    layout["tree"].update(
        Panel(game_resources.node.display_node(), title="Map")
    )
    layout['inventory'].update(Panel('', title="Inventory"))
    layout['info'].update(information.display_enemy_panel())
    layout["player_health"].update(
        (Panel(Text('♥'*10 + "   |   You have: 100HP", style="bold red"), title='Health')))

    start_screen()

    with Live(layout, refresh_per_second=10, screen=False):  # True prevents re-render
        while game_resources.player.playing:
            run_game(layout, game_resources, information)
            if game_resources.won_game:
                game_resources.player.playing = False

        if not game_resources.won_game:
            end_screen(layout)

    if game_resources.won_game:
        layout = Layout(name="win")
        with Live(layout, refresh_per_second=1, screen=False):
            win_screen(layout)


testing = False
bless = False
path = "."
if __name__ == "__main__":
    testing = "--test" in sys.argv
    bless = "--bless" in sys.argv

    try:
        for i, arg in enumerate(sys.argv):
            if "--path" in arg:
                target = sys.argv[i + 1]
                path = target if ospath.isdir(target) else "."
                break
    except Exception:
        path = "."

    main()
