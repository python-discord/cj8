#!/usr/bin/env python3

from __future__ import division

import sys
from typing import Callable, List, Tuple, Union

from asciimatics.exceptions import ResizeScreenError
from asciimatics.scene import Scene
from asciimatics.screen import Screen

import resources.exceptions as exceptions
import resources.scenes.main_pages as mp
from resources.scenes.controller import GameController, game_IH
from resources.sprites.maps import LEVELS

Scenes = Union[Callable, List[Scene]]


def play_scenes(screen: Screen, scenes: Scenes, ih: Callable) -> Tuple[Scenes, Callable]:
    """Play scenes until screen resizes, then return current scene + ih."""

    # Loop to manage scene transitions and screen resizes
    while True:
        # If "scenes" is a function, return that original function on resize
        returned_scenes = scenes
        if callable(scenes):
            scenes: List[Scene] = scenes(screen)

        try:
            # Update old effects to have new screen variable
            for scene in scenes:
                # This works for some reason (don't touch thanks :D)
                for effect in scene.effects:
                    if hasattr(effect, "screen"):
                        effect._screen = screen

            # Play the prepared scenes
            screen.play(scenes, stop_on_resize=True, unhandled_input=ih)

        except exceptions.GameTransition as e:
            # Set next scenes
            screen.clear()  # Looks nicer
            if isinstance(e, exceptions.EnterLevel):
                scenes = [GameController(screen, LEVELS[e.level])]
                ih = game_IH
            elif isinstance(e, exceptions.Title):
                # Remember - unless next scene is a level, set "scenes" to a function (not a scene)
                scenes = mp.title
                ih = mp.title_IH
            # etc

        except exceptions.ExitGame:
            sys.exit(0)

        except ResizeScreenError:
            # On resize, return current scenes and input handler
            screen.close()
            return returned_scenes, ih


def main() -> None:
    """Main function."""

    scenes = mp.title
    ih = mp.title_IH

    # Keep looping on resize, using whatever screen was showing at the time
    while True:
        scenes, ih = Screen.wrapper(play_scenes, arguments=[scenes, ih])


if __name__ == "__main__":
    main()
