from os import walk, path, sep
import os
from blessed import Terminal
term = Terminal()

cl = ["│", "─", "┌", "┬", "┐", "├", "┼", "┤", "└", "┴", "┘"]
BLANK_LINES = 50
print(term.home +  term.clear + term.move_y(term.height // 2))

def list_files(startpath):
    print(term.black_on_darkkhaki('┌─ /System/ ─────────────────────────────────────┐'))
    for root, dirs, files in walk(startpath):
        level = root.replace(startpath, '').count(sep)
        indent = '─' * 4 * (level)
        current_line_length = len('├'+'{}{}/'.format(indent, path.basename(root)))
        extra_blank_needed = (BLANK_LINES - current_line_length -1) * " "
        print(term.black_on_darkkhaki('├'+'{}{}/{}│'.format(indent, path.basename(root),extra_blank_needed)))
        subindent ='├' +'─' * 4 * (level + 1)
        for f in files:
            current_line_length = len('{}{}'.format(subindent, f))
            extra_blank_needed = (BLANK_LINES - current_line_length -1) * " "
            print(term.black_on_darkkhaki('{}{}{}│'.format(subindent, f,extra_blank_needed)))
    print(term.black_on_darkkhaki('└─ /System/ ─────────────────────────────────────┘'))    
    printLogo()

def start():
    list_files("OS")
    print(term.black_on_darkkhaki("┌─ /CMD/ ────────"))

def printLogo():
    print(term.black_on_darkkhaki(""))
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
        print(term.black_on_darkkhaki("┌─ /Help/ ───────────────────────────────────────┐"))
        print(term.black_on_darkkhaki("│add [name] [dd/mm/yyyy] [time (13:12)]  (desc)  │"))
        print(term.black_on_darkkhaki("│- creates a new file with a specified name in   │"))
        print(term.black_on_darkkhaki("│  specified directory                           │"))
        print(term.black_on_darkkhaki("└────────────────────────────────────────────────┘"))
    elif input[1] == "remove":
        print(term.black_on_darkkhaki("┌─ /Help/ ───────────────────────────────────────┐"))
        print(term.black_on_darkkhaki("│remove [name]                                   │"))
        print(term.black_on_darkkhaki("│- deletes a  file with a specified name in      │"))
        print(term.black_on_darkkhaki("│  specified directory                           │"))
        print(term.black_on_darkkhaki("└────────────────────────────────────────────────┘"))
    elif input[1] == "dir":
        print(term.black_on_darkkhaki("┌─ /Help/ ───────────────────────────────────────┐"))
        print(term.black_on_darkkhaki("│dir                                             │"))
        print(term.black_on_darkkhaki("│- shows full  user directory                    │"))
        print(term.black_on_darkkhaki("└────────────────────────────────────────────────┘"))
    elif input[1] == "help":
        print(term.black_on_darkkhaki("┌─ /Help/ ───────────────────────────────────────┐"))
        print(term.black_on_darkkhaki("│help (command)                                  │"))
        print(term.black_on_darkkhaki("│- explains what the specified command does      │"))
        print(term.black_on_darkkhaki("└────────────────────────────────────────────────┘"))
    else:
        print(term.black_on_darkkhaki("┌─ /Help/ ───────────────────────────────────────┐"))
        print(term.black_on_darkkhaki("│help (command)                                  │"))
        print(term.black_on_darkkhaki("│add [name] [dd/mm/yyyy] [time (13:12)]  (desc)  │"))
        print(term.black_on_darkkhaki("│remove [name]                                   │"))
        print(term.black_on_darkkhaki("│dir                                             │"))
        print(term.black_on_darkkhaki("└────────────────────────────────────────────────┘"))
    printLogo()

def startAdd(input):
    input = input.split()
    print(term.black_on_darkkhaki("┌─ /Add/ ────────────────────────────────────────┐"))
    print(term.black_on_darkkhaki("└────────────────────────────────────────────────┘"))
   
    input = input.split()
    
    printLogo()

def startDir(input):
    list_files("OS")
    input = input.split()

if __name__ == "__main__":
    start()