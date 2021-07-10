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

def printLogo():
    print()
    print(term.black_on_darkkhaki("---------------------CMD---------------------"))
    schedule()

def schedule():
    schedule = True
    while schedule == True:
        userInput = input(term.black_on_darkkhaki(">>>  "))
        if userInput[:4] == "help":
            startHelp(userInput)
            schedule = False
        if userInput[:3] == "add":
            startAdd(userInput)
            schedule = False

def startHelp(input):
    print(term.black_on_darkkhaki("-----------------------Help-----------------------"))
    print(term.black_on_darkkhaki("help (command)"))
    print(term.black_on_darkkhaki("add [name] [dd/mm/yyyy] [time (13:12)]  (desc)"))
    print(term.black_on_darkkhaki("remove [name]"))
    input = input.split()

    printLogo()

def startAdd(input):
    print(term.black_on_darkkhaki("-----------------------Add------------------------"))
    input = input.split()
    
    printLogo()

if __name__ == "__main__":
    start()