import sys
from abc import ABC

import keyboard
from keyboard import KeyboardEvent

from src.backend.core import CoreBackend


class BaseKeyboardHandler(ABC):
    """
    Base abstract class for handling keyboard inputs

    Subclasses should implement actual concrete keyboard handling for the different OS
    options if we decide to use Keyboard as it requires root to run.
    """

    def __init__(self, backend: CoreBackend):
        self.backend = backend

    def key_pressed(self, key: str) -> None:
        """Pass on the key press to the backend module"""
        self.backend.key_press(key)


class DefaultKeyboardHandler(BaseKeyboardHandler):
    """Implements the default handler"""

    def __init__(self, backend: CoreBackend):
        super().__init__(backend)

        self.keyboard = keyboard.on_press(self.key_press_hook)

    def key_press_hook(self, keyboard_event: KeyboardEvent, **kwargs) -> None:
        """Keyboard callback hook"""
        # TODO Log key press
        self.key_pressed(keyboard_event.name)


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
            return DefaultKeyboardHandler(backend)

        # return the default handler
        return DefaultKeyboardHandler(backend)


if __name__ == "__main__":
    test = KeyboardFactory.get(None)
