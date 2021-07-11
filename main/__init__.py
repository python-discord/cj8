__version__ = '0.0.0a'


def main() -> None:
    from main.main import main
    from functions.command_functions import *
    from functions.blessed_functions import *
    main()
    pass


if __name__ == "__main__":
    main()