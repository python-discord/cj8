from config import template


def treat_subdir(rest, intend):
    result = []
    for i in rest:
        if isinstance(i, tuple):
            result.append(intend + i[0])
            result += treat_subdir(i[1], intend + '─'*4)
        else:
            result.append(intend + i)
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
    ftemplate = '├{:<' + str(max_len) + '}│'

    print(template.format('┌', header, shift, '┐'))
    print("\n".join(ftemplate.format(i) for i in text))
    print(template.format('└', header, shift, '┘'))
