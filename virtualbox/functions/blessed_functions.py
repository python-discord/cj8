from config import template
from blessed import Terminal
from time import sleep
import os
term = Terminal()
print(term.home + term.clear + term.move_y(term.height // 2))

BLANK_LINES = 50

def treat_subdir(rest, intend):
    result = []
    for i in rest:
        if isinstance(i, tuple):
            # directories
            if len(result) > 1:  # test for no directory above
                result.append((len(intend) - 1) * ' ' + '├' +i[0])  # new directory branch
            else:  # directory found above
                result.append((len(intend) - 1) * ' ' + '|' + i[0])  # directory chain
            result += treat_subdir(i[1], intend + ' ' * 3)  # increase indent level
        else:
            # files
            if len(result) < 1:  # test for no file above
                result.append(((len(intend) - 4) * ' ') + '└──┐')  # new file branch
            try:
                exception = rest[rest.index(i)+1]
                true_false = True
            except:
                true_false = False
            if true_false == True:
                result.append(((len(intend) - 1) * ' ') + '├' + i)  # list next file
            else:
                result.append(((len(intend) - 1) * ' ') + '└' + i)  # list next file

    return result


def printstart(arg):
    clear_term()
    print(term.green_on_black(arg))
    sleep(0)  # len for each sentence
    print(term.green_on_black("Press Enter to continue"))
    c_input = input()
    return


def clear_term():
    os.system('cls' if os.name=='nt' else 'clear')
    # print(term.clear)


def printhelp_first(arg):
    print(term.green_on_black(arg))


def print_tree(header, directory, user):
    print_box(header, treat_subdir(directory.walk(user), ''))
    # "│", "─", " ┌", "┬", "┐", "├", "┼", "┤", "└", "┴", "┘"]
    # print(term.green_on_black(f'├{indent}{path.basename(root)}/{extra_blank_needed}│'))
    # print(term.green_on_black(f'{sub_indent}{f}{extra_blank_needed}│'))
    # print(term.green_on_black(f '└─ /{header}/' + ('─' * upper_lenght) + '┘'))


def print_box(header, text):
    '''
    header: string
    text: list of strings
    To print a blank line, put a "" (empty string) or "   " (space only) in the list
    '''
    print_this = str("┌─" + f" /{header}/ " + "─" * int(BLANK_LINES - 8 - len(header)) + "─┐" + "\n")
    if text:
        for words in text:
            # if blank line
            if len(str.strip(words)) == 0:
                print_this += str("│ " + " " * int(BLANK_LINES - 4) + " │" + "\n")
            # if not blank line
            else:
                # if fits in one row
                if len(words) <= BLANK_LINES - 4:
                    print_this += str("│ " + words + " " * int(BLANK_LINES - 4 - len(words)) + " │" + "\n")
                # if longer than one row
                else:
                    rows = len(words) // (BLANK_LINES - 4) + (len(words) % (BLANK_LINES - 4) != 0)
                    startpos = [(BLANK_LINES - 4) * row for row in range(rows + 1)]
                    for row in range(rows):
                        # for first row of long line
                        if row == 0:
                            print_this += str("│ " + words[startpos[row]:startpos[row + 1]] + " ┤" + "\n")
                        # for middle rows of long line
                        elif (row != 0) and (row != rows-1):
                            print_this += str("├ " + words[startpos[row]:startpos[row + 1]] + " ┤" + "\n")
                        # for last row of long line
                        elif row == rows - 1:
                            print_this += str("├ " + words[startpos[-2]:-1] + " " * int(BLANK_LINES - 4 - len(words[startpos[-2]:-1])) + " │" + "\n")

    print_this += str('└─' + f' /{header}/ ' + '─' * int(BLANK_LINES - 7 - len(header)) + '┘' + '\n')
    print(term.green_on_black(print_this))
