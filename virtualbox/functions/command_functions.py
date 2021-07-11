from .blessed_functions import print_box, print_tree


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
        printtree("System", START_PATH)
    else:
        printtree("System", f"OS/game_files/{user_input[1]}")
    user_input_cmd()


def start_help(user_input):
    print(term.home + term.clear + term.move_y(term.height // 2))
    user_input += " 1 2 3 "  # place holder inputs which stops the user from entering errors
    user_input = "help add"
    user_input = user_input.split()
    user_input_dir = {
        "add": ["Help", ["add [file path]", "- creates a new file with a specified name in specified directory"]],
        "remove" : ["Help", ["remove [file path]", "- removes a new file with a specified name in specified directory"]],
        "dir": ["Help", ["dir", "- shows full user directory"]],
        "help" : ["Help", ["help (command)", "- explains what the specific command does"]],
        "quickcrypt": ["Help", ["quickcrypt (file path) (password)", "- file encryption tool"]],
        "read":["Help", ["read (file path)", "- reads a files content"]],
        "search": ["Help", ["search (file path)", "- searches directory for a specific file"]]
    }
    if user_input[1] in user_input_dir:
        for heade, lis in user_input_dir[user_input[1]]:
            print(term.green_on_black(print_box(heade, lis)))
    else:
        print(term.green_on_black(print_box("Help", ["help (command)",
                                                     "add [name]",
                                                     "remove [name]",
                                                     "dir",
                                                     "read [file path]",
                                                     "quickcrypt [file path] [password]",
                                                     "search [name]"
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


# COMMAND DICTIONARY
user_commands = {"add": start_add,
                 "dir": start_dir,
                 "h": start_help,
                 "help": start_help,
                 "quickcrypt": start_quickcrypt,
                 "read": start_read,
                 "search": start_search
                 }


# COMMAND MANAGER
def user_input_cmd():
    print(term.green_on_black(""))
    showing_input_menu = True
    while showing_input_menu:
        user_input = input(">>>  ").lower()
        if user_input in user_commands.keys():
            user_commands[user_input](user_input)
            showing_input_menu = False

        # if user_input[:4] == "help" or user_input[:1] == "h":
        #     start_help(user_input)
        #     showing_input_menu = False
        # if user_input[:3] == "add":
        #     start_add(user_input)
        #     showing_input_menu = False
        # if user_input[:3] == "dir":
        #     start_dir(user_input)
        #     showing_input_menu = False
        # if user_input[:10] == "quickcrypt":
        #     start_quickcrypt(user_input)
        #     showing_input_menu = False
        # if user_input[:4] == "read":
        #     start_read(user_input)
        #     showing_input_menu = False
        # if user_input[:6] == "search":
        #     start_search(user_input)
        #     showing_input_menu = False

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
