from virtualbox.config import template
from time import sleep
from random import random
import os
from blessed import Terminal
term = Terminal()
print(term.home + term.clear + term.move_y(term.height // 2))

BLANK_LINES = 70


def treat_subdir(rest, add):
    result = []
    for j, i in enumerate(rest):
        s = '└' if len(rest) - 1 == j else '├'
        if isinstance(i, tuple):
            if len(i[1]) == 0:
                result.append(add + s + '─' + i[0])
            else:
                result.append(add + s + '┬' + i[0])
                result += treat_subdir(i[1], add + (" " if s == '└' else '│'))
        else:
            result.append(add + s + i)
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


def lc(char, index):
    if len(char) <= index or len(char) == 0:
        return "│"
    if char[index] in ("─", "┬", "┐", "┼", "┤"  "┴", "┘"):
        return "├"
    return "│"


def rc(char, index):
    if len(char) <= index or len(char) == 0:
        return "│"
    if char[index] in ("─", "┌", "┬", "├", "┼", "└", "┴"):
        return "├"
    return "│"


def uc(char, index):
    if len(char) <= index or len(char) == 0:
        return "─"
    if char[index] in ("│", "├", "┼", "┤", "└", "┴", "┘"):
        return "┬"
    return "─"


def dc(char, index):
    if len(char) <= index or len(char) == 0:
        return "─"
    if char[index] in ("│", "┌", "┬", "┐", "├", "┼", "┤"):
        return "┴"
    return "─"


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
                            print_this += str("├ " + words[startpos[-2]:] + " " * int(BLANK_LINES - 4 - len(words[startpos[-2]:])) + " │" + "\n")

    print_this += str('└─' + f' /{header}/ ' + '─' * int(BLANK_LINES - 7 - len(header)) + '┘' + '\n')
    print(term.green_on_black(print_this))


# print_box from sirmerge

# def print_box(header, text):
#     if len(text) == 0:
#         print(template.format('┌', header, "", '┐'))
#         print(template.format('└', header, "", '┘'))
#         return
#
#     max_len = max(map(len, text))
#     if max_len < len(header) + 4:
#         max_len = len(header) + 4
#
#     shift = len(header) + 3
#
#     ushift = ""
#     dshift = ""
#     for i in range(max_len - shift):
#         ushift += uc(text, shift + i)
#         dshift += dc(text, shift + i)
#
#     ftemplate = '{:<' + str(max_len) + '}'
#
#     print(template.format('┌', uc(text[0], 0), header, ushift, '┐'))
#     print("\n".join(lc(i, 0) + ftemplate.format(i) + rc(i, -1) for i in text))
#     print(template.format('└', dc(text[-1], 0), header, dshift, '┘'))


def print_loading(prompt):
    '''
    prompt: str
    clears screen and prints a loading bar following the prompt
    symbol for loadng bar LOADING_BAR read from config
    used by portscanner in command_functions
    '''
    print_this = prompt + " "
    for i in range(BLANK_LINES - len(prompt)):
        clear_term()
        print(term.home + term.clear + term.move_y(term.height // 2) + term.green_on_black(print_this))
        print_this += "█"
        sleep(random()/2)
