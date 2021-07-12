from functions.command_functions import user_commands
from functions.blessed_functions import print_tree
from exceptions import CannotFullFillFunction
from config import START_PATH

import time
from blessed import Terminal

from fs.fs_dir import Dir

# file system imports
fs = Dir.FromPath(START_PATH, None, 7, 0, 0)

term = Terminal()
print(term.home + term.clear + term.move_y(term.height // 2))


class User:
    """temporary user class"""
    uid = 0


def printstart(arg):
    print(term.clear)
    print(term.green_on_black(arg))
    time.sleep(1)
    print(term.green_on_black("Press C to continue"))
    with term.cbreak():
        val = ''
        if val.lower() == 'c':
            return
        else:
            pass


def clear_term():
    print(term.clear)


def ProcessArgs(function, argsDicit):
    try:
        return [argsDicit[i] for i in function.__code__.co_varnames[:function.__code__.co_argcount]]
    except KeyError:
        raise CannotFullFillFunction()


# COMMAND MANAGER
def user_input_cmd(fs, user):
    global term
    # clear_term()
    while True:
        user_input = input(">>>  ").split()
        if user_input[0] in user_commands:
            try:
                function = user_commands[user_input[0]]
                function(*ProcessArgs(function, locals()))
            except Exception as e:
                print(e)


def start(fs, user):
    #printstart(
    #    """Hey There! \n  You are an Artificial Intelligant, built by the USA, developed to get into PCs and analyze them. \n You was hacked into a System by the Atomic Program of the Iran. Here, ur job was to analyze the Data and to see if there are any files which could gives hint to the Atomatic Missiles of the Iran. \n \n""")
    #printstart(
     #   """You found out that there will be a nuclear launch today, it should hit the US. But unfortunally, the system is offline, you cant contact the USA to warn them. \n \n""")
    #printstart(
     #   """Because of that, u decide that ull try to turn of the System, because you found indicates that that will stop the attack. But unfortunally, you need Root Privilages to shutdown the Operating System \n \n""")
    #printstart(
    #    """You can gain access to these by (*insert challange here, example: get the password of the main file*). You will have to overcome multiple challenges \n \n""")
    #printstart("""So, dont waste your time, think smarter not harder, and good luck!
    #            (*Title* starting, 
    #            gaining system access,
    #            Access gained.
    #            AI will launch...) \n \n""")
    print_tree("System", fs, user)
    return


def main():
    global fs
    start(fs, User)
    user_input_cmd(fs, User)


if __name__ == "__main__":
    main()
