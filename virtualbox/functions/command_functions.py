from .blessed_functions import print_box
from .blessed_functions import print_tree
from .generalfunctions import inAny
from virtualbox.exceptions import NoSuchFileOrDirectory
from exceptions import CommandNotFound
<<<<<<< HEAD
import time
from blessed import Terminal
import random
term = Terminal()
=======

>>>>>>> parent of 67bb69f (new argument system, unicode in spearate file and in config)

# COMMAND LIST
def ls(fs, user):
    """ls
    [EXTEND]
    ls - list files and directories in current directory
    """
    print_box("ls", fs.stringList(user))


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
    print("enter animal above...")
    user_input = input(">>>  ")
    if user_input.lower() == "dog":
        print("correct")
        add_failure()
    else:
        print("incorrect")


def cd(user_input, fs, user):
    """cd [path:string]
    [EXTEND]
    cd - change directory to specified path
    """
    fs.copy(fs.getDir(user, user_input[1].split("/")))
    print_box("getdir", fs.stringList(user))


def dir_cat(fs, user):
    """dir
    [EXTEND]
    dir = print file structure
    """
    "dir"
    print_tree("dir", fs, user)


def mkdir(user_input, fs, user):
    """mkdir [path:string]
    [EXTEND]
    mdkir - creates direcotry that will have specified path
    """
    tmp = user_input[1].split("/")
    fs.getDir(user, "" if len(tmp) == 0 else tmp[:-1]).mkdir(user, tmp[-1])


def add(user_input, fs, user):
    """add [path:string]
    [EXTEND]
    add - creates file that will have specified path
    """
    tmp = user_input[1].split("/")
    fs.getDir(user, "" if len(tmp) == 0 else tmp[:-1]).touch(user, tmp[-1])


def rm(user_input, fs, user):
    """rm [path:string]
    [EXTEND]
    rm - removes file or folder that have specified path
    """
    tmp = user_input[1].split("/")
    fs.get(user, "" if len(tmp) == 0 else tmp[:-1]).rm(user, tmp[-1])


def cp(user_input, fs, user):
    """cp [from:string] [to:string]
    [EXTEND]
    cp - copies file or directory form 1 path to another
    """
    fs.cp(user, user_input[1].split("/"), user_input[2].split("/"))


def mv(user_input, fs, user):
    """mv [from:string] [to:string]
    [EXTEND]
    mv - moves file or directory form 1 path to another.
    can be used to rename directories
    """
    fs.mv(user, user_input[1].split("/"), user_input[2].split("/"))


def help_function(user_input):
    """help [function:string] [extended:string yes or no]
    [EXTEND]
    help - hymmm i wonder what it does?
    """
<<<<<<< HEAD
    if len(user_input) == 1:
        print_box("commands", user_commands.keys())
        return

    try:
        to_print = user_commands[user_input[1]].__doc__.split("[EXTEND]")
    except KeyError:
        raise CommandNotFound()

=======
    try:
        to_print = user_commands[user_input[1]].__doc__.split("[EXTEND]")
    except KeyError:
        raise CommandNotFound()

>>>>>>> parent of 67bb69f (new argument system, unicode in spearate file and in config)
    print(to_print[0].strip())
    if len(user_input) > 2 and user_input[2] == "yes":
        print(to_print[1].strip())


def encrypt(user_input, fs, user):
    """encrypt [file:string] [password:string or int(mode 3)] [mode:int default 2]
    [EXTEND]
    encrypt - encrypts file using 1 of 4 encryption algoritms
    """
    file = fs.getFile(user, user_input[1].split("/"))
    mode = int(user_input[3]) if len(user_input) > 3 else 2
    file.encrypt(user, bytes(user_input[2], "utf-8"), mode)


def decrypt(user_input, fs, user):
    """decrypt [file:string] [password:string or int(mode 3)] [mode:int default 2]
    [EXTEND]
    decrypt - decrypts file using 1 of 4 decrytpion algorithms and saves result
    """
    file = fs.getFile(user, user_input[1].split("/"))
    mode = int(user_input[3]) if len(user_input) > 3 else 2
    file.decrypt(user, bytes(user_input[2], "utf-8"), mode)


