import dataclasses
import typing

import blessed


@dataclasses.dataclass()
class Cell:
    """Represents an individual cell in a game of tic-tac-toe."""

    contents: typing.Literal[" ", "X", "O"] = " "

    def display(self, term: blessed.Terminal) -> str:
        """Gives a colored display of the cell."""
        if self.contents == " ":
            return self.contents
        elif self.contents == "X":
            return f"{term.red}{self.contents}{term.normal}"
        elif self.contents == "O":
            return f"{term.blue}{self.contents}{term.normal}"


class Board:
    """Represents the board that the game of tic-tac-toe is played on."""

    contents: tuple[Cell, Cell, Cell, Cell, Cell, Cell, Cell, Cell, Cell]
    turn: typing.Literal["X", "O"]

    def __init__(self) -> None:
        self.contents = (
            Cell(),
            Cell(),
            Cell(),
            Cell(),
            Cell(),
            Cell(),
            Cell(),
            Cell(),
            Cell(),
        )
        self.turn = "O"

    def handle_input(self, number: typing.Literal[0, 1, 2, 3, 4, 5, 6, 7, 8]) -> None:
        """Handles updating the board when it needs to be updated."""
        self.contents[number].contents = self.turn

        self.turn = "O" if self.turn == "X" else "X"

    def display(self, term: blessed.Terminal) -> str:
        """Gives a colored display of the board."""
        result = ""
        for i in range(3):
            for j in range(3):
                result += self.contents[i * 3 + j].display(term)
            result += "\n"

        return result
