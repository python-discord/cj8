from pygame.time import Clock, wait
from os import system

from maps import Map
from blessed import Terminal

terminal = Terminal()
fps = 120


def main():
    system("resize -s 30 100 | 2> /dev/null")

    map = Map(terminal)
    map.create_level1()

    clock = Clock()
    with terminal.cbreak(), terminal.hidden_cursor(),terminal.fullscreen():
        val = terminal.inkey(timeout=1/fps)
        while val != 'q':
            map.delete() 
            map.draw()
            map.space.step(fps)
            map.sync_coords()
            clock.tick(fps)
            if len(map.space.targets_to_engage) != 0:
                val = terminal.inkey(timeout=1/fps)
                if val.name == "KEY_UP" or val.name == "KEY_DOWN" or val.name == "KEY_RIGHT" or val.name == "KEY_LEFT":
                    map.space.move_player(val)
            else:
                print(terminal.white_on_firebrick3('Well done! Level completed.'))
                wait(3000)
                break


system("clear")
main()
system("clear")