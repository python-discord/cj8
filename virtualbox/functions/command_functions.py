from .blessed_functions import print_box, print_tree, clear_term, print_loading
from .generalfunctions import inAny
from virtualbox.exceptions import NoSuchFileOrDirectory
from virtualbox.exceptions import CommandNotFound
from virtualbox.vulnerabilities import VULNERABILITIES, add_failure, add_vulnerabillity, remove_vulnerabillity
from virtualbox.config import MAIN_PATH
import random
import time


failed_tasks = 0


def add_failure():
    global failed_tasks
    failed_tasks += 1
    print(f"DEBUG: failures: {failed_tasks}")


# COMMAND LIST
def ls(fs, user):
    """ls
    ls - list files and directories in current directory
    [EXTEND]
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
        add_failure(5)
    else:
        print("incorrect")
    clear_term()


def add_failure(value):
    global failed_tasks
    failed_tasks += value
    print(f"DEBUG: failues: {failed_tasks}")


def cd(user_input, fs, user):
    """cd [path:string]
    cd - change directory to specified path
    [EXTEND]
    """
    fs.copy(fs.getDir(user, user_input[1].split("/")))
    print_box("getdir", fs.stringList(user))


def dir_cat(fs, user):
    """dir
    dir = print file structure
    [EXTEND]
    """
    "dir"
    print_tree("dir", fs, user)


def mkdir(user_input, fs, user):
    """mkdir [path:string]
    mdkir - creates direcotry that will have specified path
    [EXTEND]
    """
    tmp = user_input[1].split("/")
    fs.getDir(user, "" if len(tmp) == 0 else tmp[:-1]).mkdir(user, tmp[-1])
    print_box("mkdir", [f"Created file {tmp}"])

def add(user_input, fs, user):
    """add [path:string]
    add - creates file that will have specified path
    [EXTEND]
    """
    tmp = user_input[1].split("/")
    fs.getDir(user, "" if len(tmp) == 0 else tmp[:-1]).touch(user, tmp[-1])


def rm(user_input, fs, user):
    """rm [path:string]
    rm - removes file or folder that have specified path
    [EXTEND]
    """
    tmp = user_input[1].split("/")
    fs.get(user, "" if len(tmp) == 0 else tmp[:-1]).rm(user, tmp[-1])


def cp(user_input, fs, user):
    """cp [from:string] [to:string]
    cp - copies file or directory form 1 path to another
    [EXTEND]
    """
    fs.cp(user, user_input[1].split("/"), user_input[2].split("/"))


def mv(user_input, fs, user):
    """mv [from:string] [to:string]
    mv - moves file or directory form 1 path to another.
    can be used to rename directories
    [EXTEND]
    """
    fs.mv(user, user_input[1].split("/"), user_input[2].split("/"))


def help_function(user_input):
    """help [function:string] [extended:string yes or no]
    help - hymmm i wonder what it does?
    [EXTEND]
    """
    if len(user_input) == 1:
        print_box("commands", user_commands.keys())
        return
    to_print = get_command_doc(name).split("[EXTEND]")
    print_box('helper', to_print[0].strip())

    if extend:
        print_box('helper', to_print[1].strip())


def encrypt(user_input, fs, user):
    """encrypt [file:string] [password:string or int(mode 3)] [mode:int default 2]
    encrypt - encrypts file using 1 of 4 encryption algoritms
    [EXTEND]
    """
    file = fs.getFile(user, user_input[1].split("/"))
    mode = int(user_input[3]) if len(user_input) > 3 else 2
    file.encrypt(user, bytes(user_input[2], "utf-8"), mode)


def decrypt(user_input, fs, user):
    """decrypt [file:string] [password:string or int(mode 3)] [mode:int default 2]
    decrypt - decrypts file using 1 of 4 decrytpion algorithms and saves result
    [EXTEND]
    """
    file = fs.getFile(user, user_input[1].split("/"))
    mode = int(user_input[3]) if len(user_input) > 3 else 2
    file.decrypt(user, bytes(user_input[2], "utf-8"), mode)


def decryptread(user_input, fs, user):
    """decryptread [file:string] [password:string or int(mode 3)] [mode:int default 2]
    decryptread - decrypts file using 1 of 4 decrytpion algorithms and prints result
    [EXTEND]
    """
    file = fs.getFile(user, user_input[1].split("/"))
    mode = int(user_input[3]) if len(user_input) > 3 else 2
    print_box("decryptread",[f"{file.decryptRead(user, bytes(user_input[2], 'utf-8'), mode)}"])


def read(user_input, fs, user):
    """read [file:string] [mode:text]
    read - reads file using binary(bin) or text(text) modes
    [EXTEND]
    """
    mode = True if len(user_input) > 2 and user_input[2] == "bin" else False
    print_box("read",[f"{fs.getFile(user, user_input[1].split(' / ')).read(user, mode)}"])


def write(user_input, fs, user):
    """write [file:string] [content]
    write - overwrites file with specified content
    [EXTEND]
    """
    fs.getFile(user, user_input[1].split("/")).write(user, " ".join(user_input[2:]))


def quickcrypt(user_input, fs, user):
    """quickcrypt [file path] [password] [mode:2]
    quickcrypt - decrypts a file using a given password
    [EXTEND]
    """
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
    search - searches for file that contains name in it's name
    [EXTEND]
    """
    "search [name]"
    result = search_back(user_input[1:], fs.walk(user), "")

    if len(result) == 0:
        raise NoSuchFileOrDirectory

    print_box("search", result)


@add_function(("portscann", "nmap"), "user_input", "fs", "user", "term")
@expand_args(0, "port")
def portscanner(user_input, fs, user):
    """portscan [port:int]
    portscan - scans for port in network
    [EXTEND]
    """
    ports = [str(port) for port in [22, 80, 9929, 8898, 22542, 187, 32312]]
    outputs = ['not a hint',
    'not a hint', 'not a hint', 'not a hint', 'not a hint', 'a hint', 'a hint', 'a hint', 'a hint']
    # if specified var (= if user_input contains specific port)
    if len(user_input)>1:
        # Different Prints to show user a portscanner experience and show hint/ no hint
        print_loading(f"Scanning Network for Port {user_input[1]}")
        print_box("PortScanner", [f"Found Port in Network:", f"{user_input[1]}/TCP [State: open]"])
        time.sleep(5)
        print_loading(f"Scanning Port {user_input[1]}")
        output = random.choice(outputs)
        print_box("PortScanner", [f"Port {user_input[1]} attackable. ", "Attack launchend. ", f"Output: {output}"])
 



@add_function(("devresetintro", ))
def dev_reset():
    """replace docstring if you want help for this function"""
    # script_dir = os.path.dirname(__file__)
    # script_dir = script_dir.replace('functions/', '') it will crash without argumnts
    with open(MAIN_PATH + 'first_game.txt', 'w') as firstgamefile:
        firstgamefile.truncate()
        firstgamefile.write('0')


def add_vulnerabillity(vulnerability):
    VULNERABILITIES.append(vulnerability)

def remove_vulnerabillity(vulnerability):
    VULNERABILITIES.remove(vulnerability)


@add_function(("vscan", ))
def hint():
    """replace docstring if you want help for this function"""
    print_box("vscan", ["Looking for vulnerabilities..."])
    # selects random vulnerability
    chosen_vulnerability = random.choice(VULNERABILITIES)
    # display our selected vulnerability.
    print_box("vscan", [f"Vulnerability found: {chosen_vulnerability}"])
    # removes vulnerability from the list.
    remove_vulnerabillity(chosen_vulnerability)
    # add 1 failure point.
    add_failure()

