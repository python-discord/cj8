from os import walk, path, sep
import os
import binary_file_library
from blessed import Terminal
term = Terminal()

cl = ["│", "─", "┌", "┬", "┐", "├", "┼", "┤", "└", "┴", "┘"]
BLANK_LINES = 50 #amount of lines each box should be
print(term.home +  term.clear + term.move_y(term.height // 2))

def list_files(startpath):
    print(term.green_on_black('┌─ /System/ ─────────────────────────────────────┐'))
    for root, dirs, files in walk(startpath):
        level = root.replace(startpath, '').count(sep)
        indent = '─' * 4 * (level)
        # finds the length of the directory that is going to be printed
        # takes away the length from the constant valriable to find 
        # the amount of extra blank spaces needed
        current_line_length = len('├'+'{}{}/'.format(indent, path.basename(root)))
        extra_blank_needed = (BLANK_LINES - current_line_length -1) * " "
        print(term.green_on_black('├'+'{}{}/{}│'.format(indent, path.basename(root),extra_blank_needed)))
        subindent ='├' +'─' * 4 * (level + 1)
        for f in files:
             # does the same as above but with the files
            current_line_length = len('{}{}'.format(subindent, f))
            extra_blank_needed = (BLANK_LINES - current_line_length -1) * " "
            print(term.green_on_black('{}{}{}│'.format(subindent, f,extra_blank_needed)))
    print(term.green_on_black('└─ /System/ ─────────────────────────────────────┘'))    
    user_input_cmd()

def printhelp(header, textl):
    retstring = ""
    retstring += str(cl[2] + cl[1] + f" /{header}/ " + cl[1]*int(46-len(header)) + cl[4]) + "\n"
    for words in textl:
        retstring += str(cl[0] + " " + words + " "*int(50 - len(words)) + cl[0] + "\n")
    retstring += str(cl[8] + cl[1]*51 + cl[10])
    return(retstring)
    
def start():
    list_files("OS")
    print(term.green_on_black("┌─ /CMD/ ────────"))



def user_input_cmd():
    print(term.green_on_black(""))
    showing_input_menu = True
    while showing_input_menu == True:
        userInput = input(">>>  ").lower()
        #commands list V
        if userInput[:4] == "help" or userInput[:1] == "h":
            startHelp(userInput)
            showing_input_menu = False
        if userInput[:3] == "add":
            startAdd(userInput)
            showing_input_menu = False
        if userInput[:3] == "dir":
            startDir(userInput)
            showing_input_menu = False

def startHelp(input):
    print(term.home +  term.clear + term.move_y(term.height // 2))
    input += " 1 2 3 " #place holder inputs which stops the user from entering errors
    input = input.split()
    if input[1] == "add":
        print(term.green_on_black(printhelp("Help", ["add [name] [dd/mm/yyyy] [time (13:12)]  (desc)", "- creates a new file with a specified name in","specified directory"])))
    elif input[1] == "remove":
        print(term.green_on_black(printhelp("Help", ["remove [name]", "- deletes a  file with a specified name in", "specified directory"])))
    elif input[1] == "dir":
        print(term.green_on_black(printhelp("Help", ["dir", "- shows full  user directory"])))
    elif input[1] == "help":
        print(term.green_on_black(printhelp("Help", ["help (command)", "- explains what the specified command does"])))
    else:
        print(term.green_on_black(printhelp("Help", ["help (command)", "add [name] [dd/mm/yyyy] [time (13:12)]  (desc)", "remove [name]", "dir"])))
    user_input_cmd()

def startAdd(input):
    print(term.home +  term.clear + term.move_y(term.height // 2))
    input = input.split()
    print(term.green_on_black("┌─ /Add/ ────────────────────────────────────────┐"))
    print(term.green_on_black("└────────────────────────────────────────────────┘"))
    open(input[1], "a").close()
    startDir("dire")
    user_input_cmd()

def startDir(input):
    print(term.home +  term.clear + term.move_y(term.height // 2))
    list_files("OS")
    
#Just like in the binaryfilelibrary, encrypt and decrypt does the same thing.
def encrypt_file(path, password):
    binaryfilelibrary.modifyFile(path, password)

def decrypt_file(path, password):
    binaryfilelibrary.modifyFile(path, password)


if __name__ == "__main__":
    start()