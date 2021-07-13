import sys
from typing import NoReturn

from src.frontend.core import CoreFrontend


def main() -> NoReturn:
    """Run the game."""
    frontend = CoreFrontend()
    try:
        frontend.start_loop()
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == "__main__":
    main()
