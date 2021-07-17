from os import system

import blessed.keyboard
from blessed import Terminal
from pygame.time import Clock, wait
from math import ceil

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
        with terminal.cbreak(), terminal.hidden_cursor(), terminal.fullscreen():
            val: blessed.keyboard.Keystroke = terminal.inkey(timeout=1 / fps)
            while val != 'q':
                if map.time_left < 0:
                    print(terminal.move_xy(40, 15), terminal.white_on_firebrick3("Time's up! Try again!"))
                    wait(3000)
                    level = 1
                    break
                elif map.space.targets_engaged != len(map.space.targets):
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
                    if not map.space.player_in_thinkingbox:
                        map.sync_coords()
                        map.draw()
                        map.time_left -= 1 / fps
                        time_left = terminal.move_xy(48, 2) + terminal.lightcyan(terminal.on_midnightblue(str(int(map.time_left / 60)) + ":" + str(int(map.time_left % 60))))
                        print(time_left)
                    else:
                        print(terminal.home + terminal.on_gray20 + terminal.clear)
                        time_left = terminal.move_xy(48, 2) + terminal.lightcyan(terminal.on_gray20(str(int(map.time_left / 60)) + ":" + str(int(map.time_left % 60))))
                        info = terminal.move_xy(10, 10) +  terminal.lightcyan(terminal.on_gray20('You are inside the thinking box. The time has stopped'))
                        map.thinking_box.draw_inside_box()
                        map.player.draw_inside_box()
                        print(info + time_left)

                    clock.tick(fps)
                    val = terminal.inkey(timeout=1 / fps)
                else:
                    print(terminal.move_xy(40, 15), terminal.white_on_firebrick3('Well done! Level completed.'))
                    wait(3000)
                    level += 1
                    break

def run_tutorial():
    val = terminal.inkey(timeout=1 / fps)
    while val != 'q':
        val = terminal.inkey(timeout=1/fps)
        tutorial = terminal.move_xy(40, 5) +  terminal.lightcyan(terminal.on_darkslategray4('TUTORIAL'))
        info1 = terminal.move_xy(20, 10) +  terminal.lightcyan(terminal.on_darkslategray('The purpose of the game is to push the boxes until all targets have a box inside. Make sure to finish it in time. If you want to think about the level, enter the gray thinking box and the timer will stop.'))
        info2 = terminal.move_xy(20, 17) +  terminal.lightcyan(terminal.on_darkslategray('MOVEMENT: use A and D or left and right arrow keys to move. Use W and up arrow to jump and S and down arrow to cancel the jump'))
        exit = terminal.move_xy(20, 20) + terminal.lightcyan(terminal.on_darkslategray('Press q to exit. You can use q to quit the main game and the menu too.'))
        print(tutorial + info2 + info1 + exit, flush=True)
        

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
                    print(terminal.home + terminal.lightcyan_on_darkslategray + terminal.clear)
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
