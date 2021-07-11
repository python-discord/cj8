from os import walk, path, sep


import functions.blessed_functions
import functions.file_functions
# local modules
import binary_file_library

# file system imports
from fs.fs_dir import Dir
fs = Dir.FromPath("OS", None, 7, 0, 0)
this_dir = fs




class User:
    """temporary user class"""
    uid = 0


cl = ["│", "─", "┌", "┬", "┐", "├", "┼", "┤", "└", "┴", "┘"]
START_PATH = "OS/game_files/"
BLANK_LINES = 50  # number of characters each line should be
print(term.home + term.clear + term.move_y(term.height // 2))









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
            start_add(user_input)
            showing_input_menu = False
        if user_input[:3] == "dir":
            start_dir(user_input)
            showing_input_menu = False
        if user_input[:10] == "quickcrypt":
            start_quickcrypt(user_input)
            showing_input_menu = False
        if user_input[:4] == "read":
            start_read(user_input)
            showing_input_menu = False
        if user_input == "ls":
            for i in this_dir.ls(User).keys():
                print(i)
        if user_input[:2] == "cd":
            try:
                this_dir = this_dir.getDir(User(), user_input[3:])
            except Exception as e:
                print(e)
        if user_input[:5] == "mkdir":
            try:
                this_dir.mkdir(User, user_input[6:])
            except Exception as e:
                print(e)
        if user_input[:5] == "touch":
            try:
                this_dir.touch(User, user_input[6:])
            except Exception as e:
                print(e)
        if user_input[:2] == "rm":
            try:
                this_dir.rm(User, user_input[3:])
            except Exception as e:
                print(e)
        if user_input[:6] == "search":
            start_search(user_input)
            showing_input_menu = False



def start_dir(user_input):
    user_input += " 1 1 1 "
    user_input = user_input.split()
    print(term.home + term.clear + term.move_y(term.height // 2))
    if user_input[1] == "1":
        printtree("System", START_PATH)
    else:
        printtree("System", f"OS/game_files/{user_input[1]}")
    user_input_cmd()



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


def start_read(user_input):
    user_input = user_input.split()


def start_quickcrypt(user_input):
    # "quickcrypt [file path] [password]"
    user_input += " 1 2 3 "  # place holder inputs which stops the user from entering errors
    user_input = user_input.split()
    binary_file_library.decrypt_file(user_input[1], user_input[2])


def start_search(user_input):
    # only searches for the first word after "search"
    user_input = user_input.split()
    search_word = user_input[1]
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


if __name__ == "__main__":
    start()
