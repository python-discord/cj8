from pynput.keyboard import Key, Listener

from src.resources.Level import Level

from .AbstractDungeonEntity import AbstractDungeonEntity


class Character(AbstractDungeonEntity):
    """This describes a character"""

    def __init__(self, current_level: Level, symbol: str = "$") -> None:
        super().__init__(
            ground_symbol=current_level.board[current_level.width // 2][
                current_level.height // 2
            ],
            x=current_level.width // 2,
            y=current_level.height // 2,
            symbol=symbol,
            level=current_level
        )
        self.playing = True

    def press(self, key: Key) -> None:
        """Reads keyboard input"""
        try:
            self.level.board[self.y][self.x] = self.ground_symbol
            if key.char == 'a':
                if self.x > 1:
                    self.x -= 1
            if key.char == 'd':
                if self.x < self.level.width - 2:
                    self.x += 1
            if key.char == 'w':
                if self.y > 1:
                    self.y -= 1
            if key.char == 's':
                if self.y < self.level.height - 2:
                    self.y += 1
            self.ground_symbol = self.level.board[self.y][self.x]
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

    def draw(self) -> None:
        """Places player on map"""
        self.level.board[self.y][self.x] = self.symbol
