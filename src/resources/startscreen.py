from time import sleep

from pynput.keyboard import Key, Listener
from rich.panel import Panel
from rich.progress import Progress
from rich.text import Text

from .PanelLayout import PanelLayout


class StartScreen:
    """Start screen of game"""

    def __init__(self) -> None:
        self.layout = PanelLayout.make_layout(start=True)
        self.guide = False
        self.in_start = True

    def press(self, key: Key) -> None:
        """Reads keyboard input"""
        try:
            if key.char == 'h':
                self.guide = True
            if key.char == 'b' and self.guide is True:
                self.guide = False
            if key.char == 's':
                self.in_start = False
        except AttributeError:
            self.in_start = False

    def release(self, key: Key) -> bool:
        """On key release"""
        return False

    def keyboard_input(self) -> None:
        """Uses listener that reads keyboard input from press"""
        with Listener(on_press=self.press, on_release=self.release) as listener:  # set keys to be read immediately
            listener.join()

    def display_screen(self) -> Panel:
        """Display default start screen"""
        with open("start_screen_display.txt", "r") as file:
            screen_panel = Panel(Text(''.join(file.readlines()), style="bold white", justify="full"))

        return screen_panel

    def display_guide(self) -> Panel:
        """Display 'how to play' screen; displays guide screen"""
        with open("guide.txt", "r") as file:
            guide_panel = Panel(Text(''.join(file.readlines()), style="bold green", justify="full"))

        return guide_panel

    def loading_bar(self) -> None:
        """Sets loading bar"""
        with Progress() as progress:
            task1 = progress.add_task("[bold blue] Configuring levels...", total=500)
            task2 = progress.add_task("[bold green] Configuring player...", total=500)
            task3 = progress.add_task("[bold red] Configuring enemies...", total=500)

            while not progress.finished:
                progress.update(task1, advance=1.7)
                progress.update(task2, advance=2)
                progress.update(task3, advance=1.8)
                sleep(0.01)
