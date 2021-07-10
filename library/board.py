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
    player1_turn: bool
    game_over: bool

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
        self.player1_turn = True
        self.game_over = False

    def handle_input(self, number: typing.Literal[0, 1, 2, 3, 4, 5, 6, 7, 8]) -> None:
        """Handles updating the board when it needs to be updated."""
        if self.game_over:
            return

        if self.contents[number].contents != " ":
            return

        self.contents[number].contents = "O" if self.player1_turn else "X"
        self.player1_turn = not self.player1_turn

        self.game_over = self._won_wrapper()

    def display(self, term: blessed.Terminal) -> str:
        """Gives a colored display of the board."""
        result = ""
        for i in range(3):
            for j in range(3):
                result += self.contents[i * 3 + j].display(term)
            result += "\n"

        return result

    def _won_wrapper(self) -> bool:
        return self._won(tuple(content.contents for content in self.contents))

    def _won(self, board: tuple[typing.Literal["X", "O", " "], ...]) -> bool:
        if any(
            board[3 * i : 3 * (i + 1)] in (("X", "X", "X"), ("O", "O", "O"))
            for i in range(3)
        ):
            return True

        if any(
            board[3 * i :: 3] in (("X", "X", "X"), ("O", "O", "O")) for i in range(3)
        ):
            return True

        if board[0] == board[4] == board[8] != " ":
            return True

        if board[2] == board[4] == board[6] != " ":
            return True

        return False
