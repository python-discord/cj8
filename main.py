from os import system
from blessed import Terminal
from pygame.time import Clock

import maps

terminal = Terminal()


def main():
    system("resize -s 30 100 | 2> /dev/null")
    map = maps.Map(terminal)
    map.create_level1(terminal)
    clock = Clock()
    with terminal.cbreak(), terminal.hidden_cursor():
        print(terminal.home + terminal.on_midnightblue + terminal.clear)
        print(terminal.is_term_resized(100, 100))
        val = terminal.inkey(timeout=0.02)
        while val != 'q':
            val = terminal.inkey(timeout=0.02)
            map.space.move_player(val)
            map.sync_coords()
            map.draw(terminal)
            map.space.step(60)
            clock.tick(60)


system("clear")
main()
system("clear")
