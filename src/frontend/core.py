import time
from shutil import get_terminal_size

from rich.color import Color
from rich.live import Live
from rich.table import Table

from src.backend.core import CoreBackend
from src.frontend.keyboard_handlers import BaseKeyboardHandler, KeyboardFactory


class CoreFrontend:
    """
    Frontend module

    Responsible for rendering the game state to the terminal

    Should query the backend module for an update each loop cycle as well as passing
    on any keyboard presses that were registered.

    Should draw the 'illuminated' circle of vision around the ball by querying the
    backend for all of the objects within a certain distance from the ball.

    Should draw out the current active mutators as well and the current score.
    """

    FPS = 12
    MIN_WIDTH = 75
    MIN_HEIGHT = 40

    def __init__(self):
        self.backend: CoreBackend = CoreBackend()
        self.keyboard_handler: BaseKeyboardHandler = KeyboardFactory.get(self.backend)

    def start_loop(self) -> None:
        """Start the render loop"""
        width, height = get_terminal_size()
        while width < self.MIN_WIDTH or height < self.MIN_HEIGHT:
            print(f"Your terminal must be {self.MIN_WIDTH}x{self.MIN_HEIGHT}", end="\r")
            width, height = get_terminal_size()
        with Live(
            self.get_display(), screen=True, transient=True, refresh_per_second=self.FPS
        ) as live:
            while True:
                time.sleep(1 / self.FPS)
                self.backend.move_ball()
                live.update(self.get_display())

    def get_display(self) -> Table:
        """Return Table grid for display."""
        table = Table.grid()
        all_tiles = self.backend.get_board()
        for row in all_tiles:
            table.add_row(
                *[f"[{Color.from_rgb(*tile.color).name}]{tile}" for tile in row]
            )
        return table


if __name__ == "__main__":
    frontend = CoreFrontend()
    frontend.backend.new_level()
    frontend.start_loop()
