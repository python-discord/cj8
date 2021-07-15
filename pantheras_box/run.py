import sys
from typing import NoReturn

from pantheras_box.frontend.core import CoreFrontend


def run_game() -> NoReturn:
    """Run the game."""
    frontend = CoreFrontend()
    try:
        frontend.start_loop()
    except KeyboardInterrupt:
        sys.exit(0)
