from itertools import chain
from typing import Optional
from time import time
from random import randint, choice

from asciimatics.effects import Effect, Print, Sprite, Stars
from asciimatics.event import Event, KeyboardEvent
from asciimatics.particles import RingFirework, SerpentFirework, StarFirework, PalmFirework
from asciimatics.paths import Path
from asciimatics.renderers import Box, FigletText, StaticRenderer, Rainbow
from asciimatics.scene import Scene
from asciimatics.screen import Screen

import resources.exceptions as exceptions
from resources.sprites.characters import character_box, character_box_pushing, character_box_pushing2
from ..asciimatics_better import Mirage2


# todo
#  incorporate sound settings
#  add exit_scene when exiting a scene


def back_button(screen) -> Effect: return Print(screen, StaticRenderer(["<-- Back (Esc)"]), 0, 1)


def exit_scene(screen: Screen, speed: float) -> Effect:
    return Mirage2(screen, StaticRenderer([(" " * screen.width + "\n") * screen.height]), False, 0, 0, speed,
                   stop_frame=60)


class Title(Scene):
    def __init__(self, screen: Screen):
        """Title screen"""
        char_path, bubble_path = Path(), Path()
        char_path.jump_to(screen.width // 5 + 3, screen.height // 2 + 5)
        bubble_path.jump_to(screen.width // 5 - 4, screen.height // 2 + 1)

        # Opening character with box on his head
        char_sprite = Sprite(
            screen, path=char_path, renderer_dict={
                "default": StaticRenderer(images=[character_box] * 8
                                                 + [character_box_pushing] * 10
                                                 + [character_box_pushing2] * 10)
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
                screen.height // 2 - 8,
                start_frame=0
            ),
            Print(
                screen,
                FigletText("BOX ???", width=120),
                screen.height // 2 - 3,
                start_frame=0
            ),
            Print(
                screen,
                StaticRenderer(images=["Start (Space)"]),
                screen.height // 2 + 4,
                start_frame=0,
            ),
            Print(
                screen,
                StaticRenderer(images=["Quit (Esc)"]),
                screen.height // 2 + 5,
                start_frame=0,
            ),
            Print(
                screen,
                StaticRenderer(images=["Settings (S)"]),
                screen.height // 2 + 7,
                start_frame=0,
            ),
            Print(
                screen,
                StaticRenderer(images=["Credits (C)"]),
                screen.height // 2 + 8,
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
        ['volume', 5],
    ]

    def __init__(self, screen: Screen):
        """Settings screen"""
        # todo sound settings mostly, dk what else to put
        self.selected_setting = 0
        super().__init__([Print(screen, StaticRenderer(['│']), screen.height // 2)])

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
    names = "\n".join(["DEVELOPED BY:", "Objectivitix#9891", "nop#6157", "Lognarius#1483", "JLW#1242", "stg-tel#7084"])
    nicks = "\n".join(["DEVELOPED BY:", "object           ", "nop     ", "Lognarius     ", "JLW     ", "snuffles    "])

    def __init__(self, screen: Screen):
        """Credits screen"""
        won = exceptions.WinGame.won
        effects = [Stars(screen, round(screen.height * screen.width / 30),
                         "........+++.......   .......xx......     .......**......     ......,,,,......               "
                         "              ..............                               "),
                   Print(screen, StaticRenderer([Credits.names, Credits.nicks], lambda: 0 if time() % 8 < 4 else 1),
                         screen.height // 2 + (5 if won else -3), clear=True, transparent=False)]
        if won:
            effects.append(Print(screen, FigletText("THANK YOU FOR PLAYING!", width=screen.width), screen.height // 3))
        super().__init__(effects)

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
        super().__init__(list(
            chain.from_iterable((Mirage2(screen, Box(box_width, box_height, False), True,
                                         y := i // 3 * int(box_height * 1.5) + box_height,
                                         x := (i % 3 + 1) * (screen.width // 4), 0.25),
                                 Print(screen, StaticRenderer([f"{i + 1}"]), y - 1, x))
                                for i in range(exceptions.EnterLevel.max_level + 1))), -1)

    def process_event(self, event: Event) -> Event:
        """Level selector input handler"""
        if isinstance(event, KeyboardEvent):
            key = event.key_code
            try:
                if (lvl := int(chr(key))) in range(1, 10):
                    if lvl <= exceptions.EnterLevel.max_level + 1:
                        raise exceptions.EnterLevel(lvl - 1)
            except ValueError:
                pass
        return event


class EndScene(Scene):
    def __init__(self, screen: Screen):
        self._screen = screen
        self.current_fireworks = []
        self.firework_choices = [
            (PalmFirework, 25, 30),
            (PalmFirework, 30, 40),
            (StarFirework, 25, 35),
            (StarFirework, 30, 45),
            (StarFirework, 25, 50),
            (RingFirework, 20, 40),
            (SerpentFirework, 25, 40),
        ]
        runtime = 5000
        self.add_fireworks(1000, runtime)
        effects = [Stars(screen, screen.width), *self.current_fireworks,
                   Print(screen,
                         Rainbow(screen, FigletText("CONGRATULATIONS")),
                         screen.height // 2 - 6,
                         speed=0,
                         start_frame=0, stop_frame=runtime),
                   Print(screen,
                         Rainbow(screen, FigletText("YOU ESCAPED THE BOXES!")),
                         screen.height // 2 + 1,
                         speed=0,
                         start_frame=0, stop_frame=runtime)]
        super().__init__(effects)

    def add_fireworks(self, amount: int, stop_frame: int):
        for _ in range(amount):
            firework, start, stop = choice(self.firework_choices)
            self.current_fireworks.append(
                firework(self._screen,
                         randint(0, self._screen.width),
                         randint(self._screen.height // 8, self._screen.height * 3 // 7),
                         randint(start, stop),
                         start_frame=randint(0, stop_frame)))

    def process_event(self, event):
        pass


def default_IH(event: Event) -> Event:
    if isinstance(event, KeyboardEvent):
        key = event.key_code
        if key in [Screen.KEY_ESCAPE]:
            raise exceptions.Title()
        if key in [ord("e"), ord("E")]:
            raise exceptions.WinGame()
    return event
