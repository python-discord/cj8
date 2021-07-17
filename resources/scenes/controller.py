from __future__ import division

from copy import deepcopy
from math import ceil
# from random import choice
from typing import Any, List, Optional, Tuple

from asciimatics.effects import Effect, Print
from asciimatics.event import Event, KeyboardEvent
from asciimatics.renderers import SpeechBubble
# from asciimatics.sprites import Arrow, Plot, Sam
from asciimatics.scene import Scene
from asciimatics.screen import Screen

import resources.exceptions as exceptions
from resources.sprites.maps import LEVELS
from resources.raycasting import raycast
from resources.generation import even_random_distribution as r_distribution

# Mappings of directional trigger keys such as movement or tag
# to their corresponding properties/direction/map changes.
# This is to reduce the redundancy of elif-chains, using a more
# general approach.
DIRECTIONAL_MANEUVER_MAPPINGS = [
    {
        "movement_trigger_keys": (ord("a"), Screen.KEY_LEFT),
        "tag_trigger_keys": (ord("A"),),
        "wall": "l",
        "raycast_direction": (-1, 0),
        "map_movement": ("x", -1),
    },
    {
        "movement_trigger_keys": (ord("d"), Screen.KEY_RIGHT),
        "tag_trigger_keys": (ord("D"),),
        "wall": "r",
        "raycast_direction": (+1, 0),
        "map_movement": ("x", +1),
    },
    {
        "movement_trigger_keys": (ord("w"), Screen.KEY_UP),
        "tag_trigger_keys": (ord("W"),),
        "wall": "u",
        "raycast_direction": (0, -1),
        "map_movement": ("y", -1),
    },
    {
        "movement_trigger_keys": (ord("s"), Screen.KEY_DOWN),
        "tag_trigger_keys": (ord("S"),),
        "wall": "d",
        "raycast_direction": (0, +1),
        "map_movement": ("y", +1),
    },
]

texturing = r_distribution([' ', '.', ','], [80, 10, 10], 1000)


