from functions.blessed_functions import print_box, print_tree, printstart, start
from functions.command_functions import start_help, user_input_cmd

from fs.fs_dir import Dir

# file system imports
fs = Dir.FromPath("OS", None, 7, 0, 0)
this_dir = fs


class User:
    """temporary user class"""
    uid = 0


def main():
    start()
    user_input_cmd()



if __name__ == "__main__":
    main()
