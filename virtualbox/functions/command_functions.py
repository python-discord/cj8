from .blessed_functions import print_box
from .blessed_functions import print_tree
from .generalfunctions import inAny
from virtualbox.exceptions import NoSuchFileOrDirectory
import random
import time







def random_test():
    print_box("OS SECURITY",
            ["SECURITY BREACH DETECTED",
            """         ____,'`-, """,
            """         _,--'   ,/::.; """,
            """      ,-'       ,/::,' `---.___        ___,_ """,
            """      |       ,:';:/        ;'"``--./ ,-^.;--. """,
            """       |:     ,:';,'         '         `.   ;`   `-. """,
            """        \:.,:::/;/ -:.                   `  | `     `-. """,
            """         \:::,'//__.;  ,;  ,  ,  :.`-.   :. |  ;       :. """,
            """          \,',';/O)^. :'  ;  :   '__` `  :::`.       .:' ) """,
            """          |,'  |\__,: ;      ;  '/O)`.   :::`;       ' ,' """,
            """               |`--''            \__,' , ::::(       ,' """,
            """               `    ,            `--' ,: :::,'\   ,-' """,
            """                | ,;         ,    ,::'  ,:::   |,' """,
            """                |,:        .(          ,:::|   ` """,
            """                ::'_   _   ::         ,::/:| """,
            """               ,',' `-' \   `.      ,:::/,:| """,
            """             | : _  _   |   '     ,::,' ::: """,
            """              | \ O`'O  ,',   ,    :,'   ;:: """,
            """               \ `-'`--',:' ,' , ,,'      :: """,
            """                ``:.:.__   ',-','        ::' """,
            """                       |:  ::::.       ::' """,
            """                       |:  ::::::    ,::' """
            ])
    from virtualbox.project import add_failure
    print("enter animal above...")
    user_input = input(">>>  ")
    if user_input.lower() == "dog":
        print("correct")
        add_failure()
    else:
        print("incorrect")


def ls(fs, user):
    "ls"
    print_box("ls", fs.stringList(user))


def cd(user_input, fs, user):
    "cd [path]"
    fs.copy(fs.getDir(user, user_input[1].split("/")))
    print_box("getdir", fs.stringList(user))


def dir_cat(fs, user):
    "dir"
    # print(term.home + term.clear + term.move_y(term.height // 2))
    print_tree("dir", fs, user)


def mkdir(user_input, fs, user):
    "mkdir [path]"
    tmp = user_input[1].split("/")
    fs.getDir(user, "" if len(tmp) == 0 else tmp[:-1]).mkdir(user, tmp[-1])


def add(user_input, fs, user):
    "add [path]"
    tmp = user_input[1].split("/")
    fs.getDir(user, "" if len(tmp) == 0 else tmp[:-1]).touch(user, tmp[-1])


def rm(user_input, fs, user):
    "rm [path]"
    tmp = user_input[1].split("/")
    fs.get(user, "" if len(tmp) == 0 else tmp[:-1]).rm(user, tmp[-1])


def start_help(user_input, fs, user, term):
    print(term.home + term.clear + term.move_y(term.height // 2))
    user_input_dir = {
        "add": ["Help", ["add [file path]", "- creates a new file with a specified name in specified directory"]],
        "remove" : ["Help", ["remove [file path]", "- removes a new file with a specified name in specified directory"]],
        "dir": ["Help",  ["dir", "- shows full user directory"]],
        "help" : ["Help", ["help (command)", "- explains what the specific command does"]],
        "quickcrypt": ["Help", ["quickcrypt (file path) (password)", "- file encryption tool"]],
        "read":["Help", ["read (file path)", "- reads a files content"]],
        "search": ["Help", ["search (file path)", "- searches directory for a specific file"]],
        "portscan":["Help", ["portscan", "- searches for open ports in the operating system network"]],
        "cd": ["Help", ["cd", "- go to a target directory"]],
        "cat": ["Help", ["cat", "- go to a target directory"]]
    }
    if user_input[1] in user_input_dir.keys():
        print(term.green_on_black(print_box(user_input[1], user_input_dir[user_input[1]])))
    else:
        print(term.green_on_black(print_box("Help", ["help (command)",
                                                     "add [name]",
                                                     "remove [name]",
                                                     "dir",
                                                     "read [file path]",
                                                     "quickcrypt [file path] [password]",
                                                     "search [name]",
                                                     "portscan",
                                                     "walk",
                                                     "cd"
                                                     ])))


def quickcrypt(user_input, fs, user):
    "quickcrypt [file path] [password] [mode:2]"
    fs.getFile(user_input[1]).encrypt(user_input[1], user_input[2], user_input[3] if len(user_input) >= 3 else 2)


def read(user_input, fs, user):
    "read [file path]"
    print(fs.getFile(user, user_input[1].split("/")).Read(user))


def search_back(what, walk, piervous):
    result = []
    for i in walk:
        if isinstance(i, tuple):
            if inAny(what, i[0]):
                result.append(piervous + "/" + i[0])
            result += search_back(what, i[1], piervous + "/" + i[0])
        elif inAny(what, i):
            result.append(piervous + "/" + i)
    return result


def search(user_input, fs, user):
    "search [name]"
    result = search_back(user_input[1:], fs.walk(user), "")

    if len(result) == 0:
        raise NoSuchFileOrDirectory

    print_box("search", result)


def portscanner(user_input, fs, user):
    from virtualbox.project import clear_term
    from random import randint
    # try:
    #     # if user_input contains specific port specifies var
    #     if user_input[1]:
    #         use_true = 'temp'
    # except:
    #     pass
    # ports = [22, 80, 9929, 8898, 22542, 187, 32312]
    # outputs = ['not a hint', 'not a hint', 'not a hint', 'not a hint', 'not a hint', 'a hint', 'a hint', 'a hint', 'a hint']
    # # if specified var (= if user_input contains specific port)
    # if use_true:
    #     # Different Prints to show user a portscanner experience and show hint/ no hint
    #     print_box("PortScanner", f'Scanning Network for Port: {user_input}')
    #     time.sleep(1)
    #     clear_term()
    #     print_box("PortScanner", f"Found Port in Network: \n    {port}/TCP [State: open] \n    Scanning Port... \n")
    #     time.sleep(1)
    #     clear_term()
    #     output = random.choice(outputs)
    #     clear_term()
    #     print_box("PortScanner",f'Port {inp} attackable. \n    Attack launchend. \n    Output: {output} \n')
    # else:
    #     # 5-7 to show user a portscanner experience and show hint/ no hint
    #     for i in range(randint(5, 7)):
    #         port = ports[i]
    #         print_box("PortScanner",f"Found Port in Network: \n    {port}/TCP [State: open] \n    Scanning Port... \n")  # term.green_on_black
    #         time.sleep(0.4)
    #     inp = int(input('Select a port to scan: '))
    #     with term.cbreak():
    #         val = ''
    #         if int(val.lower()) in ports:
    #             output = random.choice(outputs)
    #             time.sleep(3)
    #             clear_term()
    #             print_box("PortScanner",f'Port {inp} attackable. \n    Attack launchend. \n    Output: {output} \n')
    #
    #         else:
    #             print_box("PortScanner",'The Port you entered wasnt found in the Network!')


# COMMAND LIST
user_commands = {"ls": ls,
                 "touch": add,
                 "add": add,
                 "mkdir": mkdir,
                 "rm": rm,
                 "dir": dir_cat,
                 "h": help,
                 "help": help,
                 "quickcrypt": quickcrypt,
                 "read": read,
                 "search": search,
                 "portscan": portscanner,
                 "cd": cd
}

