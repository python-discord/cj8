from .blessed_functions import print_tree, clear_term, print_box, print_loading
from .generalfunctions import inAny
from virtualbox.argssystem.functions import expand_args
from virtualbox.argssystem.classes import Keyword, Optional, Flag
from virtualbox.exceptions import NoSuchFileOrDirectory
from virtualbox.exceptions import CommandNotFound
from virtualbox.unicode import encode
from virtualbox.cryptology import encrypt
from virtualbox.config import MAIN_PATH

import string
import random
import time


# COMMAND LIST
functions_list = []
user_commands = {}

failed_tasks = 0
VULNERABILITIES = ["clue1","clue2"]
OSlog = ['unknown user: connected,']


# wrappers
def add_function(names, *args):
    def add(function):
        for i in names:
            user_commands[i] = len(functions_list)
        functions_list.append((function, args))
        return function
    return add


# getcommands
def get_entry(name):
    try:
        return functions_list[user_commands[name]]
    except KeyError:
        raise CommandNotFound()


def get_command(name):
    return get_entry(name)[0]


def get_command_args(name):
    return get_entry(name)[1]


def get_command_doc(name):
    return get_command(name).__doc__


# COMMAND LIST


def add_failure(value):
    global failed_tasks
    failed_tasks += value
    print(f"DEBUG: failues: {failed_tasks}")
    OSlog.append(f"SECURITY AI: became more aware of unknown user,")


@add_function(("ls", "dir"), "fs", "user")
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


@add_function(("cd", ), 'user_input', "fs", "user")
@expand_args(0, "path")
def cd(path: str, fs, user):
    """cd [path:string]
    [EXTEND]
    cd - change directory to specified path
    """
    fs.copy(fs.getDir(user, path.split("/")))
    print_box("getdir", fs.stringList(user))


@add_function(("tree", ), 'fs', 'user')
def dir_cat(fs, user):
    """dir
    [EXTEND]
    dir = print file structure
    """
    print_tree("dir", fs, user)


@add_function(("mkdir", "makedirectory"), 'user_input', 'fs', 'user')
@expand_args(0, "path")
def mkdir(path: str, fs, user):
    """mkdir [path:string]
    [EXTEND]
    mdkir - creates direcotry that will have specified path
    """
    tmp = path.split("/")
    fs.getDir(user, "" if len(tmp) == 0 else tmp[:-1]).mkdir(user, tmp[-1])


@add_function(("touch", "add"), 'user_input', 'fs', 'user')
@expand_args(0, "path")
def add(path: str, fs, user):
    """add [path:string]
    [EXTEND]
    add - creates file that will have specified path
    """
    tmp = path.split("/")
    fs.getDir(user, "" if len(tmp) == 0 else tmp[:-1]).touch(user, tmp[-1])


@add_function(("rm", "remove"), "user_input", "fs", "user")
@expand_args(0, "path")
def rm(path: str, fs, user):
    """rm [path:string]
    [EXTEND]
    rm - removes file or folder that have specified path
    """
    tmp = path.split("/")
    fs.get(user, "" if len(tmp) == 0 else tmp[:-1]).rm(user, tmp[-1])


@add_function(("cp", "copy"), "user_input", "fs", "user")
@expand_args(0, "from_path", "to_path")
def cp(from_path: str, to_path: str, fs, user):
    """cp [from:string] [to:string]
    [EXTEND]
    cp - copies file or directory form 1 path to another
    """
    fs.cp(user, from_path.split("/"), to_path.split("/"))


@add_function(("mv", "move"), "user_input", "fs", "user")
@expand_args(0, "from_path", "to_path")
def mv(from_path: str, to_path: str, fs, user):
    """mv [from:string] [to:string]
    [EXTEND]
    mv - moves file or directory form 1 path to another.
    can be used to rename directories
    """
    fs.mv(user, from_path.split("/"), to_path.split("/"))


