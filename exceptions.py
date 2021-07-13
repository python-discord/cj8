

class GameTransition(Exception):
    """Base for all exceptions raised to transition between scenes"""


class EnterLevel(GameTransition):
    """Raised when user starts the game"""
    def __init__(self, level: int):
        self.level = level


class LevelSelector(GameTransition):
    """Raised when user goes to the level selector"""


class Title(GameTransition):
    """Raised when user goes to the title screen"""


class Settings(GameTransition):
    """Raised when user goes to settings"""


class Credits(GameTransition):
    """Raised when user goes to credits"""


class ExitGame(Exception):
    """Raised to exit the game"""
