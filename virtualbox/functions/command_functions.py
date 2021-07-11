from .blessed_functions import print_box, print_tree
from blessed import Terminal
from os import walk
import random
import time
import os
term = Terminal()
START_PATH = "OS/game_files/"
BLANK_LINES = 50

# COMMAND LIST
def start_add(user_input):
    # print(term.home + term.clear + term.move_y(term.height // 2))
    # user_input = input.split()
    # path_l = input[1].split("/")
    # if not os.path.isdir(path_l[0]):
    #     os.makedirs(path_l[0])
    #     open(os.path.join(path_l[0], path_l[1])).close()
    # else:
    #     if "." in path_l[0]:
    #         open(path_l[0]).close()
    #     else:
    #         open(os.path.join(path_l[0], path_l[1])).close()
    #
    # start_dir("dir")
    user_input_cmd()


def start_dir(user_input):
    user_input += " 1 1 1 "
    user_input = user_input.split()
    print(term.home + term.clear + term.move_y(term.height // 2))
    if user_input[1] == "1":
        print_tree("System", START_PATH)
    else:
        print_tree("System", f"OS/game_files/{user_input[1]}")
    user_input_cmd()


def start_help(user_input):
    print(term.home + term.clear + term.move_y(term.height // 2))
    user_input += " 1 2 3 "  # place holder inputs which stops the user from entering errors
    user_input = user_input.split()
    user_input_dir = {
        "add": ["Help", ["add [file path]", "- creates a new file with a specified name in specified directory"]],
        "remove" : ["Help", ["remove [file path]", "- removes a new file with a specified name in specified directory"]],
        "dir": ["Help", ["dir", "- shows full user directory"]],
        "help" : ["Help", ["help (command)", "- explains what the specific command does"]],
        "quickcrypt": ["Help", ["quickcrypt (file path) (password)", "- file encryption tool"]],
        "read":["Help", ["read (file path)", "- reads a files content"]],
        "search": ["Help", ["search (file path)", "- searches directory for a specific file"]],
        "portscan":["Help", ["portscan", "- searches for open ports in the operating system network"]]
    }
    if user_input[1] in user_input_dir.keys():
        print(term.green_on_black(print_box(user_input[1], user_input_dir[user_input[1]])))
    else:
        print(term.green_on_black(print_box("Help", ["help (command)",
                                                     "add [name]",
                                                     "remove [name]",
                                                     "dir",
                                                     "read [file path]",
                                                     "quickcrypt [file path] [password]",
                                                     "search [name]",
                                                     "portscan"
                                                     ])))
    user_input_cmd()


def start_quickcrypt(user_input):
    # "quickcrypt [file path] [password]"
    user_input += " 1 2 3 "  # place holder inputs which stops the user from entering errors
    user_input = user_input.split()
    binary_file_library.decrypt_file(user_input[1], user_input[2])


def start_read(user_input):
    user_input = user_input.split()


def start_search(user_input):
    user_input = user_input.split()
    search_word = " ".join(user_input[1:])
    search_here = walk(START_PATH)
    search_result = []
    for root, dirs, file_lists in search_here:
        if search_word in root.lower():
            search_result.append(root)
        for files in file_lists:
            if search_word in files.lower():
                search_result.append(root + "\\" + files)
    search_result = [each_search_result[14:] for each_search_result in search_result]
    if len(search_word) > BLANK_LINES - 16:
        search_word = search_word[0:(BLANK_LINES - 19)] + "..."

    print(print_box(f"Search: {search_word}", search_result))
    user_input_cmd()

def start_portscanner(user_input):
    ports = [22, 80, 9929, 8898, 22542, 187, 32312]
    outputs = ['not a hint', 'not a hint', 'not a hint', 'not a hint',\
               'not a hint', 'a hint', 'a hint', 'a hint', 'a hint']
    for i in range(7):
        port = ports[i]
        print(
            str(f"Found Port in Network: \n    {port}/TCP [State: open] \n    Scanning Port... \n"))  # term.green_on_black
        time.sleep(0.4)
    inp = input('Select a port to scan: ')
    inp = int(inp)
    if inp in ports:
        output = random.choice(outputs)
        time.sleep(3)
        os.system('cls')
        print(f'Port {inp} attackable. \n    Attack launchend. \n    Output: {output} \n')

    else:
        print('nothing')


# print(term.home + term.clear + term.move_y(term.height // 2))
# for i in range(7):
#     time.sleep(0.4)
#     port = ports[i]
#     randomi = random.randint(0, 1)
#     output = random.choice(outputs)
#     if randomi == 1:
#         print(f'Port {port} attackable. \n    Attack launchend. \n    Output: {output} \n')

# COMMAND DICTIONARY
user_commands = {"add": start_add,
                 "dir": start_dir,
                 "h": start_help,
                 "help": start_help,
                 "quickcrypt": start_quickcrypt,
                 "read": start_read,
                 "search": start_search,
                 "portscan": start_portscanner
                 }


# COMMAND MANAGER
def user_input_cmd():
    # print(term.green_on_black(""))
    showing_input_menu = True
    while showing_input_menu:
        user_input = input(">>>  ").lower()

        if user_input.split()[0] in user_commands.keys():
            user_commands[user_input.split()[0]](user_input)
            showing_input_menu = False


