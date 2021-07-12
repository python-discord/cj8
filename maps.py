from typing import List

import pymunk
from blessed import Terminal

import physics
from sprites import Box, Platform, Player, Target, ThinkingBox


class Map:
    def __init__(self, terminal: Terminal):
        self.terminal = terminal
        self.player = 0
        self.player_p: pymunk.Poly
        self.thinking_box = 0
        self.boxes = []
        self.boxes_p: List[pymunk.Poly] = []
        self.targets = []
        self.platforms = []
        self.space = physics.MySpace()

    def create_level1(self, terminal):
        self.player = Player(10, 26)
        self.player_p = self.space.add_object((10, 26), type="player")

        self.thinking_box = ThinkingBox(15, 26, terminal)

        box1 = Box(54, 21, terminal)
        box1_p = self.space.add_object((54, 21), type="box")
        self.boxes_p.append(box1_p)
        box2 = Box(70, 27, terminal)
        box2_p = self.space.add_object((70, 27), type="box")
        self.boxes_p.append(box2_p)
        self.boxes.append(box1)
        self.boxes.append(box2)

        platform1 = Platform(50, 23, 30, True, terminal)
        self.space.add_object((50, 23), type="platform", w=30)
        border1 = Platform(0, 29, 100, True, terminal)
        self.space.add_object((0, 29), type="platform", w=100)
        self.platforms.append(platform1)
        self.platforms.append(border1)

        target1 = Target(70, 21, terminal)
        self.space.add_object((70, 22.99), type="target")
        target2 = Target(90, 27, terminal)
        self.space.add_object((70, 29.99), type="target")
        self.targets.append(target1)
        self.targets.append(target2)

    def sync_coords(self):
        self.player.x, self.player.y = physics.get_position(self.player_p)
        for i, box in enumerate(self.boxes):
            box.x, box.y = physics.get_position(self.boxes_p[i])

    def draw(self, terminal):
        self.thinking_box.draw()
        for target in self.targets:
            target.draw()
        self.player.draw(terminal)
        for platform in self.platforms:
            platform.draw()
        for box in self.boxes:
            box.draw()

    def clear_level(self):
        self.targets = []
        self.boxes = []
        self.platforms = []
        self.space = physics.MySpace()
