from random import random
from time import sleep

from virtualbox.config import BLANK_LINES


def echo(args, term, **keywords):
    print(term.green_on_black(str(args)), **keywords, flush=True)


def genl(term, args):
    if len(args) != 0:
        return args + term.move_left(len(args)) + term.move_down(1)
    return term.move_down(1)


def echol(term, args):
    echo(genl(term, args), term)


def request(args, term, hist=[]):
    echo(args, term, end='')
    cursor = 0
    hpos = 0
    hist.insert(0, '')

    with term.cbreak():
        while True:
            key = term.inkey()
            if key.is_sequence:
                if key.code == term.KEY_ENTER:
                    echo('', term)
                    return hist[hpos]
                elif key.code == term.KEY_BACKSPACE and cursor != 0:
                    hist[hpos] = hist[hpos][:-1]

                    echo(term.move_left(1) + ' ' + term.move_left(1), term, end='')

                    cursor -= 1
                elif key.code == term.KEY_LEFT and cursor != 0:
                    cursor -= 1
                    echo(term.move_left(1), term, end='')
                elif key.code == term.KEY_RIGHT and cursor != len(hist[hpos]):
                    cursor += 1
                    echo(term.move_right(1), term, end='')
                elif key.code == term.KEY_UP and hpos + 1 != len(hist):
                    echo(term.move_x(len(args)) + " "*len(hist[hpos]), term, end='')
                    hpos += 1
                    cursor = len(hist[hpos])
                    echo(term.move_x(len(args)) + hist[hpos], term, end='')
                elif key.code == term.KEY_DOWN and hpos != 0:
                    echo(term.move_x(len(args)) + " "*len(hist[hpos]), term, end='')
                    hpos -= 1
                    cursor = len(hist[hpos])
                    echo(term.move_x(len(args)) + hist[hpos], term, end='')
            else:
                hist[hpos] = hist[hpos][:cursor] + key + hist[hpos][cursor:]
                echo(hist[hpos][cursor:] + term.move_x(cursor + 1 + len(args)), term, end='')
                cursor += 1


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


def termstart(arg, term):
    clear_term(term)
    echo(arg, term)
    sleep(0)  # len for each sentence
    echo("Press Enter to continue", term)
    request('', term)
    return


def print_tree(header, directory, user, term):
    print_box(header, treat_subdir(directory.walk(user), ''), term)
    # "│", "─", " ┌", "┬", "┐", "├", "┼", "┤", "└", "┴", "┘"]


def dc(char, index):
    if len(char) <= index or len(char) == 0:
        return "─"
    if char[index] in ("│", "┌", "┬", "┐", "├", "┼", "┤"):
        return "┴"
    return "─"


def print_box(header, text, term):
    '''
    header: string
    text: list of strings
    To term a blank line, put a "" (empty string) or "   " (space only) in the list
    '''
    term_this = str("┌─" + f" /{header}/ " + "─" * int(BLANK_LINES - 8 - len(header)) + "─┐" + "\n")
    if text:
        for words in text:
            # if blank line
            if len(str.strip(words)) == 0:
                term_this += str("│ " + " " * int(BLANK_LINES - 4) + " │" + "\n")
            # if not blank line
            else:
                # if fits in one row
                if len(words) <= BLANK_LINES - 4:
                    term_this += str("│ " + words + " " * int(BLANK_LINES - 4 - len(words)) + " │" + "\n")
                # if longer than one row
                else:
                    rows = len(words) // (BLANK_LINES - 4) + (len(words) % (BLANK_LINES - 4) != 0)
                    startpos = [(BLANK_LINES - 4) * row for row in range(rows + 1)]
                    for row in range(rows):
                        # for first row of long line
                        if row == 0:
                            term_this += str("│ " + words[startpos[row]:startpos[row + 1]] + " ┤" + "\n")
                        # for middle rows of long line
                        elif (row != 0) and (row != rows-1):
                            term_this += str("├ " + words[startpos[row]:startpos[row + 1]] + " ┤" + "\n")
                        # for last row of long line
                        elif row == rows - 1:
                            term_this += str("├ " + words[startpos[-2]:] + " " * int(BLANK_LINES - 4 - len(words[startpos[-2]:])) + " │" + "\n")

    term_this += str('└─' + f' /{header}/ ' + '─' * int(BLANK_LINES - 7 - len(header)) + '┘' + '\n')
    echo(term_this, term)


def clear_term(term):
    echo(term.clear, term)


def print_loading(prompt, term):
    '''
    prompt: str
    clears screen and terms a loading bar following the prompt
    symbol for loadng bar LOADING_BAR read from config
    used by portscanner in command_functions
    '''
    term_this = prompt + " "
    for i in range(BLANK_LINES - len(prompt)):
        echo(term.home + term.clear + term.move_y(term.height // 2) + term.green_on_black(term_this), term)
        term_this += "█"
        sleep(random()/2)
