import logging
import math
import time
from typing import List, Callable, Tuple
import operator


class Object:
    def __init__(self, topleft: Tuple[int, int], w: int, h: int, type: str, mass: int = 1):
        self.topleft = topleft
        self.w = w
        self.h = h
        self.bottomright = tuple(map(operator.add, topleft, (w, h)))
        self.type = type
        self.mass = mass

    def update_pos(self, topleft: Tuple[int, int]):
        self.topleft = topleft
        self.bottomright = tuple(map(operator.add, topleft, (self.w, self.h)))


class Space:
    targets_to_engage: List[object] = []
    objects: List[object] = []

    def __init__(self, w: int, h: int, gravity: int):
        self.w = w
        self.h = h
        self.gravity = gravity

    def add(self, object):
        pass

    def check_collisions(self) -> List[object]:
        pass

    def resolve_collisions(self, collisions: List[object]):
        pass

    def move_player(self, player: Object, key: str):
        pass

    def step(self, fps: int):
        collisions = self.check_collisions()
        self.resolve_collisions(collisions)


class Collision:
    def __init__(self, object_a: Object, object_b: Object):
        self.object_a = object_a
        self.object_b = object_b

    def resolve(self) -> bool:  # returns a boolean to indicate whether the solution was successful
        pass