def decryptread(user_input, fs, user):
    """decryptread [file:string] [password:string or int(mode 3)] [mode:int default 2]
    [EXTEND]
    decryptread - decrypts file using 1 of 4 decrytpion algorithms and prints result
    """
    file = fs.getFile(user, user_input[1].split("/"))
    mode = int(user_input[3]) if len(user_input) > 3 else 2
    print(file.decryptRead(user, bytes(user_input[2], "utf-8"), mode))


def read(user_input, fs, user):
    """read [file:string] [mode:text]
    [EXTEND]
    read - reads file using binary(bin) or text(text) modes
    """
    mode = True if len(user_input) > 2 and user_input[2] == "bin" else False
    print(fs.getFile(user, user_input[1].split("/")).read(user, mode))


def write(user_input, fs, user):
    """write [file:string] [content]
    [EXTEND]
    write - overwrites file with specified content"""
    fs.getFile(user, user_input[1].split("/")).write(user, " ".join(user_input[2:]))


def quickcrypt(user_input, fs, user):
    "quickcrypt [file path] [password] [mode:2]"
    fs.getFile(user_input[1]).encrypt(user_input[1], user_input[2], user_input[3] if len(user_input) >= 3 else 2)


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
    """search [name:string]
    [EXTEND]
    search - searches for file that contains name in it's name
    """
    "search [name]"
    result = search_back(user_input[1:], fs.walk(user), "")

    if len(result) == 0:
        raise NoSuchFileOrDirectory

    print_box("search", result)


def portscanner(user_input, fs, user):
    """portscan [port:int]
    [EXTEND]
    portscan - scans for port in network
    """
    "portscan [int]"
    # try:
    #     # if user_input contains specific port specifies var
    #     if user_input[1]:
    #         use_true = 'temp'
    # except:
    #     pass
<<<<<<< HEAD
    ports = [22, 80, 9929, 8898, 22542, 187, 32312]
    outputs = ['not a hint',
    'not a hint', 'not a hint', 'not a hint', 'not a hint', 'a hint', 'a hint', 'a hint', 'a hint']
    # if specified var (= if user_input contains specific port)
    if len(user_input)>1:
        # Different Prints to show user a portscanner experience and show hint/ no hint
        print_box("PortScanner", [f"Scanning Network for Port: {user_input[1]}"])
        time.sleep(1)
        term.clear
        print_box("PortScanner", [f"Found Port in Network:", f"{user_input[1]}/TCP [State: open]", "Scanning Port..."])
        time.sleep(1)
        term.clear
        output = random.choice(outputs)
        term.clear
        print_box("PortScanner", [f"Port {user_input[1]} attackable. ", "Attack launchend. ", f"Output: {output}"])
    else:
        # 5-7 to show user a portscanner experience and show hint/ no hint
        for i in range(random.randint(5, 7)):
            port = ports[i]
            print_box("PortScanner", [f"Found Port in Network: ", f"{port}/TCP [State: open]", "Scanning Port..."])
            time.sleep(0.4)
        inp = int(input("Select a port to scan: "))
        with term.cbreak():
            if inp in ports:
                output = random.choice(outputs)
                time.sleep(1)
                term.clear
                print_box("PortScanner", [f"Port {inp} attackable. ", "Attack launchend. ", f"Output: {output}"])
            else:
                print_box("PortScanner", ["The Port you entered wasnt found in the Network!"])
=======
    # ports = [22, 80, 9929, 8898, 22542, 187, 32312]
    # outputs = ['not a hint',
    # 'not a hint', 'not a hint', 'not a hint', 'not a hint', 'a hint', 'a hint', 'a hint', 'a hint']
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
    #         print_box("PortScanner",f"Found Port in Netw
    # ork: \n    {port}/TCP [State: open] \n    Scanning Port... \n")  # term.green_on_black
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
    pass
>>>>>>> parent of 67bb69f (new argument system, unicode in spearate file and in config)


# COMMAND LIST
user_commands = {"ls": ls,
                 "touch": add,
                 "add": add,
                 "mkdir": mkdir,
                 "rm": rm,
                 "mv": mv,
                 "cp": cp,
                 "dir": dir_cat,
                 "h": help_function,
                 "help": help_function,
                 "encrypt": encrypt,
                 "decrypt": decrypt,
                 "decryptread": decryptread,
                 "read": read,
                 "write": write,
                 "dir": dir_cat,
                 "quickcrypt": quickcrypt,
                 "read": read,
                 "search": search,
                 "portscan": portscanner,
                 "cd": cd
                 }
