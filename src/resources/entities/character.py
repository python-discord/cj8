from collections import deque
from threading import Thread

from blessed import Terminal
from pynput.keyboard import Key, Listener

from .abstractdungeonentity import AbstractDungeonEntity

term = Terminal()


class Character(AbstractDungeonEntity):
    """This describes a character"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ENTITY_TYPE = "character"
        self.playing = True
        self.commands = deque()
        self.health = 100

    def press(self, key: Key) -> None:
        """Reads keyboard input"""
        self.new_positions = {"x": 0, "y": 0}

        try:
            if key.char == 'a':
                self.new_positions["x"] = -1
            if key.char == 'd':
                self.new_positions["x"] = 1
            if key.char == 'w':
                self.new_positions["y"] = -1
            if key.char == 's':
                self.new_positions["y"] = 1
        except AttributeError:
            self.playing = False

    def release(self, key: Key) -> bool:
        """On key release"""
        try:
            if key.char == 'p':
                self.playing = False
        except AttributeError:
            pass
        return False

    def keyboard_input(self) -> None:
        """Uses listener that reads keyboard input from press"""
        with Listener(on_press=self.press, on_release=self.release) as listener:  # set keys to be read immediately
            listener.join()

    def move(self, direction: str) -> None:
        """Move player"""
        if direction == 'a':
            self.new_positions["x"] = -1
        if direction == 'd':
            self.new_positions["x"] = 1
        if direction == 'w':
            self.new_positions["y"] = -1
        if direction == 's':
            self.new_positions["y"] = 1
        if direction == 'p':
            self.playing = False

    def start(self) -> None:
        """Start thread"""
        Thread(target=self.control, args=()).start()

    def control(self) -> None:
        """Get keyboard controls"""
        while self.playing:
            with term.cbreak():  # set keys to be read immediately
                inp = term.inkey()  # wait and read one character
                self.commands.append(inp)

    def update(self) -> None:
        """Turn based update"""
        command = ""
        while len(command) == 0:
            if len(self.commands) > 0:
                command = (self.commands.pop())
                self.move(command)
