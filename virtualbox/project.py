from functions.command_functions import get_entry
from functions.blessed_functions import print_tree, clear_term, echo, print_box, print_loading, request
from time import sleep
from users.user import User, ROOT
from users.uid import Uidspace
from users.login import login
from exceptions import CannotFullFillFunction
from config import START_PATH
from copy import copy
from fs.fs_dir import Dir
from playsound import playsound
from blessed import Terminal
import threading
from shutil import copytree, rmtree
from os import getcwd


def playbgm():
    playsound('music/bgm_part01.mp3', block=False)
    sleep(40)
    while True:
        playsound('music/bgm_part02.mp3', block=False)
        sleep(16)


# file system imports
fs = Dir.FromPath(START_PATH, None, 7, 0, 0)
# Users uid space
users_uid_space = Uidspace(1)
# User
Users = User.loadUsers(ROOT, fs, users_uid_space)
Users[ROOT.name] = ROOT
# Term
term = Terminal()


def ProcessArgs(functionArgs, argsDicit):
    try:
        return [argsDicit[i] for i in functionArgs]
    except KeyError:
        raise CannotFullFillFunction()


# COMMAND MANAGER
def user_input_cmd(fs, user, rootfs, term):
    while True:
        user_input = request(">>>  ", term).strip().split()
        if len(user_input) == 0:
            continue
        try:
            clear_term(term)
            entry = get_entry(user_input[0])
            entry[0](*ProcessArgs(entry[1], locals()))
        except Exception as e:
            echo(e, term)


def start(fs, user, term):
    firstgamefile = open('first_game.txt', 'r')
    content = firstgamefile.readline()
    print_loading('Loading Operating System:', term)
    clear_term(term)
    if content[0] == '0':
        print_box('Intro',
           [' You are Netsec architect working for the USA, you just managed to get into a System controlling the Atomic Program of the Iran. Originally your job was to analyze the Data and to find out if there are any files which could gives hints to imminent nuclear attacks.'], term)
        input()
        clear_term(term)
        print_box('Intro',
           [' You realise that there wil be an stealth launch attack very soon, it is targeted at Europe. You will not have enough time to contact the European agency. Your only chance to stop this is to deactivate it yourself.'], term)
        input()
        clear_term(term)
        print_box('Intro',
           [' The system has a built in artificial intelligence built to stop intruders. It will work against you and try to stop you. You will need to hack this system and gain root access and shut down the nuclear launch so that you have enough time to warn the EA.'], term)
        input()
        clear_term(term)
        print_box('Intro',
                ['Booting OS drive...',
                 '',
                 '',
                 '',
                 ''], term)
        sleep(0.5)
        clear_term(term)
        print_box('Intro',
                  ['Booting OS drive... COMPLETE',
                   'Securing connection...',
                   '',
                   '',
                   ''], term)
        sleep(0.5)
        clear_term(term)
        print_box('Intro',
                  ['Booting OS drive... COMPLETE',
                   'Securing Connection...COMPLETE',
                   'Clearing Entry Logs...',
                   '',
                   ''], term)
        sleep(0.5)
        clear_term(term)
        print_box('Intro',
                  ['Booting OS drive... COMPLETE',
                   'Securing Connection...COMPLETE',
                   'Clearing Entry Logs...COMPLETE',
                   'INITIALIZING ANTI-THREAT AI...',
                   ''], term)
        sleep(0.5)
        clear_term(term)
        print_box('Intro',
                  ['Booting OS drive... COMPLETE',
                   'Securing Connection...COMPLETE',
                   'Clearing Entry Logs...COMPLETE',
                   'INITIALIZING ANTI-THREAT AI...COMPLETE',
                   ''], term)
        sleep(0.5)
        clear_term(term)
        print_box('Intro',
                  ['Booting OS drive... COMPLETE',
                   'Securing Connection...COMPLETE',
                   'Clearing Entry Logs...COMPLETE',
                   'INITIALIZING ANTI-THREAT AI...COMPLETE',
                   'Welcome operator. Press Enter to coninue'], term)
        input()
        clear_term(term)
        echo('This is the file tree, here, you can see every file in the operating system!', term)
        print_tree("System", fs, user, term)
        echo('First, type "help" in the console to see all of the commands you can use!', term)
        echo('If you would like a tutorial type "tutorial" or "t"', term)
        with open('first_game.txt', 'w') as firstgamefile:
            firstgamefile.truncate()
            firstgamefile.write('1')
            echo('SYSTEM HACKED username = user, password = 1234567', term)
    else:
        print_box('Welcome Back', ['', 'Your Game-State was loaded again! ', ''], term)
        echo('SYSTEM HACKED username = user, password = 1234567', term)


def main():
    global fs
    # resets os directory to initial
    current_dir = getcwd()
    src = current_dir + '/default-files'
    dest = current_dir + '/OS'
    rmtree(dest)
    copytree(src, dest)

    # start game
    start(fs, ROOT, term)
    user_input_cmd(copy(fs), login(Users, term), fs, term)


if __name__ == "__main__":
    t1 = threading.Thread(target=main)
    t2 = threading.Thread(target=playbgm)
    t1.start()
    t2.start()