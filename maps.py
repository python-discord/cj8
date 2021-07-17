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
THINKINGBOX_W = 8
THINKINGBOX_H = 3


class Map:
    def __init__(self, terminal: Terminal):
        self.terminal = terminal
        self.player = None
        self.player_rect: physics2.Object
        self.thinking_box = None
        self.boxes = []
        self.boxes_rect: List[physics2.Object] = []
        self.targets = []
        self.platforms = []
        self.space = physics2.Space(100, 30, gravity=10, upscale=100)
        self.time_left = 0  # you should always use the ceil() of this variable to get the integer number of seconds left

    def create_level1(self):
        self.player = Player(10, 26, self.terminal)
        player_rect = self.space.add_object(10, 26, PLAYER_W, PLAYER_H, type="player")
        self.player_rect = player_rect

        self.thinking_box = ThinkingBox(15, 26, self.terminal)
        self.space.add_object(15, 26, THINKINGBOX_W, THINKINGBOX_H, type="thinkingbox")

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
        self.space.add_object(90, 27, TARGET_W, TARGET_H, type="target")
        self.targets.append(target1)
        self.targets.append(target2)

        self.time_left = 120

    def create_level2(self):
        self.player = Player(35, 4, self.terminal)
        player_rect = self.space.add_object(35, 4, PLAYER_W, PLAYER_H, type="player")
        self.player_rect = player_rect

        self.thinking_box = ThinkingBox(20, 4, self.terminal)
        self.space.add_object(20, 4, THINKINGBOX_W, THINKINGBOX_H, type="thinkingbox")

        box1 = Box(6, 5, self.terminal)
        box1_rect = self.space.add_object(6, 5, BOX_W, BOX_H, type="box")
        self.boxes_rect.append(box1_rect)
        self.boxes.append(box1)

        box2 = Box(47, 12, self.terminal)
        box2_rect = self.space.add_object(47, 12, BOX_W, BOX_H, type="box")
        self.boxes_rect.append(box2_rect)
        self.boxes.append(box2)
        box3 = Box(55, 12, self.terminal)
        box3_rect = self.space.add_object(55, 12, BOX_W, BOX_H, type="box")
        self.boxes_rect.append(box3_rect)
        self.boxes.append(box3)


        border1 = Platform(0, 29, 100, True, self.terminal)
        self.space.add_object(0, 29, 100, PLATFORM_H, type="platform")
        self.platforms.append(border1)
        
        platform1 = Platform(0, 7, 40, True, self.terminal)
        self.space.add_object(0, 7, 40, PLATFORM_H, type="platform")
        self.platforms.append(platform1)

        platform2 = Platform(0, 26, 40, True, self.terminal)
        self.space.add_object(0, 26, 40, PLATFORM_H, type="platform")
        self.platforms.append(platform2)

        platform3 = Platform(44, 14, 30, True, self.terminal)
        self.space.add_object(44, 14, 30, PLATFORM_H, type="platform")
        self.platforms.append(platform3)

        target1 = Target(36, 27, self.terminal)
        self.space.add_object(36, 27, TARGET_W, TARGET_H, type="target")
        self.targets.append(target1)
        target1 = Target(90, 27, self.terminal)
        self.space.add_object(90, 27, TARGET_W, TARGET_H, type="target")
        self.targets.append(target1)
        target1 = Target(0, 24, self.terminal)
        self.space.add_object(70, 21, TARGET_W, TARGET_H, type="target")
        self.targets.append(target1)

        self.time_left = 120

    def create_level3(self):
        self.player = Player(25, 4, self.terminal)
        player_rect = self.space.add_object(25, 4, PLAYER_W, PLAYER_H, type="player")
        self.player_rect = player_rect

        self.thinking_box = ThinkingBox(15, 4, self.terminal)
        self.space.add_object(15, 4, THINKINGBOX_W, THINKINGBOX_H, type="thinkingbox")
        
        border1 = Platform(0, 29, 100, True, self.terminal)
        self.space.add_object(0, 29, 100, PLATFORM_H, type="platform")
        self.platforms.append(border1)

        platform1 = Platform(0, 7, 40, True, self.terminal)
        self.space.add_object(0, 7, 40, PLATFORM_H, type="platform")
        self.platforms.append(platform1)

        platform2 = Platform(44, 10, 40, True, self.terminal)
        self.space.add_object(44, 10, 40, PLATFORM_H, type="platform")
        self.platforms.append(platform2)

        platform3 = Platform(0, 16, 40, True, self.terminal)
        self.space.add_object(0, 16, 40, PLATFORM_H, type="platform")
        self.platforms.append(platform3)

        platform4 = Platform(0, 24, 40, True, self.terminal)
        self.space.add_object(0, 24, 40, PLATFORM_H, type="platform")
        self.platforms.append(platform4)

        platform5 = Platform(44, 24, 40, True, self.terminal)
        self.space.add_object(44, 24, 40, PLATFORM_H, type="platform")
        self.platforms.append(platform5)

        box1 = Box(35, 5, self.terminal)
        box1_rect = self.space.add_object(35, 5, BOX_W, BOX_H, type="box")
        self.boxes_rect.append(box1_rect)
        self.boxes.append(box1)

        box2 = Box(50, 8, self.terminal)
        box2_rect = self.space.add_object(50, 8, BOX_W, BOX_H, type="box")
        self.boxes_rect.append(box2_rect)
        self.boxes.append(box2)
        box3 = Box(60, 8, self.terminal)
        box3_rect = self.space.add_object(60, 8, BOX_W, BOX_H, type="box")
        self.boxes_rect.append(box3_rect)
        self.boxes.append(box3)

        box4 = Box(20, 14, self.terminal)
        box4_rect = self.space.add_object(20, 14, BOX_W, BOX_H, type="box")
        self.boxes_rect.append(box4_rect)
        self.boxes.append(box4)

        target1 = Target(0, 27, self.terminal)
        self.space.add_object(0, 27, TARGET_W, TARGET_H, type="target")
        self.targets.append(target1)
        target2 = Target(0, 25, self.terminal)
        self.space.add_object(0, 25, TARGET_W, TARGET_H, type="target")
        self.targets.append(target2)
        target3 = Target(0, 22, self.terminal)
        self.space.add_object(0, 22, TARGET_W, TARGET_H, type="target")
        self.targets.append(target3)
        target4 = Target(90, 27, self.terminal)
        self.space.add_object(90, 27, TARGET_W, TARGET_H, type="target")
        self.targets.append(target4)

        self.time_left = 120

    def delete(self):
        print(self.terminal.home + self.terminal.on_midnightblue + self.terminal.clear(), flush=True)

    def sync_coords(self):
        self.player.x, self.player.y = self.player_rect.get_position()
        for i, box in enumerate(self.boxes):
            box.x, box.y = self.boxes_rect[i].get_position()

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
        self.player = 0
        self.player_rect = None
        self.targets = []
        self.thinking_box = None
        self.boxes = []
        self.boxes_rect = []
        self.platforms = []
        self.space.reset()
