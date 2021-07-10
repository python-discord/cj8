from os import walk, path, sep
from blessed import Terminal
term = Terminal()

cl = ["│", "─", "┌", "┬", "┐", "├", "┼", "┤", "└", "┴", "┘"]

print(term.home +  term.clear + term.move_y(term.height // 2))

def list_files(startpath):
    print(term.black_on_darkkhaki('┌─ /System/ ──'))
    for root, dirs, files in walk(startpath):
        level = root.replace(startpath, '').count(sep)
        indent = '─' * 4 * (level)
        print(term.black_on_darkkhaki('├'+'{}{}/'.format(indent, path.basename(root))))
        subindent ='├' +'─' * 4 * (level + 1)
        for f in files:
            print(term.black_on_darkkhaki('{}{}'.format(subindent, f)))
    printLogo()

def start():
    list_files("OS")
    print(term.black_on_darkkhaki("─────────CMD─────────"))

def printLogo():
    print()
    print(term.black_on_darkkhaki(""))
    schedule()

def schedule():
    schedule = True
    while schedule == True:
        userInput = input(">>>  ").lower()
        if userInput[:4] == "help":
            startHelp(userInput)
            schedule = False
        if userInput[:3] == "add":
            startAdd(userInput)
            schedule = False
        if userInput[:3] == "dir":
            startDir(userInput)
            schedule = False

def startHelp(input):
    input = input.split()
    if input[1] == "add":
        print(term.black_on_darkkhaki("┌─────────HELP─────────────────────────────────┐"))
        print(term.black_on_darkkhaki("│add [name] [dd/mm/yyyy] [time (13:12)]  (desc)│"))
        print(term.black_on_darkkhaki("│- creates a new file with a specified name in │"))
        print(term.black_on_darkkhaki("│  specified directory                         │"))
        print(term.black_on_darkkhaki("└──────────────────────────────────────────────┘"))
    if input[1] == "remove":
        print(term.black_on_darkkhaki("┌─────────HELP─────────────────────────────────┐"))
        print(term.black_on_darkkhaki("│remove [name]                                 │"))
        print(term.black_on_darkkhaki("│- deletes a  file with a specified name in    │"))
        print(term.black_on_darkkhaki("│  specified directory                         │"))
        print(term.black_on_darkkhaki("└──────────────────────────────────────────────┘"))
    if input[1] == "dir":
        print(term.black_on_darkkhaki("┌─────────HELP─────────────────────────────────┐"))
        print(term.black_on_darkkhaki("│dir                                           │"))
        print(term.black_on_darkkhaki("│- shows full  user directory                  │"))
        print(term.black_on_darkkhaki("└──────────────────────────────────────────────┘"))
    if input[1] == "help":
        print(term.black_on_darkkhaki("┌─────────HELP─────────────────────────────────┐"))
        print(term.black_on_darkkhaki("│help (command)                                │"))
        print(term.black_on_darkkhaki("│- explains what the specified command does    │"))
        print(term.black_on_darkkhaki("└──────────────────────────────────────────────┘"))
    else:
        print(term.black_on_darkkhaki("┌─────────HELP─────────────────────────────────┐"))
        print(term.black_on_darkkhaki("│help (command)                                │"))
        print(term.black_on_darkkhaki("│add [name] [dd/mm/yyyy] [time (13:12)]  (desc)│"))
        print(term.black_on_darkkhaki("│remove [name]                                 │"))
        print(term.black_on_darkkhaki("│dir                                           │"))
        print(term.black_on_darkkhaki("└──────────────────────────────────────────────┘"))
    printLogo()

def startAdd(input):
    print(term.black_on_darkkhaki("┌─────────ADD─────────┐"))
    print(term.black_on_darkkhaki("└─────────────────────┘"))
    input = input.split()
    
    printLogo()

def startDir(input):
    print(term.black_on_darkkhaki("─────────DIR─────────"))
    list_files("OS")
    input = input.split()

if __name__ == "__main__":
    start()