from typing import Union

from pynput import keyboard
from pynput.keyboard import Key, KeyCode

from src.backend.core import CoreBackend
from src.keyboard_handlers.core import BaseKeyboardHandler


class FallbackKeyboardHandler(BaseKeyboardHandler):
    """Implements the fallback handler"""

    def __init__(self, backend: CoreBackend):
        super().__init__(backend)

        self.keyboard = keyboard.Listener(on_press=self.key_press_hook)
        self.keyboard.start()

    def key_press_hook(self, keyboard_event: Union[KeyCode, Key], **kwargs) -> None:
        """Keyboard callback hook"""
        try:
            key = keyboard_event.char
        except AttributeError:
            key = keyboard_event.name
        self.key_pressed(key)