@add_function(("help", "h"), "user_input")
@expand_args(0, "name", "extend")
def help_function(name: Optional(str, None), extend: Flag(True) = False):
    """help [function:string] [extend if present print more detailed help]
     [EXTEND]
     help - hymmm i wonder what it does?
     """
    if name is None:
        print_box("commands", user_commands.keys())
        return

    to_print = get_command_doc(name).split("[EXTEND]")
    print_box('helper', to_print[0].split("\n") )

    if extend:
        print_box('helper', to_print[1].strip())


@add_function(("encrypt", "enc"), "user_input", "fs", "user")
@expand_args(0, "file", "password", "mode")
def user_encrypt(file: str, password: encode, fs, user, mode: Keyword(int) = 2):
    """encrypt [file:string] [password:string or int(mode 3)] [mode:int default 2]
    [EXTEND]
    encrypt - encrypts file using 1 of 4 encryption algoritms
    """
    fs.getFile(user, file.split("/")).encrypt(user, password, mode)


@add_function(("encryptword", "encword"), "user_input")
@expand_args(0, "phrashe", "password", "mode")
def encryptword(phrashe: encode, password: encode, mode: Keyword(int) = 2):
    """encrypt [phrashe:string] [password:string or int(mode 3)] [mode:int default 2]
    [EXTEND]
    encryptword - encrypts phrahse using 1 of 4 encryption algoritms and prints it back to user
    """
    print(encrypt(phrashe, password, mode=mode))


@add_function(("decrypt", "dec"), "user_input", "fs", "user")
@expand_args(0, "file", "password", "mode")
def decrypt(file: str, password: encode, fs, user, mode: Keyword(int) = 2):
    """decrypt [file:string] [password:string or int(mode 3)] [mode:int default 2]
    [EXTEND]
    decrypt - decrypts file using 1 of 4 decrytpion algorithms and saves result
    """
    fs.getFile(user, file.split("/")).decrypt(user, password, mode)


@add_function(("decryptread", "dread", "decread"), "user_input", "fs", "user")
@expand_args(0, "file", "password", "mode")
def decryptread(file: str, password: encode, fs, user, mode: Keyword(int) = 2):
    """decryptread [file:string] [password:string or int(mode 3)] [mode:int default 2]
    [EXTEND]
    decryptread - decrypts file using 1 of 4 decrytpion algorithms and prints result
    """
    fs.getFile(user, file.split("/")).decrypt(user, password, mode)


@add_function(("cat", "read"), "user_input", "fs", "user")
@expand_args(0, "file", "bin")
def read(file: str, fs, user, bin: Flag(True) = False):
    """read [file:string] [mode:text]
    [EXTEND]
    read - reads file using binary(bin) or text(text) modes
    """
    print_box("read", [fs.getFile(user, file.split("/")).read(user, bin)])

@add_function(("write", ), "user_input", "fs", "user")
@expand_args(0, "file", "content", "bin")
def write(file: str, content: str, fs, user, bin: Flag(True) = False):
    """write [file:string] [content]
    [EXTEND]
    write - overwrites file with specified content"""
    fs.getFile(user, file.split("/")).write(user, " ".join(content), bin)


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


@add_function(("search", "find"), "user_input", "fs", "user")
@expand_args(0, "what")
def search(what: str, fs, user):
    """search [name:string]
    [EXTEND]
    search - searches for file that contains name in it's name
    """
    "search [name]"
    result = search_back(what, fs.walk(user), "")

    if len(result) == 0:
        raise NoSuchFileOrDirectory

    print_box("search", result)


@add_function(("portscan", "nmap"), "user_input", "fs", "user")
@expand_args(0, "port")
def portscanner(port: Optional(int, None), fs, user):
    """portscan [port:int]
    [EXTEND]
    portscan - scans for port in network
    """
    ports = [2, 5, 7, 12, 15, 19, 20, 22, 26, 31,
             33, 55, 62, 73, 74, 80, 81, 89, 91, 93,
             164, 224, 353, 522, 529, 634, 698, 934, 988, 996]
    port_hint = {22: 'Scannable Ip: 3861.7679.7174.6743.61.59.77.74.65.76.81.40.57.70.61.68.25.59.59.61.75.75.33.75.38.61.77.76.74.71.70.25.76.71.69.38.61.76',
                 164: "net config decryption code: app12ut",
                 "no_hint": 'missing data'}
    if port is not None:
        print_loading(f"Scanning network for port {port}")
        if port in ports:
            if port in port_hint.keys():
                print_this = port_hint[port]
            else:
                print_this = port_hint["no_hint"]
            print_box("PortScanner", [f"Found port in network:", f"{port}/TCP [State: open]", print_this])
        else:
            print_box("PortScanner", [f"Port {port} not found in network"])

    else:
        print_loading("Scanning network for ports")
        print_this = ["Found Ports in network: "]
        for p in ports:
            print_this.append(f"{p}/TCP [State: open]")
        print_box("PortScanner", print_this)


