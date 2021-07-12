from os import system
from blessed import Terminal

terminal = Terminal()


def main():
    system("resize -s 30 100 | 2> /dev/null")
    with terminal.cbreak(), terminal.hidden_cursor():
        print(terminal.home + terminal.on_midnightblue + terminal.clear)
        print(terminal.is_term_resized(100, 100))
        val = terminal.inkey(timeout=0.02)
        while val != 'q':
            val = terminal.inkey(timeout=0.02)


system("clear")
main()
