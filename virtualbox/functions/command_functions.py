#START_PATH = "OS/game_files/"
# BLANK_LINES = 50  # number of characters each line should be
# cl = ["│", "─", "┌", "┬", "┐", "├", "┼", "┤", "└", "┴", "┘"]

def start_dir(user_input):
    from virtualbox.project import clear_term,print_tree, user_input_cmd
    START_PATH = "OS/game_files/"
    user_input += " 1 1 1 "
    user_input = user_input.split()
    clear_term()
    if user_input[1] == "1":
        print_tree("System", START_PATH)
    else:
        print_tree("System", f"OS/game_files/{user_input[1]}")
    user_input_cmd()


def start_help(user_input):
    from virtualbox.project import clear_term, print_tree, print_box, user_input_cmd
    clear_term()
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
            print_box(heade, lis)
    else:
        print_box("Help", ["help (command)",
                         "add [name]",
                         "remove [name]",
                         "dir",
                         "read [file path]",
                         "quickcrypt [file path] [password]",
                         "search [name]"
                         ])
    user_input_cmd()


def start_quickcrypt(user_input):
    from virtualbox.project import clear_term, print_tree, print_box, user_input_cmd
    # "quickcrypt [file path] [password]"
    user_input += " 1 2 3 "  # place holder inputs which stops the user from entering errors
    user_input = user_input.split()
    binary_file_library.decrypt_file(user_input[1], user_input[2])

    user_input_cmd()


def start_read(user_input):
    from virtualbox.project import clear_term, print_tree, print_box, user_input_cmd
    user_input = user_input.split()
    user_input_cmd()

def start_search(user_input):
    from virtualbox.project import clear_term, print_tree, print_box, user_input_cmd
    from os import walk
    START_PATH = "OS/game_files/"
    BLANK_LINES = 50  # number of characters each line should be
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




