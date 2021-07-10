from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.text import Text
from rich.panel import Panel
from time import sleep
from threading import Thread
from collections import deque
from blessed import Terminal
import copy
from resources.map import Level
from resources.character import Character


term = Terminal()

def runGame(layout):
    player.draw(level.board)
    panel = Panel(level.to_string(), width=14, height=12)
    layout.update(panel)
    sleep(.1)


level = Level(10, 10)

player = Character(2, 2, '$')

panel = Panel(level.to_string(), width=14, height=12)
layout = Layout(panel)

with Live(layout, refresh_per_second=10, screen=True):
    while True:
        runGame(layout)
