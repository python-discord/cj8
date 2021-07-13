import logging
import sys
from abc import ABC

from src.backend.core import CoreBackend
from src.file_logging import logger


class BaseKeyboardHandler(ABC):
    """
    Base abstract class for handling keyboard inputs

    Subclasses should implement actual concrete keyboard handling for the different OS
    options if we decide to use Keyboard as it requires root to run.
    """

    def __init__(self, backend: CoreBackend):
        self.backend = backend

        self.logger = logger

    def key_pressed(self, key: str) -> None:
        """Pass on the key press to the backend module"""
        if self.logger.isEnabledFor(logging.DEBUG):
            self.logger.debug(f"Keyboard handler registered: {key}")
        self.backend.key_press(key)


class KeyboardFactory:
    """
    Called by the frontend module to get a keyboard handler

    Handles sending the correct module depending on OS
    """

    WIN = "win32"
    LINUX = "linux"
    MACOS = "darwin"

    @staticmethod
    def get(backend: CoreBackend) -> BaseKeyboardHandler:
        """
        Returns a concrete Keyboard Handler class

        Implements the factory pattern for returning the correct Keyboard handler
        depending on the OS

        :param backend: CoreBackend object to pass to the keyboard handler
        """
        platform = sys.platform

        if platform in (KeyboardFactory.LINUX, KeyboardFactory.MACOS):
            from src.keyboard.fallback import FallbackKeyboardHandler

            return FallbackKeyboardHandler(backend)

        # Return the default handler
        from src.keyboard.default import DefaultKeyboardHandler

        return DefaultKeyboardHandler(backend)
