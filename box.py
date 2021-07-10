#!/usr/bin/env python3

from __future__ import division
from asciimatics.effects import Print, Sprite
from asciimatics.renderers import FigletText, StaticRenderer
from asciimatics.scene import Scene
from asciimatics.screen import Screen
# from asciimatics.sprites import Arrow, Plot, Sam
from asciimatics.paths import Path
from asciimatics.exceptions import ResizeScreenError
from sprites.sprites import characther_box
import sys


def demo(screen: Screen) -> None:
    """Main Loop"""
    path = Path()
    path.jump_to(int(screen.width / 5), int(screen.height / 1.5))

    char = Sprite(screen, path=path, renderer_dict={
        "default": StaticRenderer(images=[characther_box])
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

    screen.play(scenes, stop_on_resize=True)


if __name__ == "__main__":
    while True:
        try:
            Screen.wrapper(demo)
            sys.exit(0)
        except ResizeScreenError:
            pass
