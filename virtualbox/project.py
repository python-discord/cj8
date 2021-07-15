from functions.command_functions import random_test, get_entry
from functions.blessed_functions import print_tree, clear_term, printhelp_first, print_box, print_loading
from random import randint
from time import sleep
from users.user import User, ROOT
from users.uid import Uidspace
from exceptions import CannotFullFillFunction
from config import START_PATH
from copy import copy
from fs.fs_dir import Dir
from playsound import playsound
import threading


def playbgm():
    playsound('bgm_part01.mp3', block=False)
    sleep(40)
    while True:
        playsound('bgm_part02.mp3', block=False)
        sleep(16)


# file system imports
fs = Dir.FromPath(START_PATH, None, 7, 0, 0)

# Users uid space
users_uid_space = Uidspace(1)

# User
Users = User.loadUsers(ROOT, fs, users_uid_space)


def ProcessArgs(functionArgs, argsDicit):
    try:
        return [argsDicit[i] for i in functionArgs]
    except KeyError:
        raise CannotFullFillFunction()


# COMMAND MANAGER
def user_input_cmd(fs, user):
    while True:
        user_input = input(">>>  ").strip().split()
        if len(user_input) == 0:
            continue
        # try:
        # clear_term()
        # if randint(1, 30) == 1:
        #     random_test()
        entry = get_entry(user_input[0])
        entry[0](*ProcessArgs(entry[1], locals()))
        # except Exception as e:
        #    print(e)


def start(fs, user):
    firstgamefile = open('first_game.txt', 'r')
    content = firstgamefile.readline()
    print_loading('Loading Operating System ', '40')
    clear_term()
    if content[0] == '0':
        print_box('Intro',
           [' You are Netsec architect working for the USA, you just managed to get into a System controlling the Atomic Program of the Iran. Originally your job was to analyze the Data and to find out if there are any files which could gives hints to imminent nuclear attacks.'])
        input()
        clear_term()
        print_box('Intro',
           [' You realise that there wil be an stealth launch attack very soon, it is targeted at Europe. You will not have enough time to contact the European agency. Your only chance to stop this is to deactivate it yourself.'])
        input()
        clear_term()
        print_box('Intro',
           [' The system has a built in artificial intelligence built to stop intruders. It will work against you and try to stop you. You will need to hack this system and gain root access and shut down the nuclear launch so that you have enough time to warn the EA.'])
        input()
        clear_term()
        print_box('Intro',
                ['Booting OS drive...',
                 '',
                 '',
                 '',
                 ''])
        sleep(0.5)
        clear_term()
        print_box('Intro',
                  ['Booting OS drive... COMPLETE',
                   'Securing connection...',
                   '',
                   '',
                   ''])
        sleep(0.5)
        clear_term()
        print_box('Intro',
                  ['Booting OS drive... COMPLETE',
                   'Securing Connection...COMPLETE',
                   'Clearing Entry Logs...',
                   '',
                   ''])
        sleep(0.5)
        clear_term()
        print_box('Intro',
                  ['Booting OS drive... COMPLETE',
                   'Securing Connection...COMPLETE',
                   'Clearing Entry Logs...COMPLETE',
                   'INITIALIZING ANTI-THREAT AI...',
                   ''])
        sleep(0.5)
        clear_term()
        print_box('Intro',
                  ['Booting OS drive... COMPLETE',
                   'Securing Connection...COMPLETE',
                   'Clearing Entry Logs...COMPLETE',
                   'INITIALIZING ANTI-THREAT AI...COMPLETE',
                   ''])
        sleep(0.5)
        clear_term()
        print_box('Intro',
                  ['Booting OS drive... COMPLETE',
                   'Securing Connection...COMPLETE',
                   'Clearing Entry Logs...COMPLETE',
                   'INITIALIZING ANTI-THREAT AI...COMPLETE',
                   'Welcome operator. Press Enter to coninue'])
        input()
        clear_term()
        printhelp_first('This is the file tree, here, you can see every file in the operating system!')
        print_tree("System", fs, user)
        printhelp_first('First, type "help" in the console to see all of the commands you can use!')
        with open('first_game.txt', 'w') as firstgamefile:
            firstgamefile.truncate()
            firstgamefile.write('1')
    else:
        print_box('Welcome Back', ['', 'Your Game-State was loaded again! ', ''])



def main():
    global fs
    start(fs, ROOT)
    user_input_cmd(copy(fs), ROOT)


if __name__ == "__main__":
    t1 = threading.Thread(target=main)
    t2 = threading.Thread(target=playbgm)
    t1.start()
    t2.start()



