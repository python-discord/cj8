from os import walk, path, sep
import os
import binary_file_library

from blessed import Terminal
term = Terminal()

cl = ["│", "─", "┌", "┬", "┐", "├", "┼", "┤", "└", "┴", "┘"]
BLANK_LINES = 50  # number of characters each line should be
print(term.home + term.clear + term.move_y(term.height // 2))


def list_files(startpath):
    print(term.green_on_black('┌─ /System/ ─────────────────────────────────────┐'))
    for root, dirs, files in walk(startpath):
        level = root.replace(startpath, '').count(sep)
        indent = '─' * 4 * level
        # finds the length of the directory that is going to be printed
        # takes away the length from the constant variable to find
        # the amount of extra blank spaces needed
        current_line_length = len('├'+'{}{}/'.format(indent, path.basename(root)))
        extra_blank_needed = (BLANK_LINES - current_line_length - 1) * " "  # -1 used to make space for edge of box
        print(term.green_on_black('├'+'{}{}/{}│'.format(indent, path.basename(root), extra_blank_needed)))
        sub_indent = ' ├ ' + ' ─ ' * 4 * (level + 1)
        for f in files:
            # does the same as above but with the files
            current_line_length = len('{}{}'.format(sub_indent, f))
            extra_blank_needed = (BLANK_LINES - current_line_length - 1) * " "  # -1 used to make space for edge of box
            print(term.green_on_black('{}{}{}│'.format(sub_indent, f, extra_blank_needed)))
    print(term.green_on_black('└─ /System/ ─────────────────────────────────────┘'))    
    user_input_cmd()


def print_box(header, textl):
    def print_box_str(ret_string, words):
        # if fits in one line
        if len(words) <= BLANK_LINES - 2:
            ret_string += str(cl[0] + " " + words + " " * int(BLANK_LINES - 3 - len(words)) + cl[0] + "\n")
        # if longer than one line
        else:
            rows = len(words) // (BLANK_LINES - 2) + (len(words) % (BLANK_LINES - 2) != 0)
            startpos = [(BLANK_LINES - 4) * row for row in range(rows + 1)]
            for row in range(rows):
                # for last row of long line
                if row == rows - 1:
                    ret_string += str(cl[0] + " " + words[startpos[-2]:-1] +
                                     " " * int(BLANK_LINES - 3 - len(words[startpos[-2]:-1])) + cl[0] + "\n")
                # for other rows of long line
                else:
                    ret_string += str(cl[0] + " " + words[startpos[row]:startpos[row + 1]] + " " + cl[0] + "\n")
        return ret_string

    ret_string = str(cl[2] + cl[1] + f" /{header}/ " + cl[1] * int(BLANK_LINES - 7 - len(header)) + cl[4] + "\n")
    for words in textl:
        if type(words) == list:
            for word in words:
                ret_string = print_box_str(ret_string, word)
        elif type(words) == str:
            ret_string = print_box_str(ret_string, words)
        else:
            print("error in printhelp: input should be str or list of str")
    ret_string += str(cl[8] + cl[1] * (BLANK_LINES - 2) + cl[10])
    return ret_string


def start():
    list_files("OS")
    print(term.green_on_black("┌─ /CMD/ ────────"))


def user_input_cmd():
    print(term.green_on_black(""))
    showing_input_menu = True
    while showing_input_menu:
        user_input = input(">>>  ").lower()
        # commands list V
        if user_input[:4] == "help" or user_input[:1] == "h":
            start_help(user_input)
            showing_input_menu = False
        if user_input[:3] == "add":
            startAdd(user_input)
            showing_input_menu = False
        if user_input[:3] == "dir":
            startDir(user_input)
            showing_input_menu = False


def start_help(user_input):
    print(term.home + term.clear + term.move_y(term.height // 2))
    user_input += " 1 2 3 " # place holder inputs which stops the user from entering errors
    user_input = user_input.split()
    if user_input[1] == "add":
        print(term.green_on_black(print_box("Help", ["add [name] [dd/mm/yyyy] [time (13:12)]  (desc)",
                                                     "- creates a new file with a specified name in specified directory"
                                                     ])))
    elif user_input[1] == "remove":
        print(term.green_on_black(print_box("Help", ["remove [name]",
                                                     "- deletes a  file with a specified name in specified directory"])))
    elif user_input[1] == "dir":
        print(term.green_on_black(print_box("Help", ["dir",
                                                     "- shows full  user directory"])))
    elif user_input[1] == "help":
        print(term.green_on_black(print_box("Help", ["help (command)",
                                                     "- explains what the specified command does"])))
    else:
        print(term.green_on_black(print_box("Help", ["help (command)",
                                                     "add [name] [dd/mm/yyyy] [time (13:12)]  (desc)",
                                                     "remove [name]",
                                                     "dir"])))
    user_input_cmd()


def startDir(user_input):
    print(term.home + term.clear + term.move_y(term.height // 2))
    list_files("OS")


def startAdd(user_input):
    print(term.home +  term.clear + term.move_y(term.height // 2))
    user_input = input.split()
    pathl = input[1].split("/")
    if not os.path.isdir(pathl[0]):
        os.makedirs(pathl[0])
        open(os.path.join(pathl[0], pathl[1])).close()
    else:
        if "." in pathl[0]:
            open(pathl[0]).close()
        else:
            open(os.path.join(pathl[0], pathl[1])).close()
    
    startDir("dir")
    user_input_cmd()


# Just like in the binary_file_library, encrypt and decrypt does the same thing.
def encrypt_file(user_input_path, password):
    binary_file_library.modifyFile(user_input_path, password)


def decrypt_file(user_input_path, password):
    binary_file_library.modifyFile(user_input_path, password)


if __name__ == "__main__":
    start()