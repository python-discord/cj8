from os import walk, path, sep
import os
from blessed import Terminal
term = Terminal()

cl = ["│", "─", "┌", "┬", "┐", "├", "┼", "┤", "└", "┴", "┘"]
BLANK_LINES = 50
print(term.home +  term.clear + term.move_y(term.height // 2))

def list_files(startpath):
    print(term.green_on_black('┌─ /System/ ─────────────────────────────────────┐'))
    for root, dirs, files in walk(startpath):
        level = root.replace(startpath, '').count(sep)
        indent = '─' * 4 * (level)
        current_line_length = len('├'+'{}{}/'.format(indent, path.basename(root)))
        extra_blank_needed = (BLANK_LINES - current_line_length -1) * " "
        print(term.green_on_black('├'+'{}{}/{}│'.format(indent, path.basename(root),extra_blank_needed)))
        subindent ='├' +'─' * 4 * (level + 1)
        for f in files:
            current_line_length = len('{}{}'.format(subindent, f))
            extra_blank_needed = (BLANK_LINES - current_line_length -1) * " "
            print(term.green_on_black('{}{}{}│'.format(subindent, f,extra_blank_needed)))
    print(term.green_on_black('└─ /System/ ─────────────────────────────────────┘'))    
    printLogo()

def start():
    list_files("OS")
    print(term.green_on_black("┌─ /CMD/ ────────"))

def printLogo():
    print(term.green_on_black(""))
    schedule()

def schedule():
    schedule = True
    while schedule == True:
        userInput = input(">>>  ").lower()
        if userInput[:4] == "help" or userInput[:1] == "h":
            startHelp(userInput)
            schedule = False
        if userInput[:3] == "add":
            startAdd(userInput)
            schedule = False
        if userInput[:3] == "dir":
            startDir(userInput)
            schedule = False

def startHelp(input):
    input += " 1 2 3 " #place holder inputs which stops the user from entering errors
    input = input.split()
    if input[1] == "add":
        print(term.green_on_black("┌─ /Help/ ───────────────────────────────────────┐"))
        print(term.green_on_black("│add [name] [dd/mm/yyyy] [time (13:12)]  (desc)  │"))
        print(term.green_on_black("│- creates a new file with a specified name in   │"))
        print(term.green_on_black("│  specified directory                           │"))
        print(term.green_on_black("└────────────────────────────────────────────────┘"))
    elif input[1] == "remove":
        print(term.green_on_black("┌─ /Help/ ───────────────────────────────────────┐"))
        print(term.green_on_black("│remove [name]                                   │"))
        print(term.green_on_black("│- deletes a  file with a specified name in      │"))
        print(term.green_on_black("│  specified directory                           │"))
        print(term.green_on_black("└────────────────────────────────────────────────┘"))
    elif input[1] == "dir":
        print(term.green_on_black("┌─ /Help/ ───────────────────────────────────────┐"))
        print(term.green_on_black("│dir                                             │"))
        print(term.green_on_black("│- shows full  user directory                    │"))
        print(term.green_on_black("└────────────────────────────────────────────────┘"))
    elif input[1] == "help":
        print(term.green_on_black("┌─ /Help/ ───────────────────────────────────────┐"))
        print(term.green_on_black("│help (command)                                  │"))
        print(term.green_on_black("│- explains what the specified command does      │"))
        print(term.green_on_black("└────────────────────────────────────────────────┘"))
    else:
        print(term.green_on_black("┌─ /Help/ ───────────────────────────────────────┐"))
        print(term.green_on_black("│help (command)                                  │"))
        print(term.green_on_black("│add [name] [dd/mm/yyyy] [time (13:12)]  (desc)  │"))
        print(term.green_on_black("│remove [name]                                   │"))
        print(term.green_on_black("│dir                                             │"))
        print(term.green_on_black("└────────────────────────────────────────────────┘"))
    printLogo()

def startAdd(input):
    input = input.split()
    print(term.green_on_black("┌─ /Add/ ────────────────────────────────────────┐"))
    print(term.green_on_black("└────────────────────────────────────────────────┘"))
   
    input = input.split()
    
    printLogo()

def startDir(input):
    list_files("OS")
    input = input.split()

if __name__ == "__main__":
    start()