

class GameTransition(Exception):
    """Base for all exceptions raised to transition between scenes"""


class EnterLevel(GameTransition):
    """Raised when user starts the game"""
    max_level = 0

    def __init__(self, level: int):
        self.level = level
        EnterLevel.max_level = max(self.level, EnterLevel.max_level)


class WinGame(GameTransition):
    """Raised when user beats the game"""
    won = False

    def __init__(self):
        WinGame.won = True


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
