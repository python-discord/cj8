import datetime
import os
import time
from pathlib import Path
from shutil import get_terminal_size
from typing import NoReturn, Optional

from rich.align import Align
from rich.color import Color
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.tree import Tree

from src.backend.core import CoreBackend
from src.backend.events import BaseEvent
from src.backend.mutators import CoreMutators
from src.backend.tiles import PauseTile
from src.keyboard_handlers.core import BaseKeyboardHandler, KeyboardFactory
from src.sounds.core import CoreSounds
from src.story.core import CoreStory


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

    FPS = 20
    MIN_WIDTH = 75
    MIN_HEIGHT = 40

    def __init__(self):
        self.backend: CoreBackend = CoreBackend()
        self.story: CoreStory = CoreStory(self.backend)
        self.sound: CoreSounds = CoreSounds(self.backend)
        self.mutators = CoreMutators(self.backend)
        self.keyboard_handler: BaseKeyboardHandler = KeyboardFactory.get(self.backend)
        self._paused = False

        self.backend.register_hook(self.toggle_pause)

    def start_loop(self) -> NoReturn:
        """Start the render loop"""
        self._check_terminal_size()
        current_frame: Optional[datetime.datetime] = datetime.datetime.now()
        frame_delta = datetime.timedelta(
            milliseconds=(1 / self.FPS) * 1000
        ).microseconds
        with Live(
            self.create_layout(),
            screen=True,
            transient=True,
            refresh_per_second=self.FPS,
        ) as live:

            while True:
                now = datetime.datetime.now()
                delta = (now - current_frame).microseconds
                sleep_period = (frame_delta - delta) / 1_000_000
                if not self._paused:
                    self.backend.tick()
                live.update(self.create_layout())
                current_frame = now
                # Add sleep only if frame was rendered faster than expected
                if sleep_period > 0:
                    time.sleep(sleep_period)

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
        if self._paused:
            center_row = len(all_tiles) // 2
            all_tiles[center_row] = [
                PauseTile(pos=(tile.pos.x, center_row))
                if tile.pos.x == len(all_tiles[center_row]) // 2
                else tile
                for tile in all_tiles[center_row]
            ]
        for row in all_tiles:
            table.add_row(
                *[f"[{Color.from_rgb(*tile.color).name}]{tile}" for tile in row]
            )
        return table

    @property
    def panel(self) -> Panel:
        """Return informational panel about current game."""
        tree = Tree("[b]Panthera's Box")
        tree.add(f"Level: [i]{self.backend.board.level_name}")
        tree.add(f"Score: [i]{self.backend.win_count}")
        mutators = tree.add("Mutators:")
        for mutator in self.mutators.active_mutators:
            mutators.add(f"[i]{mutator}")
        if not mutators.children:
            mutators.add("[i]None")
        controls = tree.add("Controls:")
        for keys, color in self.backend._controls.items():
            if color:
                k1, k2 = [key.upper() for key in keys]
                controls.add(f"{k1} <[{Color.from_rgb(*color).name}]↑[/]> {k2}")
        for key, handler in self.backend._controls_aux.items():
            controls.add(f"{key.upper()}: [i]{handler.description}")
        return Panel(tree)

    @property
    def menu(self) -> Panel:
        """Return main menu panel."""
        layout = Layout()

        title = self._get_title()

        layout.split_column(
            Layout(name="Title"),
            Layout(
                Align(
                    Panel(
                        Text(self.story.prologue, justify="center"),
                        expand=False,
                        padding=(1, 6),
                    ),
                    align="center",
                    vertical="middle",
                )
            ),
            Layout(Align("Press N to Start.", align="center", vertical="middle")),
        )
        layout["Title"].ratio = 3
        layout["Title"].update(Align(title, align="center", vertical="middle"))

        return Panel(layout)

    def _get_title(self) -> str:
        width, height = get_terminal_size()
        title = "[b]Panthera's Box"
        title_files = ["title_full.txt", "title_small.txt"]
        for title_file in title_files:
            path = Path(__file__).absolute().parent / f"static/{title_file}"
            with open(path, encoding="utf-8") as fd:
                title = fd.read()
                if width >= max([len(line) for line in title.split("\n")]):
                    break
        return title

    def create_layout(self) -> Layout:
        """Create layout object to display."""
        if not self.backend.board:
            return Layout(self.menu)
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
