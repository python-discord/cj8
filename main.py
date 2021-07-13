import sys

from src.frontend.core import CoreFrontend


def main():
    frontend = CoreFrontend()
    try:
        frontend.start_loop()
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == "__main__":
    main()
