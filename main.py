from os import system

from blessed import Terminal
from pygame.time import Clock, wait

from maps import Map

terminal = Terminal()
fps = 60


def main():
    system("resize -s 30 100 | 2> /dev/null")

    map = Map(terminal)
    map.create_level1()

    clock = Clock()
    with terminal.cbreak(), terminal.hidden_cursor():
        print(terminal.home + terminal.on_midnightblue + terminal.clear)
        print(terminal.is_term_resized(100, 100))
        val = terminal.inkey(timeout=1/fps)
        while val != 'q':
            map.delete()
            if len(map.space.targets_to_engage) != 0:
                val = terminal.inkey(timeout=0.01)
                if val.name == "KEY_UP" or val.name == "KEY_DOWN" or val.name == "KEY_RIGHT" or val.name == "KEY_LEFT":
                    map.space.move_player(val)
                map.sync_coords()
                map.draw()
                map.space.step(60)
                clock.tick(60)
            else:
                print(terminal.white_on_firebrick3('Well done! Level completed.'))
                wait(3000)


system("clear")
main()
system("clear")
