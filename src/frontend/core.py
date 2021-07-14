import datetime
import os
import time
from pathlib import Path
from shutil import get_terminal_size
from typing import List, NoReturn, Optional

from rich.align import Align
from rich.color import Color
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.tree import Tree

from src.backend.core import CoreBackend
from src.backend.events import BaseEvent, EventTypes
from src.backend.mutators import CoreMutators
from src.backend.scoring import CoreScoring
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
        self.scoring: CoreScoring = CoreScoring(self.backend)
        self.mutators = CoreMutators(self.backend)
        self.keyboard_handler: BaseKeyboardHandler = KeyboardFactory.get(self.backend)
        self._paused = False
        self._failed = False

        self.backend.register_hook(self._event_handler)

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

    def _event_handler(self, event: BaseEvent) -> None:
        event_dispatcher = {
            EventTypes.pause.value: self.toggle_pause,
            EventTypes.failed.value: self.game_over,
        }
        event_type = event.type

        if event_type in event_dispatcher:
            event_dispatcher[event_type]()

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
        tree.add(f"Win Count: [i]{self.backend.win_count}")
        tree.add(f"Elapsed: [i]{self.scoring.elapsed_seconds}s")
        tree.add(f"Score: [i]{self.scoring.current_score}")
        tree.add(f"Level High Score: [i]{self.scoring.level_high_score}")
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
        story = tree.add("Story:")
        if story_content := self.story.current_story:
            story.add(f"[i]{story_content}")
        else:
            story.add("🔒 [i]Find story tiles to unlock")
        return Panel(tree)

    @property
    def menu(self) -> Panel:
        """Return main menu panel."""
        return self.create_panel(self._title, self.story.prologue, "Press N to Start.")

    @property
    def end_screen(self) -> Panel:
        """Return game over panel."""
        return self.create_panel(
            self._fail_text, self.story.failed, "Press M to return to Main Menu."
        )

    @property
    def _title(self) -> str:
        """Return title for terminal size"""
        return self._get_static_text(
            ["title_full.txt", "title_small.txt"], default="[b]Panthera's Box"
        )

    @property
    def _fail_text(self) -> str:
        """Return game over text"""
        return self._get_static_text(
            ["failed_full.txt", "failed_small.txt"], default="[b]Game Over"
        )

    def _get_static_text(self, file_names: List[str], default: str = None) -> str:
        width, height = get_terminal_size()
        for file_name in file_names:
            path = Path(__file__).absolute().parent / f"static/{file_name}"
            with open(path, encoding="utf-8") as fd:
                text = fd.read()
                if width >= max([len(line) for line in text.split("\n")]):
                    break
        else:
            text = default
        return text

    def create_panel(self, title: str, body: str, footer: str) -> Panel:
        """Return vertical panel with text"""
        layout = Layout()

        layout.split_column(
            Layout(name="Title"),
            Layout(
                Align(
                    Panel(
                        Text(body, justify="center"),
                        expand=False,
                        padding=(1, 6),
                    ),
                    align="center",
                    vertical="middle",
                )
            ),
            Layout(Align(footer, align="center", vertical="middle")),
        )
        layout["Title"].ratio = 3
        layout["Title"].update(Align(title, align="center", vertical="middle"))

        return Panel(layout)

    def create_layout(self) -> Layout:
        """Create layout object to display."""
        if not self.backend.board:
            self._failed = False
            self._paused = False
            return Layout(self.menu)

        if self._failed:
            return Layout(self.end_screen)

        layout = Layout()
        layout.split_row(
            Layout(name="Display"),
            Layout(self.panel),
        )
        layout["Display"].ratio = 3
        layout["Display"].update(Align(self.display, align="center", vertical="middle"))
        return layout

    def toggle_pause(self) -> None:
        """Toggle the pause state"""
        self._paused = not self._paused

    def game_over(self) -> None:
        """Show the game over screen"""
        self._failed = True
        self._paused = True
