from os import system

import blessed.keyboard
from blessed import Terminal
from pygame.time import Clock, wait

from maps import Map

terminal = Terminal()
fps = 120


def main():
    system("resize -s 30 100 | 2> /dev/null")

    map = Map(terminal)
    map.create_level1()

    clock = Clock()
    with terminal.cbreak(), terminal.hidden_cursor(), terminal.fullscreen():
        val: blessed.keyboard.Keystroke = terminal.inkey(timeout=1/fps)
        while val != 'q':
            if map.space.targets_to_engage:
                if val.name == "KEY_UP" or val.name == "KEY_w":
                    map.space.move_player(map.player_rect, key="up")
                if val.name == "KEY_DOWN" or val.name == "KEY_s":
                    map.space.move_player(map.player_rect, key="down")
                if val.name == "KEY_LEFT" or val.name == "KEY_a":
                    map.space.move_player(map.player_rect, key="left")
                if val.name == "KEY_RIGHT" or val.name == "KEY_d":
                    map.space.move_player(map.player_rect, key="right")

                map.space.step(fps)
                map.delete()
                map.sync_coords()
                map.draw()
                clock.tick(fps)
                val = terminal.inkey(timeout=1/fps)
            else:
                print(terminal.white_on_firebrick3('Well done! Level completed.'))
                wait(3000)
                break


system("clear")
main()
system("clear")
