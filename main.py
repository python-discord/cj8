from pygame.time import Clock, wait
from os import system

from maps import Map
from blessed import Terminal

terminal = Terminal()
fps = 120


def main():
    system("resize -s 30 100 | 2> /dev/null")

    map = Map(terminal)
    map.create_level2()

    clock = Clock()
    with terminal.cbreak(), terminal.hidden_cursor(),terminal.fullscreen():
        val = terminal.inkey(timeout=1/fps)
        while val != 'q':
            map.delete() 
            map.draw()
            clock.tick(fps)
            val = terminal.inkey(timeout=1/fps)



system("clear")
main()
system("clear")