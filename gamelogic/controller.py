from __future__ import division

from copy import deepcopy
from math import ceil
from typing import Any, List, Optional, Tuple

from asciimatics.effects import Effect
from asciimatics.event import Event, KeyboardEvent
from asciimatics.exceptions import StopApplication
# from asciimatics.sprites import Arrow, Plot, Sam
from asciimatics.scene import Scene
from asciimatics.screen import Screen

MOVEMENT_MAPPINGS = [
    {
        "trigger_keys": (ord("a"), Screen.KEY_LEFT),
        "raycast_direction": (-1, 0),
        "map_movement": ("x", -1),
    },
    {
        "trigger_keys": (ord("d"), Screen.KEY_RIGHT),
        "raycast_direction": (+1, 0),
        "map_movement": ("x", +1),
    },
    {
        "trigger_keys": (ord("w"), Screen.KEY_UP),
        "raycast_direction": (0, -1),
        "map_movement": ("y", -1),
    },
    {
        "trigger_keys": (ord("s"), Screen.KEY_DOWN),
        "raycast_direction": (0, +1),
        "map_movement": ("y", +1),
    },
]


class Map(Effect):
    """
    Draw the map relative to the player position
    and controls the map in general.
    """

    def __init__(self, screen: Screen, game_map: List[str]):
        super(Map, self).__init__(screen)
        self._map: List[str] = deepcopy(game_map)

        for i, line in enumerate(game_map):
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
        and the maps surrounding it.
        """
        space_x = self.screen.width
        offset_x = (space_x // 2 - self.player_x, ceil(space_x / 2) + self.player_x)
        space_y = self.screen.height
        offset_y = space_y // 2 - self.player_y

        for i in range(offset_y):
            self.screen.print_at(" "*self.screen.width, 0, i)
        for i, chars in enumerate(self._map):
            chars = " "*offset_x[0] + chars + " "*offset_x[1]
            self.screen.print_at(chars, 0, offset_y + i)
        for i in range(offset_y+len(self._map), self.screen.height):
            self.screen.print_at(" "*self.screen.width, 0, i)

        self.screen.print_at("@", self.screen.width//2, self.screen.height//2)

    @property
    def frame_update_count(self) -> int:
        """Required function for Effects."""
        # No animation required.
        return 0

    @property
    def stop_frame(self) -> int:
        """Required function for Effects."""
        # No specific end point for this Effect.  Carry on running forever.
        return 0

    def reset(self) -> None:
        """Required function for Effects."""
        # Nothing special to do.  Just need this to satisfy the ABC.
        pass


class GameController(Scene):
    """
    Class responsible for moving the player along the map
    and controlling the game in general.
    """

    # Controls collisions
    EMPTY_SPACE = 0
    WALL = 1

    def __init__(self, screen: Screen, level_map: List[str]):
        self._map = Map(screen, level_map)
        effects = [
            self._map,
        ]
        super(GameController, self).__init__(effects, -1)

    def cast_ray(self, direction: Tuple[int], pos: Optional[List[int]] = None) -> int:
        """
        Cast a ray into 'direction' starting from 'pos';
        if 'pos' is not specified we default to player pos.
        """

        if pos is None:
            pos = [self._map.player_x, self._map.player_y]

        x = direction[0] + pos[0]
        y = direction[1] + pos[1]

        if self._map._map[y][x] == " ":
            return GameController.EMPTY_SPACE

    def process_event(self, event: Event) -> Optional[Event]:
        """Process events, mostly player input."""
        # Allow standard event processing first
        if super(GameController, self).process_event(event) is None:
            return

        # If that didn't handle it, check for a key that this demo understands.
        if isinstance(event, KeyboardEvent):
            key_code = event.key_code
            not_recognised = True  # Flag for if the key code wasn't recognised

            if key_code in (ord("q"), ord("Q")):
                raise StopApplication("User exit")

            for movement_mapping in MOVEMENT_MAPPINGS:
                if key_code in movement_mapping["trigger_keys"]:
                    if (
                            self.cast_ray(movement_mapping["raycast_direction"])
                            == GameController.EMPTY_SPACE
                    ):
                        axis, move = movement_mapping["map_movement"]
                        attr = (self._map, f"player_{axis}")
                        setattr(*attr, getattr(*attr) + move)

                    not_recognised = False
                    break

            if not_recognised:
                # Not a recognised key - pass on to other handlers.
                return event

        else:
            # Ignore other types of events.
            return event
