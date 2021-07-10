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
    retstring = str(cl[2] + cl[1] + f" /{header}/ " + cl[1]*int(BLANK_LINES - 7 - len(header)) + cl[4] + "\n")
    for words in textl:
        # if fits in one line
        if len(words) <= BLANK_LINES - 2:
            retstring += str(cl[0] + " " + words + " "*int(BLANK_LINES - 3 - len(words)) + cl[0] + "\n")
        # if longer than one line
        else:
            rows = len(words) // (BLANK_LINES - 2) + (len(words) % (BLANK_LINES - 2) != 0)
            startpos = [(BLANK_LINES - 4) * row for row in range(rows + 1)]
            for row in range(rows):
                # for last row of long line
                if row == rows - 1:
                    retstring += str(cl[0] + " " + words[startpos[-2]:-1] +
                                     " "*int(BLANK_LINES - 3 - len(words[startpos[-2]:-1])) + cl[0] + "\n")
                # for other rows of long line
                else:
                    retstring += str(cl[0] + " " + words[startpos[row]:startpos[row+1]] + " " + cl[0] + "\n")
    retstring += str(cl[8] + cl[1]*(BLANK_LINES-2) + cl[10])
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
        print(term.green_on_black(printhelp("Help", ["add [name] [dd/mm/yyyy] [time (13:12)]  (desc)", "- creates a new file with a specified name in specified directory"])))
    elif input[1] == "remove":
        print(term.green_on_black(printhelp("Help", ["remove [name]", "- deletes a  file with a specified name in specified directory"])))
    elif input[1] == "dir":
        print(term.green_on_black(printhelp("Help", ["dir", "- shows full  user directory"])))
    elif input[1] == "help":
        print(term.green_on_black(printhelp("Help", ["help (command)", "- explains what the specified command does"])))
    else:
        print(term.green_on_black(printhelp("Help", ["help (command), add [name] [dd/mm/yyyy] [time (13:12)]  (desc), remove [name], dir"])))
    user_input_cmd()

def startDir(input):
    print(term.home +  term.clear + term.move_y(term.height // 2))
    list_files("OS")
    
def startAdd(input):
    print(term.home +  term.clear + term.move_y(term.height // 2))
    input = input.split()
    pathl = input[1].split("/")
    if os.path.isdir(pathl[0]) == False:
        os.makedirs(pathl[0])
        open(os.path.join(pathl[0], pathl[1])).close()
    else:
        if "." in pathl[0]:
            open(pathl[0]).close()
        else:
            open(os.path.join(pathl[0], pathl[1])).close()
    
    startDir("dir")
    user_input_cmd()

#Just like in the binaryfilelibrary, encrypt and decrypt does the same thing.
def encrypt_file(path, password):
    binary_file_library.modifyFile(path, password)

def decrypt_file(path, password):
    binary_file_library.modi
    fyFile(path, password)


if __name__ == "__main__":
    start()