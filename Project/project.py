from functions.blessed_functions import print_box, print_tree, printstart
from functions import command_functions
from fs.fs_dir import Dir

# file system imports
fs = Dir.FromPath("OS", None, 7, 0, 0)
this_dir = fs


class User:
    """temporary user class"""
    uid = 0


def main():
    printstart()



if __name__ == "__main__":
    main()
