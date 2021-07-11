from src.backend.core import CoreBackend
from src.frontend.keyboard_handlers import BaseKeyboardHandler, KeyboardFactory


class CoreFrontend:
    """
    Frontend module

    Responsible for rendering the game state to the terminal

    Should query the backend module for an update each loop cycle as well as passing
    on any keyboard presses that were registered.

    Should draw the 'illuminated' circle of vision around the ball by querying the
    backend for all of the objects within a certain distance from the ball.

    Should draw out the current active mutators as well and the current score.
    """

    def __init__(self):
        self.backend: CoreBackend = CoreBackend()
        self.keyboard_handler: BaseKeyboardHandler = KeyboardFactory.get(self.backend)

    def start_loop(self) -> None:
        """Start the render loop"""