@add_function(("devresetintro", ))
def dev_reset():
    """replace docstring if you want help for this function"""
    # script_dir = os.path.dirname(__file__)
    # script_dir = script_dir.replace('functions/', '') it will crash without argumnts
    with open(MAIN_PATH + 'first_game.txt', 'w') as firstgamefile:
        firstgamefile.truncate()
        firstgamefile.write('0')


def add_vulnerabillity(vulnerability):
    global VULNERABILITIES
    VULNERABILITIES.append(vulnerability)


def remove_vulnerabillity(vulnerability):
    global VULNERABILITIES
    try:
        VULNERABILITIES.remove(vulnerability)
    except ValueError:
        pass


@add_function(("morse", ), "user_input")
@expand_args(0, "user_input")
def morsescan(user_input: str):
    """morse [string of 0/1, separated by *]
        [EXTEND]
        morse - translates morse code
        """
    # inputs must be 010*1020*293 ect seperated by "*"
    character = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    code = ['01', '1000', '1010', '100', '0', '0010', '110', '0000', '00', '0111', '101', '0100', '11', '10', '111',
            '0110', '1101', '010', '000', '1', '001', '0001', '011', '1001', '1011', '1100', '11111', '01111', '00111',
            '00011', '00001', '00000', '10000', '11000', '11100', '11110']

    zipped = zip(code, character)
    morse_dict = dict(list(zipped))
    while True:
        ori_msg = []
        dec_msg = []
        ori_msg.append(user_input)
        new_msg = user_input.split("*")

        for j in range(0, len(new_msg)):
            if new_msg[j] in morse_dict.keys():
                dec_msg.append(morse_dict[new_msg[j]])

        print_box("morsescan",["Decoded Message is: " + ''.join(dec_msg)])  # end the infinite while loop
        OSlog.append(f"unknown user: Decoded Message is: " + ''.join(dec_msg) + ",")
        break


@add_function(("vscan", ))
def hint():
    """vscan
    vscan - scans for vulnerabilities in network
    [EXTEND]
    """
    global VULNERABILITIES
    print_box("vscan",["Looking for vulnerabilities..."])
    time.sleep(3)
    clear_term()
    #selects random vulnerability
    chosen_vulnerability = random.choice(VULNERABILITIES)
    #display our selected vulnerability.
    print_box("vscan",[f"Vulnerability found: {chosen_vulnerability}"])
    #removes vulnerability from the list.
    remove_vulnerabillity(chosen_vulnerability)
    #add 1 failure point.
    add_failure(10)
    OSlog.append(f"unknown user: found vulnerability,")
    OSlog.append(f"SECURITY AI: detecting unknown user,")


def ipcypher(listl):
    lostl = []
    for word in listl:
        retstring = ''
        if len(word) < 8:
            minus = int(8 - len(word))
            word += str('7'*minus)
        for letter in word:
            cyphernum = ord(letter)
            cyphernum -= 40
            ret1_string = retstring.replace('.', '')
            len_string = len(ret1_string)
            len_string / 2
            forbitten_lols = [0, 2, 6, 10, 14]
            if len_string in forbitten_lols:
                retstring += str(cyphernum)
            else:
                retstring += f'.{cyphernum}'
        lostl.append(retstring)
    return lostl
# print(ipcypher(['NetworkSecurityPanelAccessIsNeutronAtomNet']))


def gethint():
    hints = ['hello test fake'] # Words split by a space, words cant be longer than 8 letters, wouldnt recommend longer hint than 4-5 words. Best is 3 words
    return random.choice(hints)


