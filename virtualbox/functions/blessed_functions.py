from config import template
from blessed import Terminal

term = Terminal()
print(term.home + term.clear + term.move_y(term.height // 2))


def treat_subdir(rest, intend):
    result = []
    for i in rest:
        if isinstance(i, tuple):
            result.append(intend + i[0])
            result += treat_subdir(i[1], intend + '─'*4)
        else:
            result.append(intend + i)
    return result


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
