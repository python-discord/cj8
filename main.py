#!/usr/bin/env python3

from __future__ import division

import sys
from typing import Optional

from asciimatics.effects import Print, Sprite
from asciimatics.event import Event, KeyboardEvent
from asciimatics.exceptions import ResizeScreenError
# from asciimatics.sprites import Arrow, Plot, Sam
from asciimatics.paths import Path
from asciimatics.renderers import Box, FigletText, StaticRenderer
from asciimatics.scene import Scene
from asciimatics.screen import Screen

from sprites.sprites import character_box, character_box_pushing


class GameStart(Exception):
    """Raised when user starts the game"""

    pass


def handle_input(event: Event) -> Optional[Event]:
    """Handle title-screen inputs"""
    if isinstance(event, KeyboardEvent):
        key = event.key_code
        if key in [ord("q"), ord("Q")]:
            sys.exit(0)
        if key in [ord("s"), ord("S")]:
            raise GameStart


def title(screen: Screen) -> None:
    """Title screen"""
    char_path, bubble_path = Path(), Path()
    char_path.jump_to(screen.width // 5 + 3, screen.height // 2 + 5)
    bubble_path.jump_to(screen.width // 5 - 4, screen.height // 2 + 1)

    # Opening character with box on his head
    char_sprite = Sprite(
        screen, path=char_path, renderer_dict={
            "default": StaticRenderer(images=[character_box]*8 + [character_box_pushing]*10)
        }
    )

    # Load all components (boxes, titles, etc)
    scenes = []
    effects = [
        char_sprite,
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
    try:
        screen.play(scenes, stop_on_resize=True, unhandled_input=handle_input)
    except GameStart:
        screen.close()
        # START GAME


if __name__ == "__main__":
    while True:
        try:
            Screen.wrapper(title)
            sys.exit(0)
        except ResizeScreenError:
            pass
