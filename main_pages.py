from typing import Any, List, Optional

from asciimatics.effects import Print, Sprite
from asciimatics.event import Event, KeyboardEvent
from asciimatics.paths import Path
from asciimatics.renderers import Box, FigletText, StaticRenderer
from asciimatics.scene import Scene
from asciimatics.screen import Screen

import exceptions
from sprites.characters import character_box, character_box_pushing


# Wish title_screen and title_input_handler were more closely linked, maybe use a structure similar to controller.py
def title(screen: Screen) -> List[Scene]:
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


def title_IH(event: Event) -> Optional[Event]:
    """Handle title-screen inputs (IH = input handler)"""
    if isinstance(event, KeyboardEvent):
        key = event.key_code
        if key in [ord("q"), ord("Q"), Screen.KEY_ESCAPE]:
            raise exceptions.ExitGame()
        elif key in [ord("s"), ord("S"), ord(" "), ord("\n")]:
            raise exceptions.EnterLevel(0)
        else:
            return event
    else:
        return event


def settings(screen: Screen) -> List[Scene]:
    """Settings screen"""
    pass


def settings_IH(event: Event) -> Any:
    """Settings input handler"""
    pass


# uh oh shadows built-in credits
def credits(sceen: Screen) -> Any:
    """Credits screen"""
    pass


def credits_IH(event: Event) -> Any:
    """Credits input handler"""
    pass


def level_selector(screen: Screen):
    pass


def level_selector_IH(event: Event):
    pass
