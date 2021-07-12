from os import system

from blessed import Terminal
from sprites import Player, ThinkingBox
from sprites import Platform
from sprites import Box
from sprites import Target

terminal = Terminal()

class Map:
    def __init__(self):
        self.player = 0
        self.thinking_box = 0
        self.boxes = []
        self.targets = []
        self.platforms = []

    def create_level1(self, terminal):
        self.targets = []
        self.boxes = []
        self.platforms = []
        self.player = Player(10 , 26)
        self.thinking_box = ThinkingBox(15, 26, terminal)
        

        box1 = Box(54,21, terminal)
        box2 = Box(70, 27, terminal)
        self.boxes.append(box1)
        self.boxes.append(box2)

        platform1 = Platform(50, 23, 30, True, terminal)
        border1 = Platform(0, 29, 100, True, terminal)
        self.platforms.append(platform1)
        self.platforms.append(border1)

        target1 = Target(70, 21, terminal)
        target2 = Target(90, 27, terminal)
        self.targets.append(target1)
        self.targets.append(target2)

    def draw(self, terminal):
            self.thinking_box.draw()
            for target in self.targets:
                target.draw()
            self.player.draw(terminal)
            for platform in self.platforms:
                platform.draw()
            for box in self.boxes:
                box.draw()


def main():
    system("resize -s 30 100 | 2> /dev/null")
    map = Map()
    map.create_level1(terminal)
    with terminal.cbreak(), terminal.hidden_cursor():
        print(terminal.home + terminal.on_midnightblue + terminal.clear)
        print(terminal.is_term_resized(100, 100))
        val = terminal.inkey(timeout=0.02)
        while val != 'q':
            val = terminal.inkey(timeout=0.02)
            map.player.move(val, terminal)
            map.draw(terminal)


system("clear")
main()
system("clear")
