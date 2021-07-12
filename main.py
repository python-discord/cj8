#!/usr/bin/env python3

from __future__ import division

import sys

from asciimatics.exceptions import ResizeScreenError
from asciimatics.screen import Screen

from gamelogic.controller import GameController
from sprites.maps import LEVELS
import main_pages as mp
from exceptions import *


def main(screen: Screen) -> None:
    """Main function"""

    # preload the main pages
    title = mp.title(screen)
    settings = mp.settings(screen)
    credits = mp.credits(screen)

    # Put everything onto the screen
    while True:
        try:
            screen.play(title, stop_on_resize=True, unhandled_input=mp.title_IH)
        except GameTransition as e:
            # I'm not sure if we should split each of the GameTransition exceptions up
            # ie - except EnterLevel:... except LevelSelector:...
            # or to have it like this, but do a bunch of isinstance()s
            # ie - if isinstance(e, EnterLevel):... elif isinstance(e, LevelSelector):...

            # screen.clear()  # dk if this is necessary or helpful
            if isinstance(e, EnterLevel):
                screen.play([GameController(screen, LEVELS[e.level])])
        except ExitGame:
            sys.exit()


if __name__ == "__main__":
    # I know, I hate this double while loop, too. We *could* move the try-except of main() into this while loop,
    # but it might not be the best to do a bunch of Screen.wrappers(). Doing screen.play() is probably better.
    # Additionally, read the comment in `except ResizeScreenError`
    while True:
        try:
            Screen.wrapper(main)
            break
        except ResizeScreenError:
            # ResizeScreenError in this outer while loop, since it still displays after resize, unlike if it were
            # in the inner scope of main()
            pass
