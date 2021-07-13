import os
import time
from shutil import get_terminal_size

from rich.align import Align
from rich.color import Color
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.tree import Tree

from src.backend.core import CoreBackend
from src.backend.events import BaseEvent
from src.keyboard_handlers.core import BaseKeyboardHandler, KeyboardFactory


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
        self._paused = False

        self.backend.register_hook(self.toggle_pause)

    def start_loop(self) -> None:
        """Start the render loop"""
        self._check_terminal_size()
        with Live(
            self.create_layout(),
            screen=True,
            transient=True,
            refresh_per_second=self.FPS,
        ) as live:
            while True:
                if not self._paused:
                    self.backend.move_ball()
                live.update(self.create_layout())
                time.sleep(1 / self.FPS)

    def _check_terminal_size(self) -> None:
        BYPASS = os.environ.get("BYPASS_SIZE_CHECK", "False") == "True"

        if not BYPASS:
            width, height = get_terminal_size()
            while width < self.MIN_WIDTH or height < self.MIN_HEIGHT:
                print(
                    f"Your terminal must be {self.MIN_WIDTH}x{self.MIN_HEIGHT}",
                    end="\r",
                )
                width, height = get_terminal_size()

    @property
    def display(self) -> Table:
        """Return Table grid representing the game board."""
        table = Table.grid()
        all_tiles = self.backend.get_board()
        for row in all_tiles:
            table.add_row(
                *[f"[{Color.from_rgb(*tile.color).name}]{tile}" for tile in row]
            )
        return table

    @property
    def panel(self) -> Panel:
        """Return informational panel about current game."""
        tree = Tree("[b]Panthera's Box")
        tree.add(f"Level: [i]{self.backend._board.level_name}")
        tree.add(f"Score: [i]{self.backend.win_count}")
        mutators = tree.add("Mutators:")
        for mutator, state in self.backend.mutators.items():
            if state:
                mutators.add(f"[i]{mutator}")
        if not mutators.children:
            mutators.add("[i]None")
        controls = tree.add("Controls:")
        for keys, color in self.backend._controls.items():
            if color:
                k1, k2 = [key.upper() for key in keys]
                controls.add(f"{k1} <[{Color.from_rgb(*color).name}]↑[/]> {k2}")
        return Panel(tree)

    def create_layout(self) -> Layout:
        """Create layout object to display."""
        layout = Layout()
        layout.split_row(
            Layout(name="Display"),
            Layout(self.panel),
        )
        layout["Display"].ratio = 3
        layout["Display"].update(Align(self.display, align="center", vertical="middle"))
        return layout

    def toggle_pause(self, event: BaseEvent) -> None:
        """Handle only pause events"""
        if event.type == "pause":
            self._paused = not self._paused


if __name__ == "__main__":
    frontend = CoreFrontend()
    frontend.backend.new_level()
    frontend.start_loop()
