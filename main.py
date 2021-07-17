from os import system

import blessed.keyboard
from blessed import Terminal
from pygame.time import Clock, wait

from maps import Map

terminal = Terminal()
fps = 120
def run_game():
    map = Map(terminal)
    clock = Clock()
    level = 1
    val = terminal.inkey(timeout=1 / fps)
    while level < 4 and val != 'q':
        val = terminal.inkey(timeout=1 / fps)
        if level == 1:
            map.clear_level()
            map.create_level1()
        if level == 2:
            map.clear_level()
            map.create_level2()
        if level == 3:
            map.clear_level()
            map.create_level3()
        while val != 'q':
            val = terminal.inkey(timeout=1 / fps)
            clock.tick(fps)
            if map.space.targets_engaged != len(map.space.targets):
                if val.name == "KEY_UP" or val.name == "KEY_w":
                    map.space.move_player(map.player_rect, key="up")
                if val.name == "KEY_DOWN" or val.name == "KEY_s":
                    map.space.move_player(map.player_rect, key="down")
                if val.name == "KEY_LEFT" or val.name == "KEY_a":
                    map.space.move_player(map.player_rect, key="left")
                if val.name == "KEY_RIGHT" or val.name == "KEY_d":
                    map.space.move_player(map.player_rect, key="right")
                    map.space.step(fps)
                if not map.space.player_in_thinkingbox:
                    map.delete()
                    map.sync_coords()
                    map.draw()
                    map.time_left -= 1 / fps
            else:
                print(terminal.white_on_firebrick3('Well done! Level completed.'))
                wait(300)
                level += 1
                break

def run_tutorial():
    val = terminal.inkey(timeout=1 / fps)
    while val != 'q':
        pass
        

def menu():
    with terminal.cbreak(), terminal.hidden_cursor(), terminal.fullscreen():
        val: blessed.keyboard.Keystroke = terminal.inkey(timeout=1/fps)
        print(terminal.home + terminal.lightcyan_on_darkslategray + terminal.clear)
        index = 1
        while val != 'q':
            val = terminal.inkey(timeout=1/fps)
            if val.name == "KEY_UP":
                index -= 1
            if val.name == "KEY_DOWN":
                index += 1
            if index < 1:
                index = 3
            if index > 3:
                index = 1
            if val.name == "KEY_ENTER":
                if index == 1:
                    run_game()
                    print(terminal.home + terminal.lightcyan_on_darkslategray + terminal.clear)
                if index == 2:
                    run_tutorial()
                    print(terminal.home + terminal.lightcyan_on_darkslategray + terminal.clear)
                if index == 3:
                    break
                
            menu = terminal.move_xy(20 , 7) + terminal.lightcyan(terminal.on_darkslategray('MENU'))
            start = terminal.move_xy(20 , 10) + terminal.lightcyan(terminal.on_darkslategray('START GAME'))
            tutorial = terminal.move_xy(20, 11) +  terminal.lightcyan(terminal.on_darkslategray('TUTORIAL'))
            exit = terminal.move_xy(20, 13) + terminal.lightcyan(terminal.on_darkslategray('EXIT'))
            if index == 1:
                start = terminal.move_xy(20 , 10) + terminal.lightcyan(terminal.on_darkslategray4('START GAME'))
            if index == 2:
                tutorial = terminal.move_xy(20, 11) +  terminal.lightcyan(terminal.on_darkslategray4('TUTORIAL'))
            if index == 3:
                exit = terminal.move_xy(20, 13) +  terminal.lightcyan(terminal.on_darkslategray4('EXIT'))
            print(start + menu + tutorial + exit, flush=True)


def main():
    system("resize -s 30 100 | 2> /dev/null")
    menu()


system("clear")
main()
system("clear")
