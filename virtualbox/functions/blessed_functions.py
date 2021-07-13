from config import template
from blessed import Terminal
from time import sleep
import os
term = Terminal()
print(term.home + term.clear + term.move_y(term.height // 2))


def treat_subdir(rest, intend):
    result = []
    for i in rest:
        if isinstance(i, tuple):
            # directories
            if len(result) > 1:  # test for no directory above
                result.append((len(intend) - 1) * ' ' + '├' +i[0])  # new directory branch
            else:  # directory found above
                result.append((len(intend) - 1) * ' ' + '│' + i[0])  # directory chain
            result += treat_subdir(i[1], intend + ' ' * 3)  # increase indent level
        else:
            # files
            if len(result) < 1:  # test for no file above
                result.append(((len(intend) - 4) * ' ') + '└──┐')  # new file branch
            result.append(((len(intend) - 1) * ' ') + '│' + i)  # list next file

    return result


def printstart(arg):
    print(term.clear)
    print(term.green_on_black(arg))
    sleep(0)  # len for each sentence
    print(term.green_on_black("Press C to continue"))
    with term.cbreak():
        val = ''
        if val.lower() == 'c':
            return
        else:
            pass


def clear_term():
    print(term.clear)


def print_tree(header, directory, user):
    print_box(header, treat_subdir(directory.walk(user), ''))
    # "│", "─", " ┌", "┬", "┐", "├", "┼", "┤", "└", "┴", "┘"]
    # print(term.green_on_black(f'├{indent}{path.basename(root)}/{extra_blank_needed}│'))
    # print(term.green_on_black(f'{sub_indent}{f}{extra_blank_needed}│'))
    # print(term.green_on_black(f '└─ /{header}/' + ('─' * upper_lenght) + '┘'))


def print_box(header, text):
    if len(text) == 0:
        print(term.green_on_black(template.format('┌', header, "", '┐')))
        print(term.green_on_black(template.format('└', header, "", '┘')))
        return

    max_len = max(map(len, text))
    if max_len < len(header) + 4:
        max_len = len(header) + 4
    shift = "─"*(max_len - len(header) - 3)
    ftemplate = '├{:<' + str(max_len) + '}│'

    print(term.green_on_black(template.format('┌', header, shift, '┐')))
    print(term.green_on_black("\n".join(ftemplate.format(i) for i in text)))
    print(term.green_on_black(template.format('└', header, shift, '┘')))
