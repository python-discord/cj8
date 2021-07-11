import sys
from abc import ABC

from src.backend.core import CoreBackend


class BaseKeyboardHandler(ABC):
    """
    Base abstract class for handling keyboard inputs

    Subclasses should implement actual concrete keyboard handling for the different OS
    options if we decide to use Keyboard as it requires root to run.

    """

    def __init__(self, backend: CoreBackend):
        self.backend = backend


class DefaultKeyboardHandler(BaseKeyboardHandler):
    """Implements the default handler"""


class KeyboardFactory:
    """
    Called by the frontend module to get a keyboard handler

    Handles sending the correct module depending on OS
    """

    WIN = "win32"
    LINUX = "linux"

    @staticmethod
    def get(backend: CoreBackend) -> BaseKeyboardHandler:
        """
        Returns a concrete Keyboard Handler class

        Implements the factory pattern for returning the correct Keyboard handler
        depending on the OS

        :param backend: CoreBackend object to pass to the keyboard handler
        """
        platform = sys.platform

        if platform == KeyboardFactory.LINUX:
            return None

        # return the default handler
        return DefaultKeyboardHandler(backend)
