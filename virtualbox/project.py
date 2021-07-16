import threading
from copy import copy
from time import sleep

from blessed import Terminal
from config import START_PATH
from exceptions import CannotFullFillFunction
from fs.fs_dir import Dir
from functions.blessed_functions import (
    clear_term, echo, print_box, print_loading, print_tree, request
)
from functions.command_functions import get_entry
from playsound import playsound

from blessed import Terminal
import threading
from shutil import copytree, rmtree
from os import getcwd

from users.login import login
from users.uid import Uidspace
from users.user import ROOT, User



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
        print_box('Introduction',
           ['As a network security architect working for the USA, you broke into the system controlling '
            'the Atomic Program of Iran. Your job is to analyze the data and recognise any signs '
            'of imminent nuclear attacks.'], term)
        input()
        clear_term(term)
        print_box('Introduction',
           ['You found out that there is a secretive attack scheduled, targeting at Europe. '
            'There is barely any time left to report to the European agency. '
            'Your only chance to stop the attack is to deactivate the launch yourself.'], term)
        input()
        clear_term(term)
        print_box('Introduction',
           ['The system has a built in artificial intelligence programmed to stop intruders. '
            'It will work against you and try to stop you. '
            'Your mission is to hack the system and gain root access to shut down the nuclear launch. '], term)
        input()
        clear_term(term)
        print_box('Introduction',
                ['Booting OS drive...',
                 '',
                 '',
                 '',
                 ''], term)
        sleep(0.5)
        clear_term(term)
        print_box('Introduction',
                  ['Booting OS Drive... COMPLETE',
                   'Securing Connection...',
                   '',
                   '',
                   ''], term)
        sleep(0.5)
        clear_term(term)
        print_box('Introduction',
                  ['Booting OS Drive... COMPLETE',
                   'Securing Connection...COMPLETE',
                   'Clearing Entry Logs...',
                   '',
                   ''], term)
        sleep(0.5)
        clear_term(term)
        print_box('Introduction',
                  ['Booting OS Drive... COMPLETE',
                   'Securing Connection...COMPLETE',
                   'Clearing Entry Logs...COMPLETE',
                   'Initializing Anti-threat AI...',
                   ''], term)
        sleep(0.5)
        clear_term(term)
        print_box('Introduction',
                  ['Booting OS Drive... COMPLETE',
                   'Securing Connection...COMPLETE',
                   'Clearing Entry Logs...COMPLETE',
                   'Initializing Anti-threat AI...COMPLETE',
                   ''], term)
        sleep(0.5)
        clear_term(term)
        print_box('Introduction',
                  ['Booting OS Drive... COMPLETE',
                   'Securing Connection...COMPLETE',
                   'Clearing Entry Logs...COMPLETE',
                   'Initializing Anti-threat AI...COMPLETE',
                   '',
                   'Welcome, operator. Press Enter to coninue'], term)
        input()
        clear_term(term)
        echo('This is the file tree. Here, you can see every file in the operating system.', term)
        print_tree("System", fs, user, term)
        echo('First, type "help" or "h" in the console to see all the commands available.', term)
        echo('To see a tutorial, type "tutorial" or "t"', term)
        with open('first_game.txt', 'w') as firstgamefile:
            firstgamefile.truncate()
            firstgamefile.write('1')
            echo('SYSTEM HACKED username = user, password = 1234567', term)
    else:
        print_box('Welcome Back', ['', 'Your Game-State is loaded again.', ''], term)
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
