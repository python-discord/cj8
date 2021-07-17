from itertools import chain
from typing import Optional

from asciimatics.effects import Print, Sprite
from asciimatics.event import Event, KeyboardEvent
from asciimatics.paths import Path
from asciimatics.renderers import Box, FigletText, StaticRenderer
from asciimatics.scene import Scene
from asciimatics.screen import Screen

import resources.exceptions as exceptions
from resources.sprites.characters import character_box, character_box_pushing
from ..asciimatics_better import Mirage2

# todo
#  add credits
#  incorporate sound settings
#  add stars render as a bg for title or credits or smth
#  add exit_scene when exiting a scene


back_button = lambda screen: Print(screen, StaticRenderer(["<-- Back (Esc)"]), 0, 1)
def exit_scene(screen: Screen) -> Scene:
    return Mirage2(screen, StaticRenderer([(" " * screen.width + "\n") * screen.height]), False, 0, 0, 0.35, stop_frame=60)


class Title(Scene):
    def __init__(self, screen: Screen):
        """Title screen"""
        char_path, bubble_path = Path(), Path()
        char_path.jump_to(screen.width // 5 + 3, screen.height // 2 + 5)
        bubble_path.jump_to(screen.width // 5 - 4, screen.height // 2 + 1)

        # Opening character with box on his head
        char_sprite = Sprite(
            screen, path=char_path, renderer_dict={
                "default": StaticRenderer(images=[character_box] * 8 + [character_box_pushing] * 10)
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
                start_frame=0
            ),
            Print(
                screen,
                FigletText("BOX ???", width=120),
                screen.height // 2 - 2,
                start_frame=0
            ),
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

        super().__init__(effects, -1)

    def process_event(self, event: Event) -> Optional[Event]:
        """Handle title-screen inputs (IH = input handler)"""
        if isinstance(event, KeyboardEvent):
            key = event.key_code
            if key in [Screen.KEY_ESCAPE, ord("q"), ord("Q")]:
                raise exceptions.ExitGame()
            elif key in [ord(" "), ord("\n"), ord("\r")]:
                raise exceptions.LevelSelector()
            elif key in [ord("s"), ord("S")]:
                raise exceptions.Settings()
            elif key in [ord("c"), ord("C")]:
                raise exceptions.Credits()
        return event


class Settings(Scene):
    # each item in settings is [name: str, val: Any]
    settings = [
        ['', 5],
        ['', True]
    ]

    def __init__(self, screen: Screen):
        """Settings screen"""
        # todo sound settings mostly, dk what else to put
        self.selected_setting = 0
        super().__init__([])

    def process_event(self, event: Event) -> Event:
        """Settings input handler"""
        if isinstance(event, KeyboardEvent):
            key = event.key_code

            if key in [Screen.KEY_DOWN, Screen.KEY_TAB]:
                self.selected_setting += 1
                if self.selected_setting >= len(Settings.settings):
                    self.selected_setting = 0

            elif key in [Screen.KEY_UP]:
                self.selected_setting -= 1
                if self.selected_setting < 0:
                    self.selected_setting = len(Settings.settings) - 1

            elif key in [Screen.KEY_RIGHT]:
                if isinstance(Settings.settings[self.selected_setting][1], int):
                    Settings.settings[self.selected_setting][1] += 1  # todo replace settings[...] with a pointer
                elif isinstance(Settings.settings[self.selected_setting][1], bool):
                    Settings.settings[self.selected_setting][1] = not Settings.settings[self.selected_setting][1]

            elif key in [Screen.KEY_LEFT]:
                if isinstance(Settings.settings[self.selected_setting][1], int):
                    Settings.settings[self.selected_setting][1] -= 1
                elif isinstance(Settings.settings[self.selected_setting][1], bool):
                    Settings.settings[self.selected_setting][1] = not Settings.settings[self.selected_setting][1]

            elif key in [ord(" "), ord("\n"), ord("\r")]:
                if isinstance(Settings.settings[self.selected_setting][1], bool):
                    Settings.settings[self.selected_setting][1] = not Settings.settings[self.selected_setting][1]

        return event


class Credits(Scene):
    def __init__(self, sceen: Screen):
        """Credits screen"""
        super().__init__([])

    def process_event(self, event: Event) -> Event:
        """Credits input handler"""
        if isinstance(event, KeyboardEvent):
            key = event.key_code
        return event


class LevelSelector(Scene):
    def __init__(self, screen: Screen):
        """Level selector screen"""
        box_width = screen.width // 5
        box_height = 7
        super().__init__(list(chain.from_iterable((
            Mirage2(screen, Box(box_width, box_height, False), True,
                    y := i // 3 * int(box_height * 1.5) + box_height, x := (i % 3 + 1) * (screen.width // 4), 0.25),
            Print(screen, StaticRenderer([f"${{{c}}}{i + 1}" for c in [1, 3, 2, 4, 6, 5]]), y-1, x))
            for i in range(exceptions.EnterLevel.max_level + 1))), -1)

    def process_event(self, event: Event) -> Event:
        """Level selector input handler"""
        if isinstance(event, KeyboardEvent):
            key = event.key_code
            try:
                if (lvl := int(chr(key))) in range(10):
                    if lvl <= exceptions.EnterLevel.max_level:
                        raise exceptions.EnterLevel(lvl - 1)
            except ValueError:
                pass
        return event


def default_IH(event: Event) -> Event:
    if isinstance(event, KeyboardEvent):
        key = event.key_code
        if key in [Screen.KEY_ESCAPE]:
            raise exceptions.Title()
    return event