@add_function(("ipsearch", ))
def ipsearch():
    """
    ipsearch
    ipsearch - Search the system for attackable ips
    [EXTEND]
    """
    hint = gethint()
    hintlist = hint.split()
    hintlist = ipcypher(hintlist)
    for item in hintlist:
        random_int = random.randint(1,2)
        for i in range(random_int):
            randip = str(f"{random.randint(100,99999)}.{random.randint(1000,9999)}.{random.randint(100,9999)}.{random.randint(1,999)}")
            clear_term()
            print_box('Found IP', ['Scanning:', randip, 'Not Attackable'])
            time.sleep(0.5)
        clear_term()
        print_box('Found IP', ['Scanning:', item, 'Attackable'])
        time.sleep(0.5)
        if random_int == 1:
            randip = str(f"{random.randint(100,99999)}.{random.randint(1000,9999)}.{random.randint(100,9999)}.{random.randint(1,999)}")
            clear_term()
            print_box('Found IP', ['Scanning:', randip, 'Not Attackable'])
            time.sleep(0.5)
    time.sleep(0.5)
    randip = str(f"{random.randint(100,99999)}.{random.randint(1000,9999)}.{random.randint(100,9999)}.{random.randint(1,999)}")
    clear_term()
    print_box('Found IP', ['Scanning:', randip, 'Not Attackable'])
    time.sleep(1)
    printlist = []
    for item in hintlist:
        printlist.append(item)
    clear_term()
    printlist.append('You can scan these IPs by using "ipscan [ip]!"')
    print_box('Ips found:', printlist)
    OSlog.append(f"unknown user: performed ip search,")


@add_function(("ipscan", ), "user_input")
@expand_args(0, "user_input")
def ipscan(user_input: str):
    """
    ipscan [ip]
    ipscan - decyphers a ip to words
    [EXTEND]
    """
    retstring = ''
    list_letters = list(string.ascii_letters)
    ip = user_input # Change to 0?
    ip_no_dots = ip.replace('.', '')
    range_num = len(ip_no_dots)
    for i in range(0, range_num, 1):
        try:
            num1, num2 = ip_no_dots[i], ip_no_dots[i+1]
        except:
            pass
        else:
            chr_this = int(int(num1 + num2) + 40)
            letter = chr(chr_this)
            if letter in list_letters:
                if i % 2 == 0:
                    retstring += letter
    print_box('Scanned IP:', [f'The Ip: "{ip}"', f'Can be decyphered to: "{retstring}"'])
    OSlog.append(f"unknown user: , The Ip: {ip} Can be decyphered to: {retstring},")


@add_function(("logs", ))
def logs():
    """
        logs
        logs - shows log history
        [EXTEND]
        """
    print_box("LOGS", OSlog)


@add_function(("pwscan", "hashcat"))
def passwordscan():
    """
           pwscan
           pwscan/hashcat - scans locally stored insecure passwords
           [EXTEND]
    """
    pwlist = ['1password', '2password', '3password']
    all1 = list(string.ascii_letters + string.digits)
    this_will_be_stupid = []
    print_box('PasswordScanner', ['Getting Operating System...', 'Filtring FileSystem...', 'Scanning for Passwords...'])
    time.sleep(2)
    clear_term()
    for item in pwlist:
        for i in range(5):
            choiceg = ''
            for _ in range(len(item)):
                choiceg += random.choice(all1)
            for items in this_will_be_stupid:
                print_box(items[0], items[1])
            print_box('PasswordScanner', ['Found Password', choiceg, str('█'*i + '_'*int(5-i))])
            time.sleep(0.3)
            clear_term()
        this_will_be_stupid.append(['PasswordScanner', ['Found Password', item]])
        # print_box('PasswordScanner', ['Found Password', item])
        for items in this_will_be_stupid:
            print_box(items[0], items[1])
        time.sleep(2)
        clear_term()
    lollist = ['Found Passwords:']
    for item in pwlist:
        lollist.append(item)
    print_box('PasswordScanner', lollist)


@add_function(("login", ), "user_input", "fs", "user")
@expand_args(0, "password")
def login(password: str, user):
    user.get()
