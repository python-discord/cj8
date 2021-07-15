# type: ignore
"""Collection of utilities."""
from typing import Iterable, Union

import numpy as np
from blessed.terminal import Terminal


class Vec(np.ndarray):
    """2D vector class that can be used with `int` and `(int, int)` for arithmetic."""

    def __new__(cls, x: int, y: int):
        """Create new array."""
        obj = super().__new__(
            cls, (2,), np.int16, np.asarray((x, y)), offset=0, strides=None, order=None
        )
        obj.x = int(x)
        obj.y = int(y)
        return obj

    @property
    def x(self) -> int:
        """Get value of x as first co-ordinate"""
        return int(self[0])

    @property
    def y(self) -> int:
        """Get value of y as first co-ordinate"""
        return int(self[1])

    @x.setter
    def x(self, x: Union[int, float]) -> None:
        """Set value of x as first co-ordinate."""
        self[0] = int(x)

    @y.setter
    def y(self, y: Union[int, float]) -> None:
        """Set value of y as first co-ordinate."""
        self[1] = int(y)

    def __iter__(self) -> Iterable:
        return map(int, (self.x, self.y))


class Boundary:
    """Boundary Class stores information necessary to render a box of a specific height and width"""

    def __init__(self, width: str, height: str, top_left: Vec, term: Terminal) -> None:
        self.width = width - 1
        self.height = height - 1
        self.term = term
        self.map = self.generate_map(top_left)

    def generate_map(self, top_left: Vec) -> str:
        """Generates a string that can be rendered by a Render Object"""
        x, y = top_left
        my_map = []
        my_map.append(self.term.move_xy(x, y) + "┌".ljust((self.width), "─") + "┐")
        for i in range(self.height - 1):
            my_map.append(
                self.term.move_xy(x, y + i + 1) + "│".ljust((self.width), " ") + "│"
            )
        my_map.append(
            self.term.move_xy(x, y + self.height) + "└".ljust((self.width), "─") + "┘"
        )
        return "".join(my_map)


if __name__ == "__main__":
    square = Boundary(20, 20)
    print("\n".join(square.map))