class Map(Effect):
    """
    Draw the map relative to the player position
    and controls the map in general.
    """

    def __init__(self, screen: Screen, game_map: str):
        super(Map, self).__init__(screen)
        
        # self.map = [''.join([choice(texturing) if char == ' ' else char for char in line]) for line in game_map]
        self.map: List[str] = "".join(
            "." if char == " " and counter % 2 else char
            for counter, char in enumerate(deepcopy(game_map))
        ).split("\n")

        for i, line in enumerate(self.map):
            j = line.find('@')
            if j > -1:
                self.player_x = j
                self.player_y = i
                self.map[i] = line.replace('@', ' ')

        self.vision = 10  # will have a way to change this later

        # print(f"player: ({self.player_x},{self.player_y})")
        # print(f"map: ({self.map_x},{self.map_y})")

    def _update(self, _: Any = None) -> None:
        """
        This function is called every frame, here we draw the player centered at the screen
        and the maps surrounding it.
        """
        offset_x = (self.screen.width // 2 - self.player_x, ceil(self.screen.width / 2) + self.player_x)
        offset_y = self.screen.height // 2 - self.player_y

        for i in range(offset_y):
            self.screen.print_at(" " * self.screen.width, 0, i)

        for i, line in enumerate(raycast(self.map, self.player_x, self.player_y, self.vision, '#', ' ')):
            line = ' ' * offset_x[0] + line + ' ' * offset_x[1]
            self.screen.print_at(line, 0, offset_y + i)

        for i in range(offset_y + len(self.map), self.screen.height):
            self.screen.print_at(" " * self.screen.width, 0, i)

        self.screen.print_at("@", self.screen.width // 2, self.screen.height // 2)

    @property
    def frame_update_count(self) -> int:
        """Required function for Effects."""
        # No animation required.
        return 0

    @property
    def stop_frame(self) -> int:
        """Required function for Effects."""
        # No specific end point for this Effect. Carry on running forever.
        return 0

    def reset(self) -> None:
        """Required function for Effects."""
        # Nothing special to do. Just need this to satisfy the ABC.
        pass


class GameController(Scene):
    """
    Class responsible for moving the player along the map
    and controlling the game in general.
    """

    # Control collisions
    EMPTY_SPACE = 0
    CORRECT_WALL = 1
    WRONG_WALL = 2
    WALL = (CORRECT_WALL, WRONG_WALL)

    # Control game ending
    WRONG_TAGS = 100
    CORRECT_TAGS = 101
    NOT_FINISHED = 102

    # Here we decide the signal each sprite sends to the game
    SPRITE_MAP = {
        " ": EMPTY_SPACE,
        ".": EMPTY_SPACE,
        ",": EMPTY_SPACE,
        "X": WRONG_WALL,
        "#": WRONG_WALL,
        "|": WRONG_WALL,
    }

    # Phrases spoken when the character tags walls
    SPEECH = {
        # TODO: we can implement various different speeches
        # and pick one at random
        ord('A'): "Is this the left wall?",
        ord('D'): "Is this the right wall?",
        ord('W'): "Is this the upper wall?",
        ord('S'): "Is this the lower wall?",
    }

    def __init__(self, screen: Screen, level: int):
        self.screen = screen
        self.map = Map(screen, LEVELS[level])
        effects = [
            self.map,
        ]
        # Walls tagged by the player,
        # if he tags the 4 outer walls correctly
        # he realizes he is in a box and finish the level
        self.tagged_walls = {}
        self.level = level
        super(GameController, self).__init__(effects, -1)

    def cast_ray(self, direction: Tuple[int], pos: Optional[List[int]] = None) -> int:
        """
        Cast a ray into 'direction' starting from 'pos';
        if 'pos' is not specified we default to player pos.
        """
        if pos is None:
            pos = [self.map.player_x, self.map.player_y]

        x = direction[0] + pos[0]
        y = direction[1] + pos[1]

        # If we tag the border of the map, we've hit the right wall
        if (
                x in (0, len(self.map.map[0])-1)
                or y in (0, len(self.map.map)-1)
        ):
            return GameController.CORRECT_WALL

        # If not, we send the information of that location
        return GameController.SPRITE_MAP.get(
            self.map.map[y][x],
            GameController.EMPTY_SPACE,
        )

    def speak(self, text: str, duration: int = 20) -> None:
        """Text to be spoken by the character"""
        linebreaks = text.count("\n")

        self.add_effect(
            Print(
                self.screen,
                SpeechBubble(text, "L"),
                self.screen.height // 2 - 4 - linebreaks,
                self.screen.width // 2 + 2,
                transparent=False,
                clear=True,
                delete_count=duration,
            ),
        )

    def check_level_completion(self) -> int:
        """
        Check if the player finished the level
        How it works:
        1 - If the player has not tagged the 4 walls (up, down, left, right)
            we return NOT_FINISHED so he can keep playing
        2 - If he tagged all 4 walls but at least 1 is wrong we return
            WRONG_TAGS, he will receive a message that he is wrong and have to guess again
        3 - If he tagged everything right, he gets CORRECT_TAGS and ends the level
        """
        directions = ("l", "r", "u", "d")
        res = GameController.CORRECT_TAGS

        for direction in directions:
            if direction not in self.tagged_walls:
                return GameController.NOT_FINISHED
            if not self.tagged_walls[direction]:
                res = GameController.WRONG_TAGS

        return res

    def process_event(self, event: Event) -> Optional[Event]:
        """Process events, mostly player input."""
        # Allow standard event processing first
        if super(GameController, self).process_event(event) is None:
            return

        # If that didn't handle it, check for a key that this demo understands.
        if isinstance(event, KeyboardEvent):
            key_code = event.key_code
            speech = None
            recognised = False  # Flag for if the key code is recognised

            # Iterate over the mappings, check to see if the key_code is
            # a movement or tag trigger key, then perform actions accordingly.
            for dm_mapping in DIRECTIONAL_MANEUVER_MAPPINGS:
                if key_code in dm_mapping["movement_trigger_keys"]:
                    if (
                            self.cast_ray(dm_mapping["raycast_direction"])
                            == GameController.EMPTY_SPACE
                    ):
                        axis, move = dm_mapping["map_movement"]
                        # Using setattr and getattr for dynamic attribute assignment
                        attr = (self.map, f"player_{axis}")
                        setattr(*attr, getattr(*attr) + move)

                    recognised = True
                    break

                if key_code in dm_mapping["tag_trigger_keys"]:
                    collision = self.cast_ray(dm_mapping["raycast_direction"])

                    if collision in GameController.WALL:
                        speech = GameController.SPEECH[key_code]
                    # If not colliding with a correct wall, assign False,
                    # True otherwise.
                    self.tagged_walls[dm_mapping["wall"]] = collision == GameController.CORRECT_WALL

                    recognised = True
                    break

            check = self.check_level_completion()
            if check == GameController.CORRECT_TAGS:
                self.speak("I knew it!\nI was in a box all along!")
                self.tagged_walls = {}
                raise exceptions.EnterLevel(self.level + 1)
            elif check == GameController.WRONG_TAGS:
                self.speak("Hmm... I don't think this is right.")
                self.tagged_walls = {}
            else:
                if speech is not None:
                    self.speak(speech)

            if not recognised:
                # Not a recognised key - pass on to other handlers.
                return event

        else:
            # Ignore other types of events.
            return event


def game_IH(event: Event) -> Optional[Event]:
    """Handle extra in-game inputs"""
    if isinstance(event, KeyboardEvent):
        key = event.key_code
        if key in [ord("q"), ord("Q"), Screen.KEY_ESCAPE]:
            raise exceptions.LevelSelector()
    return event
