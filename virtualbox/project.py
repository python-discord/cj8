
from functions.command_functions import user_commands, random_test
from functions.blessed_functions import print_tree, clear_term, printstart, printhelp_first, print_box
from exceptions import CannotFullFillFunction
from config import START_PATH
from random import randint
from time import sleep


from fs.fs_dir import Dir

# file system imports
fs = Dir.FromPath(START_PATH, None, 7, 0, 0)

failed_tasks = 0


class User:
    """temporary user class"""
    uid = 0


def add_failure():
    global failed_tasks
    failed_tasks += 1
    print(f"DEBUG: failues: {failed_tasks}")



def ProcessArgs(function, argsDicit):
    try:
        return [argsDicit[i] for i in function.__code__.co_varnames[:function.__code__.co_argcount]]
    except KeyError:
        raise CannotFullFillFunction()


# COMMAND MANAGER
def user_input_cmd(fs, user):
    while True:
        user_input = input(">>>  ").split()
        if user_input[0] in user_commands:
            try:
                clear_term()
                if randint(1, 20) == 1:
                    random_test()
                function = user_commands[user_input[0]]
                function(*ProcessArgs(function, locals()))
            except Exception as e:
                print(e)


def start(fs, user):
    clear_term()
    print_box('Intro',
       [' Hey There! You are an Artificial Intelligant,',' built by the USA, developed to get into PCs and analyze them.',' You was hacked into a System by the Atomic Program of the Iran.',' Here, your job was to analyze the Data and to see,',' if there are any files which could gives hints to the Atomatic Missiles of the Iran.'])
    input()
    clear_term()
    print_box('Intro',
       [' You found out that there will be a nuclear',' launch today, it should hit the US. But unfortunally, the system',' is offline, you cant contact the USA to warn them.'])
    input()
    clear_term()
    print_box('Intro',
       [' Because of that, you have decided that youll try to',' turn of the System, because you found indicates that that will stop',' the attack. But unfortunally, you need Root Privilages to',' shutdown the Operating System '])
    input()
    clear_term()
    print_box('Intro',
       ['You can gain access to these by (*insert challange here,',' example: get the password of the main file*). ','You will have to overcome multiple challenges'])
    input()
    clear_term()
    print_box('Intro',
        ['So, dont waste your time, think smarter not harder, and good luck!',
               '*Title* starting',
               'gaining system access',
               'Access gained.',
               'AI will launch...)'])
    clear_term()
    printhelp_first('This is the file tree, here, you can see every file in the operating system!')
    print_tree("System", fs, user)
    printhelp_first('First, type "help" in the console to see all of the commands you can use!')
    return


def main():
    global fs
    start(fs, User)
    user_input_cmd(fs, User)


if __name__ == "__main__":
    main()
