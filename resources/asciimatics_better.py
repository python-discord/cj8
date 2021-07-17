"""
This file is for things we are taking from asciimatics and making better, since asciimatics has very little
customizability on its own.
"""
from random import random

from asciimatics.screen import Screen
from asciimatics.effects import Mirage


class Mirage2(Mirage):
    def __init__(self, screen, renderer, centered: bool, y, x, rate, colour=Screen.COLOUR_WHITE, **kwargs):
        super().__init__(screen, renderer, y, colour, **kwargs)
        self._centered = centered
        self._x = x
        self._rate = rate

    def _update(self, frame_no):
        if frame_no % 2 != 0:
            return

        image, colours = self._renderer.rendered_text
        y = self._y - len(image) // 2 if self._centered else self._y
        for i, line in enumerate(image):
            x = self._x - len(line) // 2 if self._centered else (self._screen.width - len(line)) // 2

            if self._screen.is_visible(x, y):
                for j, c in enumerate(line):
                    if c != " " and random() < self._rate:
                        if colours[i][j][0] is not None:
                            self._screen.print_at(c, x, y,
                                                  colours[i][j][0],
                                                  colours[i][j][1])
                        else:
                            self._screen.print_at(c, x, y, self._colour)
                    x += 1
            y += 1

