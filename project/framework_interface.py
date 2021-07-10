from os import walk, path, sep
from blessed import Terminal

cl = ["│", "─", "┌", "┬", "┐", "├", "┼", "┤", "└", "┴", "┘"]

def list_files(startpath):
    print('── /System/ ──')
    for root, dirs, files in walk(startpath):
        level = root.replace(startpath, '').count(sep)
        indent = ' ' * 4 * (level)
        print('┌'+'{}{}/'.format(indent, path.basename(root)))
        subindent ='├' +'─' * 4 * (level + 1)
        for f in files:
            print('{}{}'.format(subindent, f))

list_files("Project")
