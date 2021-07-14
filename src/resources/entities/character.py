from pynput.keyboard import Key, Listener

from .AbstractDungeonEntity import AbstractDungeonEntity


class Character(AbstractDungeonEntity):
    """This describes a character"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.playing = True

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
