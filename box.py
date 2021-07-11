#!/usr/bin/env python3

from __future__ import division

import sys

from asciimatics.effects import Print, Sprite
from asciimatics.event import Event, KeyboardEvent
from asciimatics.exceptions import ResizeScreenError
# from asciimatics.sprites import Arrow, Plot, Sam
from asciimatics.paths import DynamicPath, Path
from asciimatics.renderers import Box, FigletText, StaticRenderer
from asciimatics.scene import Scene
from asciimatics.screen import Screen

from sprites.sprites import character_box


class KeyboardController(DynamicPath):
    """Class for controlling input"""

    def process_event(self, event: Event) -> Event:
        """When the player press something, the processing is done here"""
        if isinstance(event, KeyboardEvent):
            key = event.key_code
            if key == Screen.KEY_UP:
                self._y -= 1
                self._y = max(self._y, 2)
            elif key == Screen.KEY_DOWN:
                self._y += 1
                self._y = min(self._y, self._screen.height-2)
            elif key == Screen.KEY_LEFT:
                self._x -= 1
                self._x = max(self._x, 3)
            elif key == Screen.KEY_RIGHT:
                self._x += 1
                self._x = min(self._x, self._screen.width-3)
            else:
                return event
        else:
            return event


def demo(screen: Screen) -> None:
    """Main Loop"""
    path = Path()
    path.jump_to(int(screen.width / 5), int(screen.height / 1.5))

    # Opening character with box on his head
    char = Sprite(
        screen, path=path, renderer_dict={
            "default": StaticRenderer(images=[character_box])
        }
    )

    # Load all components (boxes, titles, etc)
    scenes = []
    effects = [
        char,
        Print(
            screen,
            Box(screen.width, screen.height),
            0,
            start_frame=0,
        ),
        Print(
            screen,
            FigletText("BOXED", width=120, font="big"),
            screen.height // 2 - 6,
            start_frame=0,
        ),
        Print(
            screen,
            StaticRenderer(images=["(S)tart"]),
            screen.height // 2 + 3,
            start_frame=0,
        ),
        Print(
            screen,
            StaticRenderer(images=["(Q)uit"]),
            screen.height // 2 + 5,
            start_frame=0,
        ),
    ]

    scenes.append(Scene(effects))

    # Put everything onto the screen
    screen.play(scenes, stop_on_resize=True)


if __name__ == "__main__":
    while True:
        try:
            Screen.wrapper(demo)
            sys.exit(0)
        except ResizeScreenError:
            pass
