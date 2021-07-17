import threading
from copy import copy
from time import sleep

from blessed import Terminal

from virtualbox.config import START_PATH
from virtualbox.exceptions import CannotFullFillFunction
from virtualbox.fs.fs_dir import Dir
from virtualbox.functions.blessed_functions import (
    clear_term, echo, print_box, print_loading, print_tree, request
)
from functions.command_functions import get_entry
from playsound import playsound

from blessed import Terminal
import threading
from shutil import copytree, rmtree
from os import getcwd


from virtualbox.functions.command_functions import get_entry
from virtualbox.users.login import login
from virtualbox.users.uid import Uidspace
from virtualbox.users.user import ROOT, User




def playbgm():
    playsound('music/bgm_part01.mp3', block=False)
    sleep(40)
    while True:
        playsound('music/bgm_part02.mp3', block=False)
        sleep(16)

# file system imports
fs = Dir.FromPath(START_PATH, None, 7, 5, 0)
# Users uid space
users_uid_space = Uidspace(1)
# User
Users = User.loadUsers(ROOT, fs, users_uid_space)
Users[ROOT.name] = ROOT
# Term
term = Terminal()


def ProcessArgs(functionArgs: tuple, argsDicit: dict) -> list:
    """Procceses functions argumens to allow 'imports'"""
    try:
        return [argsDicit[i] for i in functionArgs]
    except KeyError:
        raise CannotFullFillFunction()


# COMMAND MANAGER
def user_input_cmd(fs: Dir, user: User, rootfs: Dir, term: Terminal) -> None:
    """Shell"""
    while True:
        user_input = request(">>>  ", term).strip().split()
        if len(user_input) == 0:
            continue
        try:
            clear_term(term)
            entry = get_entry(user_input[0])
            entry[0](*ProcessArgs(entry[1], {**locals(), **globals()}))
        except Exception as e:
            echo(e, term)



def start(fs: Dir, user: User, term: Terminal) -> None:
    """Prints game intro or welcome message"""
    firstgamefile = open('first_game.txt', 'r')
    content = firstgamefile.readline()
    print_loading('Loading Operating System:', term)
    clear_term(term)
    if content[0] == '0':

        x = [['You are Netsec architect working for the NSA']]
        x[-1] += [', you just managed to get into a System controlling the Atomic Program of the Iran.']
        x[-1] += ['Originally your job was to analyze the Data and to find out if there are any files']
        x[-1] += ['which could gives hints to imminent nuclear attacks.']
        x += [[' You realise that there wil be an stealth launch attack very soon, it is targeted at Europe.']]
        x[-1] += ['You will not have enough time to contact the European agency.']
        x[-1] += [' Your only chance to stop this is to deactivate it yourself.']
        x += [[' The system has a built in artificial intelligence built to stop intruders.']]
        x[-1] += ['It will work against you and try to stop you.']
        x[-1] += ['You will need to hack this system and gain root access and shut down the nuclear launch'],
        x[-1] += ['so that you have enough time to warn the EA.']

        for i in x:
            clear_term(term)
            print_box('Intro', i, term)
            request(term)

        x = ['Booting OS drive...']
        x += ['Securing connection...']
        x += ['Clearing Entry Logs...']
        x += ['INITIALIZING ANTI-THREAT AI...'],
        x += ['INITIALIZING ANTI-THREAT AI...COMPLETE']
        x += ['Welcome operator. Press Enter to continue']

        for i in range(len(x)):
            sleep(0.5)
            clear_term(term, x[:i + 1])
            print_box('Intro')

        request(term)
        clear_term(term)
        echo('This is the file tree. Here, you can see every file in the operating system.', term)
        print_tree("System", fs, user, term)
        echo('First, type "help" in the console to see all of the commands you can use!', term)
        echo('If you would like a tutorial type "tutorial" or "t"', term)

        with open('first_game.txt', 'w') as firstgamefile:
            firstgamefile.truncate()
            firstgamefile.write('1')
            echo('SYSTEM HACKED username = user, password = 1234567', term)
    else:
        print_box('Welcome Back', ['', 'Your game state is reloaded.', ''], term)
        echo('SYSTEM HACKED username = user, password = 1234567', term)


def main() -> None:
    """Main function"""
    global fs
    # resets os directory to initial
    # current_dir = getcwd()
    # src = current_dir + '/default-files'
    # dest = current_dir + '/OS'
    # rmtree(dest)
    # copytree(src, dest)

    # start game
    start(fs, ROOT, term)
    user_input_cmd(copy(fs), login(Users, term), fs, term)


if __name__ == "__main__":
    t1 = threading.Thread(target=main)
    t2 = threading.Thread(target=playbgm)
    t1.start()
    t2.start()
