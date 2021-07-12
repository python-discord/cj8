from __future__ import division

from copy import deepcopy
from typing import Any, List

from asciimatics.effects import Effect
from asciimatics.event import Event, KeyboardEvent
from asciimatics.exceptions import StopApplication
# from asciimatics.sprites import Arrow, Plot, Sam
from asciimatics.scene import Scene
from asciimatics.screen import Screen


class Map(Effect):
    """
    Draws the map relative to the player position
    and controls the map in general
    """

    def __init__(self, screen: Screen, map: List[str]):
        super(Map, self).__init__(screen)
        self._screen = screen
        self._map = deepcopy(map)

        for i, line in enumerate(map):
            j = line.find('@')
            if j > -1:
                self.player_x = j
                self.player_y = i
                self._map[i] = line.replace('@', ' ')

        self._x = 0
        self._y = 0

        # print(f"player: ({self.player_x},{self.player_y})")
        # print(f"map: ({self._map_x},{self._map_y})")

    def _update(self, _: Any = None) -> None:
        """
        This function is called every frame, here we draw the player centered at the screen
        and the maps surrounding it
        """
        screen_i = screen_j = 0
        w2 = self._screen.width // 2
        h2 = self._screen.height // 2
        for offset_i in range(-w2, w2):
            screen_j = 0
            for offset_j in range(-h2, h2):
                # breakpoint()
                # print(f"offset: {offset_i},{offset_j}")
                rel_x, rel_y = self.player_x+offset_i, self.player_y+offset_j

                # print(f"map ({rel_x},{rel_y})")
                # breakpoint()
                if rel_x > -1 and rel_x < len(self._map[0]) \
                        and rel_y > -1 and rel_y < len(self._map):

                    if offset_i == 0 and offset_j == 0:
                        self._screen._print_at(
                            "@", screen_i, screen_j, 1)
                    else:
                        self._screen._print_at(
                            self._map[rel_y][rel_x], screen_i, screen_j, 1)
                else:
                    self._screen._print_at(" ", screen_i, screen_j, 1)
                screen_j += 1
            screen_i += 1
        self._screen._print_at("@", w2, h2, 1)

    @property
    def frame_update_count(self) -> int:
        """Required function for Effects"""
        # No animation required.
        return 0

    @property
    def stop_frame(self) -> int:
        """Required function for Effects"""
        # No specific end point for this Effect.  Carry on running forever.
        return 0

    def reset(self) -> None:
        """Required function for Effects"""
        # Nothing special to do.  Just need this to satisfy the ABC.
        pass


class GameController(Scene):
    """
    Class responsible for moving the player along the map
    and controlling the game in general
    """

    # Controls collisions
    EMPTY_SPACE = 0
    WALL = 1

    def __init__(self, screen: Screen, level_map: List[str]):
        self._screen = screen
        self._map = Map(screen, level_map)
        effects = [
            self._map,
        ]
        super(GameController, self).__init__(effects, -1)

    def cast_ray(self, direction: List[int], pos: List[int] = None) -> int:
        """
        Cast a ray into 'direction' starting from 'pos'
        if 'pos' is not specified we default to player pos
        """

        if pos is None:
            pos = [self._map.player_x, self._map.player_y]

        x = direction[0] + pos[0]
        y = direction[1] + pos[1]

        if self._map._map[y][x] == " ":
            return GameController.EMPTY_SPACE

    def process_event(self, event: Event) -> Event:
        """Process events, mostly player input"""
        # Allow standard event processing first
        if super(GameController, self).process_event(event) is None:
            return

        # If that didn't handle it, check for a key that this demo understands.
        if isinstance(event, KeyboardEvent):
            c = event.key_code
            if c in (ord("q"), ord("Q")):
                raise StopApplication("User exit")
            elif c in (ord("a"), Screen.KEY_LEFT):
                # Only move if we are going to an empty space
                if self.cast_ray([-1, 0]) == GameController.EMPTY_SPACE:
                    self._map.player_x -= 1
            elif c in (ord("d"), Screen.KEY_RIGHT):
                if self.cast_ray([1, 0]) == GameController.EMPTY_SPACE:
                    self._map.player_x += 1
            elif c in (ord("w"), Screen.KEY_UP):
                if self.cast_ray([0, -1]) == GameController.EMPTY_SPACE:
                    self._map.player_y -= 1
            elif c in (ord("s"), Screen.KEY_DOWN):
                if self.cast_ray([0, 1]) == GameController.EMPTY_SPACE:
                    self._map.player_y += 1
            # elif c in (ord("m"), ord("M")):
            #     self._state.show_mini_map = not self._state.show_mini_map
            #     if self._state.show_mini_map:
            #         self.add_effect(self._mini_map)
            else:
                # Not a recognised key - pass on to other handlers.
                return event
        else:
            # Ignore other types of events.
            return event
