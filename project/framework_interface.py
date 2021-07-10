from os import walk, path, sep
from blessed import Terminal
term = Terminal()

cl = ["│", "─", "┌", "┬", "┐", "├", "┼", "┤", "└", "┴", "┘"]

print(term.home +  term.clear + term.move_y(term.height // 2))

def list_files(startpath):
    print(term.black_on_darkkhaki('── /System/ ──'))
    for root, dirs, files in walk(startpath):
        level = root.replace(startpath, '').count(sep)
        indent = ' ' * 4 * (level)
        print(term.black_on_darkkhaki('┌'+'{}{}/'.format(indent, path.basename(root))))
        subindent ='├' +'─' * 4 * (level + 1)
        for f in files:
            print(term.black_on_darkkhaki('{}{}'.format(subindent, f)))

list_files("Project")
