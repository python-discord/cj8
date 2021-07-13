from threading import Thread

from blessed import Terminal

from src.resources.Level import Level

from .AbstractDungeonEntity import AbstractDungeonEntity

# Used to get player input
term = Terminal()


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

    def start(self) -> None:
        """Starts the movement controls in a separate thread"""
        Thread(target=self.keyboard_input, args=()).start()

    def keyboard_input(self) -> None:
        """Reads keyboard input and moves the player"""
        on = True
        while on:
            with term.cbreak():  # set keys to be read immediately
                inp = term.inkey()  # wait and read one character
                self.level.board[self.y][self.x] = self.ground_symbol
                if inp == "a":
                    if self.x > 1:
                        self.x -= 1
                if inp == "d":
                    if self.x < self.level.width - 2:
                        self.x += 1
                if inp == "w":
                    if self.y > 1:
                        self.y -= 1
                if inp == "s":
                    if self.y < self.level.height - 2:
                        self.y += 1
                if inp == "p":
                    on = False
                    self.playing = False
                self.ground_symbol = self.level.board[self.y][self.x]

    def draw(self) -> None:
        """Places player on map"""
        self.level.board[self.y][self.x] = self.symbol
