from typing import List

import pymunk
from blessed import Terminal

import physics
from sprites import Box, Platform, Player, Target, ThinkingBox


class Map:
    def __init__(self, terminal: Terminal):
        self.terminal = terminal
        self.player = 0
        self.thinking_box = 0
        self.boxes = []
        self.targets = []
        self.platforms = []

    def create_level1(self):
        self.player = Player(10, 26, self.terminal)
        self.player_p = self.space.add_object((10, 26), type="player")

        self.thinking_box = ThinkingBox(15, 26, self.terminal)

        box1 = Box(54, 21, self.terminal)
        box2 = Box(70, 27, self.terminal)
        self.boxes.append(box1)
        self.boxes.append(box2)

        platform1 = Platform(50, 23, 30, True, self.terminal)
        border1 = Platform(0, 30, 100, True, self.terminal)
        self.platforms.append(platform1)
        self.platforms.append(border1)

        target1 = Target(70, 21, self.terminal)
        target2 = Target(90, 27, self.terminal)
        self.targets.append(target1)
        self.targets.append(target2)
    
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
        print(self.terminal.home + self.terminal.on_midnightblue + self.terminal.clear(),flush=True)


    def draw(self):
        string = ""
        string+=self.thinking_box.draw()
        for target in self.targets:
            string+=target.draw()
        string+=self.player.draw()
        for platform in self.platforms:
            string+=platform.draw()
        for box in self.boxes:
            string+=box.draw()
        print(string,flush=True)

    def clear_level(self):
        self.targets = []
        self.boxes = []
        self.platforms = []
