from functions.command_functions import start_help, start_dir, start_quickcrypt,\
    start_read, start_search, start_walk, start_portscanner
from os import walk, sep, path
import time
from blessed import Terminal

from fs.fs_dir import Dir

# file system imports
fs = Dir.FromPath("OS", None, 7, 0, 0)

START_PATH = "OS/game_files/"
BLANK_LINES = 50  # number of characters each line should be

term = Terminal()
print(term.home + term.clear + term.move_y(term.height // 2))

cl = ["│", "─", "┌", "┬", "┐", "├", "┼", "┤", "└", "┴", "┘"]

user_commands = {"walk": start_walk,
                 "dir": start_dir,
                 "h": start_help,
                 "help": start_help,
                 "quickcrypt": start_quickcrypt,
                 "read": start_read,
                 "search": start_search,
                 "portscan": start_portscanner,
                 "walk": start_walk
                 }


class User:
    """temporary user class"""
    uid = 0


def print_tree(header, location):
    print(term.green_on_black(f'┌─ /{header}/' + ('─' * (BLANK_LINES - 6 - len(header))) + '┐'))
    for root, dirs, files in walk(location):
        level = root.replace(START_PATH, '').count(sep)
        indent = '─' * 4 * level
        # finds the length of the directory that is going to be printed
        # takes away the length from the constant variable to find
        # the amount of extra blank spaces needed
        current_line_length = len('├'+'{}{}/'.format(indent, path.basename(root)))
        extra_blank_needed = (BLANK_LINES - current_line_length - 1) * " "  # -1 used to make space for edge of box
        print(term.green_on_black(f'├{indent}{path.basename(root)}/{extra_blank_needed}│'))
        sub_indent = '├' + '─' * 4 * (level + 1)
        for f in files:
            # does the same as above but with the files
            current_line_length = len('{}{}'.format(sub_indent, f))
            extra_blank_needed = (BLANK_LINES - current_line_length - 1) * " "  # -1 used to make space for edge of box
            print(term.green_on_black(f'{sub_indent}{f}{extra_blank_needed}│'))
    print(term.green_on_black(f'└─ /{header}/' + ('─' * (BLANK_LINES - 6 - len(header))) + '┘'))


def print_box(header, textl):
    def print_box_str(ret_string, words):
        # if fits in one line
        if len(words) <= BLANK_LINES - 3:
            ret_string += str(cl[0] + " " + words + " " * int(BLANK_LINES - 3 - len(words)) + cl[0] + "\n")
        # if longer than one line
        else:
            rows = len(words) // (BLANK_LINES - 3) + (len(words) % (BLANK_LINES - 3) != 0)
            startpos = [(BLANK_LINES - 3) * row for row in range(rows + 1)]
            for row in range(rows):
                # for last row of long line
                if row == rows - 1:
                    ret_string += str(cl[0] + " " + words[startpos[-2]:] +
                    " " * int(BLANK_LINES - 3 - len(words[startpos[-2]:])) + cl[0] + "\n")
                # for other rows of long line
                else:
                    ret_string += str(cl[0] + " " + words[startpos[row]:startpos[row + 1]] + cl[0] + "\n")
        return ret_string

    ret_string = str(cl[2] + cl[1] + f" /{header}/ " + cl[1] * int(BLANK_LINES - 7 - len(header)) + cl[4] + "\n")
    for words in textl:
        if type(words) == list:
            for word in words:
                ret_string = print_box_str(ret_string, word)
        elif type(words) == str:
            ret_string = print_box_str(ret_string, words)
        else:
            print("error in printhelp: second input should be a list containing strings and/or lists of strings")
    ret_string += str(cl[8] + cl[1] * (BLANK_LINES - 2) + cl[10])
    return ret_string


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


# COMMAND MANAGER
def user_input_cmd():

    clear_term()
    showing_input_menu = True
    while showing_input_menu:
        user_input = input(">>>  ").lower()
        if user_input in user_commands.keys():
            # try:
                user_commands[user_input](user_input, fs, User)
                showing_input_menu = False
            # except Exception as e:
            #     print(e)


def start():
    printstart(
        """Hey There! \n  You are an Artificial Intelligant, built by the USA, developed to get into PCs and analyze them. \n You was hacked into a System by the Atomic Program of the Iran. Here, ur job was to analyze the Data and to see if there are any files which could gives hint to the Atomatic Missiles of the Iran. \n \n""")
    printstart(
        """You found out that there will be a nuclear launch today, it should hit the US. But unfortunally, the system is offline, you cant contact the USA to warn them. \n \n""")
    printstart(
        """Because of that, u decide that ull try to turn of the System, because you found indicates that that will stop the attack. But unfortunally, you need Root Privilages to shutdown the Operating System \n \n""")
    printstart(
        """You can gain access to these by (*insert challange here, example: get the password of the main file*). You will have to overcome multiple challenges \n \n""")
    printstart("""So, dont waste your time, think smarter not harder, and good luck!
                (*Title* starting, 
                gaining system access,
                Access gained.
                AI will launch...) \n \n""")
    print_tree("System", START_PATH)
    return


def main():
    start()
    while True:
        user_input_cmd()




if __name__ == "__main__":
    main()
