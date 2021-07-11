#!/usr/bin/env python3

from __future__ import division
from asciimatics.event import KeyboardEvent, Event
from asciimatics.effects import Print, Sprite
from asciimatics.renderers import FigletText, StaticRenderer
from asciimatics.scene import Scene
from asciimatics.screen import Screen
# from asciimatics.sprites import Arrow, Plot, Sam
from asciimatics.paths import Path
from asciimatics.exceptions import ResizeScreenError
from sprites.sprites import character_box, character
from asciimatics.paths import DynamicPath
import sys


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
    path = KeyboardController(screen, int(screen.width / 5), int(screen.height / 1.5))
    #path.jump_to(int(screen.width / 5), int(screen.height / 1.5))

    char = Sprite(screen, path=path, renderer_dict={
        "default": StaticRenderer(images=[character_box])
    })

    scenes = []
    effects = [
        char,
        Print(
            screen,
            FigletText("BOX", width=120),
            screen.height // 2 - 6,
            start_frame=0),
        Print(
            screen,
            StaticRenderer(images=["(S)tart"]),
            screen.height // 2 + 1,
            start_frame=0),
        Print(
            screen,
            StaticRenderer(images=["(Q)uit"]),
            screen.height // 2 + 3,
            start_frame=0)
    ]

    scenes.append(Scene(effects))

    # Start Screen
    screen.play(scenes, stop_on_resize=True)


if __name__ == "__main__":
    while True:
        try:
            Screen.wrapper(demo)
            sys.exit(0)
        except ResizeScreenError:
            pass
