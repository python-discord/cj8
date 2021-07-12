from typing import Optional

from asciimatics.effects import Print, Sprite
from asciimatics.paths import Path
from asciimatics.renderers import Box, FigletText, StaticRenderer
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.event import Event, KeyboardEvent

from sprites.characters import character_box, character_box_pushing
from exceptions import *


# Wish title_screen and title_input_handler were more closely linked, maybe use a structure similar to controller.py
def title(screen: Screen) -> list[Scene]:
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
            FigletText("ARE YOU IN A", width=120),
            screen.height // 2 - 7,
            start_frame=0),
        Print(
            screen,
            FigletText("BOX ???", width=120),
            screen.height // 2 - 2,
            start_frame=0),
        Print(
            screen,
            StaticRenderer(images=["(S)tart"]),
            screen.height // 2 + 4,
            start_frame=0,
        ),
        Print(
            screen,
            StaticRenderer(images=["(Q)uit"]),
            screen.height // 2 + 5,
            start_frame=0,
        ),
    ]

    return [Scene(effects)]


def title_IH(event: Event) -> None:  # Optional[Event]:
    """Handle title-screen inputs (IH = input handler)"""
    if isinstance(event, KeyboardEvent):
        key = event.key_code
        if key in [ord("q"), ord("Q"), Screen.KEY_ESCAPE]:
            raise ExitGame()
        if key in [ord("s"), ord("S"), ord(" "), ord("\n")]:
            raise EnterLevel(0)


def settings(screen: Screen) -> list[Scene]:
    pass


def settings_IH(event: Event):
    pass


# uh oh shadows built-in credits
def credits(sceen: Screen):
    pass


def credits_IH(event: Event):
    pass
