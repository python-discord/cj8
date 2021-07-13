import keyboard
from keyboard import KeyboardEvent

from src.backend.core import CoreBackend
from src.keyboard_handlers.core import BaseKeyboardHandler


class DefaultKeyboardHandler(BaseKeyboardHandler):
    """Implements the default handler"""

    def __init__(self, backend: CoreBackend):
        super().__init__(backend)

        self.keyboard = keyboard.on_press(self.key_press_hook)

    def key_press_hook(self, keyboard_event: KeyboardEvent, **kwargs) -> None:
        """Keyboard callback hook"""
        self.key_pressed(keyboard_event.name)
