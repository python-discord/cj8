from config import template
from time import sleep


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


def print_tree(header, directory, user):
    print_box(header, treat_subdir(directory.walk(user), ''))
    # "│", "─", " ┌", "┬", "┐", "├", "┼", "┤", "└", "┴", "┘"]
    # print(term.green_on_black(f'├{indent}{path.basename(root)}/{extra_blank_needed}│'))
    # print(term.green_on_black(f'{sub_indent}{f}{extra_blank_needed}│'))
    # print(term.green_on_black(f '└─ /{header}/' + ('─' * upper_lenght) + '┘'))


def print_box(header, text):
    if len(text) == 0:
        print(template.format('┌', header, "", '┐'))
        print(template.format('└', header, "", '┘'))
        return

    max_len = max(map(len, text))
    if max_len < len(header) + 4:
        max_len = len(header) + 4
    shift = "─"*(max_len - len(header) - 3)
    ftemplate = '│{:<' + str(max_len) + '}│'

    print(template.format('┌', header, shift, '┐'))
    print("\n".join(ftemplate.format(i) for i in text))
    print(template.format('└', header, shift, '┘'))
