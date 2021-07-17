from typing import List

from blessed import Terminal

import physics2
import sprites
from sprites import Box, Platform, Player, Target, ThinkingBox

PLAYER_W = 4
PLAYER_H = 3
BOX_W = 4
BOX_H = 2
TARGET_W = 2
TARGET_H = 2
PLATFORM_H = 1


class Map:
    def __init__(self, terminal: Terminal):
        self.terminal = terminal
        self.player = 0
        self.player_rect: physics2.Object
        self.thinking_box = 0
        self.boxes = []
        self.boxes_rect: List[physics2.Object] = []
        self.targets = []
        self.platforms = []
        self.space = physics2.Space(100, 30, gravity=20, upscale=100)

    def create_level1(self):
        self.player = Player(10, 26, self.terminal)
        player_rect = self.space.add_object(10, 26, PLAYER_W, PLAYER_H, type="player")
        self.player_rect = player_rect

        self.thinking_box = ThinkingBox(15, 26, self.terminal)

        box1 = Box(54, 21, self.terminal)
        box1_rect = self.space.add_object(54, 21, BOX_W, BOX_H, type="box")
        self.boxes_rect.append(box1_rect)
        box2 = Box(70, 27, self.terminal)
        box2_rect = self.space.add_object(70, 27, BOX_W, BOX_H, type="box")
        self.boxes_rect.append(box2_rect)
        self.boxes.append(box1)
        self.boxes.append(box2)

        platform1 = Platform(50, 23, 30, True, self.terminal)
        self.space.add_object(50, 23, 30, PLATFORM_H, type="platform")
        border1 = Platform(0, 29, 100, True, self.terminal)
        self.space.add_object(0, 29, 100, PLATFORM_H, type="platform")
        self.platforms.append(platform1)
        self.platforms.append(border1)

        target1 = Target(70, 21, self.terminal)
        self.space.add_object(70, 21, TARGET_W, TARGET_H, type="target")
        target2 = Target(90, 27, self.terminal)
        self.space.add_object(90, 27, TARGET_W, TARGET_H,type="target")
        self.targets.append(target1)
        self.targets.append(target2)

    def sync_coords(self):
        self.player.x, self.player.y = self.player_rect.get_position()
        for i, box in enumerate(self.boxes):
            box.x, box.y = self.boxes_rect[i].get_position()

    def create_level2(self):
        self.player = Player(10, 26, self.terminal)

        self.thinking_box = ThinkingBox(15, 26, self.terminal)

        border1 = Platform(0, 30, 100, True, self.terminal)
        platform1 = Platform(0, 7, 20, True, self.terminal)
        platform2 = Platform(0, 25, 20, True, self.terminal)
        self.platforms.append(platform1)
        self.platforms.append(platform2)
        self.platforms.append(border1)

    def delete(self):
        print(self.terminal.home + self.terminal.on_midnightblue + self.terminal.clear(), flush=True)

    def draw(self):
        string = ""
        string += self.thinking_box.draw()
        for target in self.targets:
            string += target.draw()
        string += self.player.draw()
        for platform in self.platforms:
            string += platform.draw()
        for box in self.boxes:
            string += box.draw()
        print(string, flush=True)

    def clear_level(self):
        self.targets = []
        self.boxes = []
        self.platforms = []
        self.space.reset()
