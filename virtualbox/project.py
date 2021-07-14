
from functions.command_functions import user_commands, random_test
from functions.blessed_functions import print_tree, clear_term, printstart, printhelp_first, print_box
from exceptions import CannotFullFillFunction
from config import START_PATH
from random import randint
from time import sleep


from fs.fs_dir import Dir

# file system imports
fs = Dir.FromPath(START_PATH, None, 7, 0, 0)


class User:
    """temporary user class"""
    uid = 0


def ProcessArgs(function, argsDicit):
    try:
        return [argsDicit[i] for i in function.__code__.co_varnames[:function.__code__.co_argcount]]
    except KeyError:
        raise CannotFullFillFunction()


# COMMAND MANAGER
def user_input_cmd(fs, user):
    while True:
        user_input = input(">>>  ").split()
        try:
            if user_input[0] in user_commands:
                 try:
                    clear_term()
                    if randint(1, 20) == 1:
                        random_test()
                    function = user_commands[user_input[0]]
                    function(*ProcessArgs(function, locals()))
                 except Exception as e:
                     print(e)
        except:
            print('must include command listed in "help"')


def start(fs, user):
    firstgamefile = open('first_game.txt', 'r')
    content = firstgamefile.readline()
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
    return


def main():
    global fs
    start(fs, User)
    user_input_cmd(fs, User)


if __name__ == "__main__":
    main()
