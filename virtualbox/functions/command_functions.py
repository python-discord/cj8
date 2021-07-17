import random
import string
import time

from virtualbox.argssystem.classes import Flag, Keyword, Optional
from virtualbox.argssystem.functions import expand_args
from virtualbox.config import MAIN_PATH
from virtualbox.cryptology import encrypt
from virtualbox.exceptions import (
    CommandNotFound, InvalidLoginOrPassword, NoSuchFileOrDirectory
)
from virtualbox.unicode import encode

from .blessed_functions import (
    clear_term, echo, print_box, print_loading, print_tree
)

# COMMAND LIST
functions_list = []
user_commands = {}

failed_tasks = 0
VULNERABILITIES = ["clue1", "clue2"]
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
@add_function(("add", "touch"), 'user_input', 'fs', 'user')
@expand_args(0, "path")
def add(path: str, fs, user):
    """add [path:string]
    [EXTEND]
    add - create file with the specified path
    """
    tmp = path.split("/")
    fs.getDir(user, "" if len(tmp) == 0 else tmp[:-1]).touch(user, tmp[-1])


def add_failure(value):
    global failed_tasks
    failed_tasks += value
    echo(f"DEBUG: failues: {failed_tasks}")
    OSlog.append("SECURITY AI: became more aware of unknown user,")


@add_function(("addpermisions", 'chadd'), 'user_input', 'user', 'fs')
@expand_args(0, 'path', 'up', 'op')
def chadd(path: str, up: int, op: int, user, fs):
    '''chadd [path: str] [user permissions: int] [other permissions: int]
    [EXTEND]
    chadd -  add access permissions to the specified file or directory
    4 = read
    2 = write
    1 = execute
    '''
    path = path.split('/')
    fs.get(user, path).chadd(user, up, op)

def add_vulnerabillity(vulnerability):
    global VULNERABILITIES
    VULNERABILITIES.append(vulnerability)


@add_function(("cd", ), 'user_input', "fs", "user", "term", 'rootfs')
@expand_args(0, "path")
def cd(path: str, fs, user, term, rootfs):
    """cd [path:string]
    [EXTEND]
    cd - change directory to the specified path
    """
    if path[0] == '/':
        fs.copy(rootfs.getDir(user, path[1:].split("/")))
    else:
        fs.copy(fs.getDir(user, path.split("/")))
    print_box("Change Directory", fs.stringList(user), term)




@add_function(('chmod', 'changepermisions'), 'user_input', 'user', 'fs')
@expand_args(0, 'path', 'up', 'op')
def chmod(path: str, up: int, op: int, user, fs):
    '''chmod [path: str] [user permissions: int] [other permissions: int]
    [EXTEND]
    chmod - change access permissions of the specified file or directory
    4 = read
    2 = write
    1 = execute
    '''
    path = path.split('/')
    fs.get(user, path).chmod(user, up, op)


@add_function(('chown', 'changeowner'), 'user_input', 'user', 'users', 'fs')
@expand_args(0, 'path', 'name')
def chown(path: str, name: str, user, users, fs):
    '''chown [path:str] [name:str]
    [EXTEND]
    chown - change owner of file or directory to the specified user
    '''
    path = path.split('/')
    if name in users:
        fs.get(user, path).chown(user, users[name])
    else:
        raise NoSuchUser(name)


@add_function(('clear', 'cls'), 'term')
def clear(term):
    '''clear - clear screen
    [EXTEND]
    '''
    clear_term(term)


@add_function(("copy", "cp"), "user_input", "fs", "user")
@expand_args(0, "from_path", "to_path")
def cp(from_path: str, to_path: str, fs, user):
    """cp [from:string] [to:string]
    [EXTEND]
    cp - copy file or folder from the first specified path to the second
    """
    fs.cp(user, from_path.split("/"), to_path.split("/"))


@add_function(("decrypt", "dec"), "user_input", "fs", "user")
@expand_args(0, "file", "password", "mode")
def decrypt(file: str, password: encode, fs, user, mode: Keyword(int) = 2):
    """decrypt [file:string] [password:string or int(mode 3)] [mode:int default 2]
    [EXTEND]
    decrypt - decrypt file using 1 of 4 decryption algorithms and save result
    """
    fs.getFile(user, file.split("/")).decrypt(user, password, mode)


@add_function(("decryptread", "dread", "decread"), "user_input", "fs", "user", 'term')
@expand_args(0, "file", "password", "mode")
def decryptread(file: str, password: encode, fs, user, term, mode: Keyword(int) = 2):
    """decryptread [file:string] [password:string or int(mode 3)] [mode:int default 2]
    [EXTEND]
    decryptread - decrypt file using 1 of 4 decryption algorithms and print result
    """
    print_box('Decrypt Read', fs.getFile(user, file.split("/")).decrypt(user, password, mode), term)


@add_function(("devresetintro", ))
def dev_reset():
    """replace docstring if you want help for this function"""
    # script_dir = os.path.dirname(__file__)
    # script_dir = script_dir.replace('functions/', '') it will crash without argumnts
    with open(MAIN_PATH + 'first_game.txt', 'w') as firstgamefile:
        firstgamefile.truncate()
        firstgamefile.write('0')


@add_function(("dir", "ls"), "fs", "user", "term")
def ls(fs, user, term):
    """ls
    [EXTEND]
    ls - list files and sub-directories in current directory
    """
    print_box("Files", fs.stringList(user), term)


@add_function(("encrypt", "enc"), "user_input", "fs", "user")
@expand_args(0, "file", "password", "mode")
def user_encrypt(file: str, password: encode, fs, user, mode: Keyword(int) = 2):
    """encrypt [file:string] [password:string or int(mode 3)] [mode:int default 2]
    [EXTEND]
    encrypt - encrypt file using 1 of 4 encryption algorithms
    """
    fs.getFile(user, file.split("/")).encrypt(user, password, mode)


@add_function(("encryptword", "encword"), "user_input", 'term')
@expand_args(0, "phrase", "password", "mode")
def encryptword(phrase: encode, password: encode, term, mode: Keyword(int) = 2):
    """encrypt [phrase:string] [password:string or int(mode 3)] [mode:int default 2]
    [EXTEND]
    encryptword - encrypt phrase using 1 of 4 encryption algorithms and print result
    """
    echo(list(map(int, encrypt(phrase, password, mode=mode))), term)


def gethint():
    # Words split by a space, words cant be longer than 8 letters
    # wouldnt recommend longer hint than 4-5 words. Best is 3 words
    hints = ['no_connection false_access AtomToor45tpf unsecure_route unknown missing_port invalid_acces\
        unsecure_route missing_ip zero_access']
    return random.choice(hints)


@add_function(("help", "h"), "user_input", "term")
@expand_args(0, "name", "s")
def help_function(name: Optional(str, None), term, s: Flag(True) = False):
    """help [function:string] [s, to suppress detailed help]
     [EXTEND]
     help - hmm I wonder what it does?
     """
    if name is None:
        print_box("Commands", user_commands.keys(), term)
        return
    to_print = get_command_doc(name).split("[EXTEND]")
    if s:
        print_box('Help', to_print[0].strip().split("\n"), term)
    else:
        print_box('Help', to_print[0].strip().split("\n") + [''] + to_print[1].strip().split("\n"), term)


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
# print(ipcypher(['nineone']))


@add_function(("ipscan", ), "user_input", "term")
@expand_args(0, "user_input")
def ipscan(user_input: str, term):
    """
    ipscan [ip]
    [EXTEND]
    ipscan - decypher the specified IP to words
    """
    retstring = ''
    list_letters = list(string.ascii_letters)
    ip = user_input  # Change to 0?
    ip_no_dots = ip.replace('.', '')
    range_num = len(ip_no_dots)
    for i in range(0, range_num, 1):
        try:
            num1, num2 = ip_no_dots[i], ip_no_dots[i+1]
        except IndexError:
            pass
        else:
            chr_this = int(int(num1 + num2) + 40)
            letter = chr(chr_this)
            if letter in list_letters:
                if i % 2 == 0:
                    retstring += letter
    print_box('IP Scan', [f'IP: "{ip}"', 'decyphers to: ', f"{retstring}"], term)
    OSlog.append(f"unknown user: , IP: {ip} decyphers to: {retstring},")


@add_function(("ipsearch", ), 'term')
def ipsearch(term):
    """
    ipsearch
    [EXTEND]
    ipsearch - Search the system for attackable IPs
    """
    hint = gethint()
    hintlist = hint.split()
    hintlist = ipcypher(hintlist)
    for item in hintlist:
        random_int = random.randint(1, 2)
        for i in range(random_int):
            randip = str(f"{random.randint(100,99999)}.{random.randint(1000,9999)}\
                .{random.randint(100,9999)}.{random.randint(1,999)}")
            clear_term(term)
            print_box('Found IP', ['Scanning:', randip, 'Not Attackable'], term)
            time.sleep(0.5)
        clear_term(term)
        print_box('Found IP', ['Scanning:', item, 'Attackable'], term)
        time.sleep(0.5)
        if random_int == 1:
            randip = str(f"{random.randint(100,99999)}.{random.randint(1000,9999)}\
                .{random.randint(100,9999)}.{random.randint(1,999)}")
            clear_term(term)
            print_box('Found IP', ['Scanning:', randip, 'Not Attackable'], term)
            time.sleep(0.5)
    time.sleep(0.5)
    randip = str(f"{random.randint(100,99999)}.{random.randint(1000,9999)}\
        .{random.randint(100,9999)}.{random.randint(1, 999)}")
    clear_term(term)
    print_box('Found IP', ['Scanning:', randip, 'Not Attackable'], term)
    time.sleep(1)
    printlist = []
    for item in hintlist:
        printlist.append(item)
    clear_term(term)
    printlist.append('You can scan these IPs by using "ipscan [ip]!"')
    print_box('Found IP', printlist, term)
    OSlog.append("unknown user: performed IP search,")


@add_function(('login', 'switchuser'), 'user_input', 'user', 'Users')
@expand_args(0, 'user', 'password')
def su(user: str, password: encode, me, users):
    '''login [user:str] [password:str]
    [EXTEND]
    login - switch current user
    '''
    if user in users and users[user].checkPassword(password):
        me.copy(users[user])
    else:
        raise InvalidLoginOrPassword


@add_function(("logs", ), 'term')
def logs(term):
    """
    logs
    [EXTEND]
    logs - show log history
    """
    print_box("Logs", OSlog, term)


@add_function(("mkdir", "makedirectory"), 'user_input', 'fs', 'user')
@expand_args(0, "path")
def mkdir(path: str, fs, user):
    """mkdir [path:string]
    [EXTEND]
    mdkir - create directory with the specified path
    """
    tmp = path.split("/")
    fs.getDir(user, "" if len(tmp) == 0 else tmp[:-1]).mkdir(user, tmp[-1])


@add_function(("morse", ), "user_input", 'term')
@expand_args(0, "user_input")
def morsescan(user_input: str, term):
    """morse [string of 0/1, separated by *]
    [EXTEND]
    morse - translate morse code
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

        print_box("Morse Scan", ["Decoded Message is: " + ''.join(dec_msg)], term)  # end the infinite while loop
        OSlog.append("unknown user: Decoded Message is: " + ''.join(dec_msg) + ",")
        break


@add_function(("mv", "move"), "user_input", "fs", "user")
@expand_args(0, "from_path", "to_path")
def mv(from_path: str, to_path: str, fs, user):
    """mv [from:string] [to:string]
    [EXTEND]
    mv - move file or folder from the first specified path to the second; can be used to rename directories
    """
    fs.mv(user, from_path.split("/"), to_path.split("/"))


@add_function(("pwscan", "hashcat"), 'term')
def passwordscan(term):
    """
    pwscan
    [EXTEND]
    pwscan/hashcat - scan for insecure passwords stored locally
    """
    pwlist = ['df23jsq', 'qsAtom5', 'LQR', "1234567", "54354fd32", "444hdFAaws", "guuf2321d"]
    all1 = list(string.ascii_letters + string.digits)
    this_will_be_stupid = []
    print_box('Password Scanner', ['Scanning operating system...',
                                  'Scanning file system...',
                                  'Scanning for passwords...'], term)
    time.sleep(2)
    clear_term(term)
    for item in pwlist:
        for i in range(5):
            choiceg = ''
            for _ in range(len(item)):
                choiceg += random.choice(all1)
            for items in this_will_be_stupid:
                print_box(items[0], items[1], term)
            print_box('Password Scanner', ['Found Password', choiceg, str('█'*i + '_'*int(5-i))], term)
            time.sleep(0.3)
            clear_term(term)
        this_will_be_stupid.append(['Password Scanner', ['Found Password', item]])
        # print_box('PasswordScanner', ['Found Password', item])
        for items in this_will_be_stupid:
            print_box(items[0], items[1], term)
        time.sleep(2)
        clear_term(term)
    lollist = ['Found Passwords:']
    for item in pwlist:
        lollist.append(item)
    print_box('Password Scanner', lollist, term)


@add_function(("portscan", "nmap"), "user_input", "fs", "user", 'term')
@expand_args(0, "port")
def portscanner(port: Optional(int, None), fs, user, term):
    """
    portscan (optional[port:int])
    [EXTEND]
    portscan - scan network for port
    """
    ports = [2, 5, 7, 12, 15, 19, 20, 22, 26, 31,
             33, 55, 62, 73, 74, 80, 81, 89, 91, 93,
             164, 224, 353, 522, 529, 634, 698, 934, 988, 996]
    port_hint = {"no_hint": 'missing data',
                 22: 'Scannable IP: 3861.7679.7174.6743.61.59.77.74.65.76.81.40.57.'+
                     '70.61.68.25.59.59.61.75.75.33.75.38.61.77.76.74.71.70.25.76.71.69.38.61.76',
                 164: "net config decryption code: app12ut",
                 7: '444.',
                 74: '5123.',
                 522: '4123',
                 988: '01*1*111*11*0110*01*000*000*011*111*010*100*1*0*11*0110',
                 529: '4359.5770.4464.6574.60.33.40',
                 80: 'shutdown.txt = ttqrsfll',
                 91: "shutdown code = meeting transcript word (6+7+10+11)",
                 62: 'meetingdata decrypt: zwqrt23p'}
    if port is not None:
        print_loading(f"Scanning network for port {port}", term)
        if port in ports:
            if port in port_hint.keys():
                print_this = port_hint[port]
            else:
                print_this = port_hint["no_hint"]
            print_box("Port Scan", [f"Found port in network: {port}/TCP [State: open]", print_this], term)
        else:
            print_box("Port Scan", [f"Port {port} not found in network"], term)
    else:
        print_loading("Scanning network for ports",term)
        print_this = ["Found Ports in network: "]
        for p in ports:
            print_this.append(f"{p}/TCP [State: open]")
        print_box("Port Scan", print_this, term)


def search_back(what, walk, piervous):
    result = []
    for i in walk:
        if isinstance(i, tuple):
            if what in i[0]:
                result.append(piervous + "/" + i[0])
            result += search_back(what, i[1], piervous + "/" + i[0])
        elif what in i:
            result.append(piervous + "/" + i)
    return result
@add_function(("search", "find"), "user_input", "fs", 'rootfs', "user", 'term')
@expand_args(0, "what", 'path')
def search(what: str, path: str, fs, rootfs, user, term):
    """search [name:string] [path]
    [EXTEND]
    search - search for file with the specified name
    """
    "search [name]"

    result = []
    if path[0] == '/':
        result = search_back(what, rootfs.getDir(user, path[1:].split('/')).walk(user), '')
    else:
        path = path.split('/')
        result = search_back(what, fs.getDir(user, path).walk(user), path[-1])

    if len(result) == 0:
        raise NoSuchFileOrDirectory

    print_box("Search", result, term)


@add_function(('showp', 'showpermissions'), 'user_input', 'fs', 'term')
@expand_args(0, 'path')
def showpermisions(path: str, fs, term):
    '''showp [path:str]
    [EXTEND]
    showp - print file or directory permissions
    '''
    path = path.split('/')
    perms = fs.get(ROOT, path).perms()
    echo('up: ' + str(perms[0]) + ' op: ' + str(perms[1]) + ' uid: ' + str(perms[2]), term)


@add_function(("shutdown", ), "user_input", "term", 'user')
@expand_args(0, "user_input")
def shutdown(user_input: str, term, user):
    print(user.uid)
    if user_input == "CODEREDATOMNANO" and user.uid == 0:
        print_box("SHUTDOWN", ["PRESS ENTER TO INITIATE SHUTDOWN"], term)
        input()
        print_box("SHUTDOWN", ["SHUTDOWN CONFIRMED",
                               "UNARMING NUCLEAR WEAPONS",
                               "LAUNCHING FAIL SAFE",
                               "SHUTDOWN SUCCESSFUL..."], term)
        exit()
    else:
        print_box("SHUTDOWN", ["MISSING ROOT PRIVILAGE OR INCORRECT PASSWORD"], term)


@add_function(("tree", ), 'fs', 'user', "term")
def dir_cat(fs, user, term):
    """dir
    [EXTEND]
    dir - print directory tree
    """
    print_tree("dir", fs, user, term)

@add_function(("tutorial", "t"), "user_input", 'term')
@expand_args(0, "user_input")
def tutorial(user_input: Optional(int, None), term):
    if user_input is None or user_input == 1:
        print_box("Tutorial", [
            "Tutorial 1: Getting around the OS (1/4)",
            "---------------------",
            "help - list all commands",
            "help (command) - help on specified command",
            "tree - show the full file system",
            "cd - move into a different directory",
            "dir - show directories",
            "search (filename) - search the OS for specified items",
            "---------------------",
            'Type "t 2" for tutorial 2/4'], term)
    else:
        if user_input == 2:
            print_box("Tutorial", [
                "Tutorial 2: Files (2/4)",
                "---------------------",
                "read (filename) - read files in the current directory",
                "write (filename) (content) - add content into file",
                "touch (filename) - create a new file",
                "mkdir (name) - make a new directory in current path",
                "---------------------",
                'Type "t 3" for tutorial 3/4'], term)
        elif user_input == 3:
            print_box("Tutorial", [
                "Tutorial 3: Hacking tools (3/4)",
                "---------------------",
                "decrypt (file) (password) - make files readable",
                "morse (code) - translate morse code from 1 and 0 to English alphabets and numbers",
                "scans:",
                "pwscan - search for insecure passwords stored in logs",
                "ipsearch - search for IPs connected to the OS",
                "ipscan (IP)- scan the specifed IP for information",
                "portscan - list open ports",
                "portscan (port ID) - scan the specified port for information",
                "---------------------",
                'Type "t 4" for tutorial 4/4'], term)
        else:
            print_box("Tutorial", [
                "Tutorial 4: Advanced (4/4)",
                "---------------------",
                "logs - track actions performed on the OS",
                "rm (filename) - remove files or directories (warning: cannot be undone)",
                "cp - copy file",
                "---------------------",
                'Type "h" for help'
            ], term)


@add_function(('users', 'listusers'), 'Users', 'term')
def listusers(users, term):
    '''listusers
    [EXTEND]
    listusers - list system users
    '''
    print_box('Users', users.keys(), term)


@add_function(("cat", "read"), "user_input", "fs", "user", 'term')
@expand_args(0, "file", "bin")
def read(file: str, fs, user, term, bin: Flag(True) = False):
    """read [file:string] [mode:text]
    [EXTEND]
    read - read file using binary (bin) or text (text) modes
    """
    print_box("Read", [fs.getFile(user, file.split("/")).read(user, bin)], term)


def remove_vulnerabillity(vulnerability):
    global VULNERABILITIES
    try:
        VULNERABILITIES.remove(vulnerability)
    except ValueError:
        pass


@add_function(("rm", "remove"), "user_input", "fs", "user")
@expand_args(0, "path")
def rm(path: str, fs, user):
    """rm [path:string]
    [EXTEND]
    rm - remove file or folder with specified path
    """
    tmp = path.split("/")
    fs.get(user, "" if len(tmp) == 0 else tmp[:-1]).rm(user, tmp[-1])

@add_function(("vscan", ), 'term')
def hint(term):
    """vscan
    [EXTEND]
    vscan - scan for vulnerabilities in network
    """
    global VULNERABILITIES
    print_box("Vulnerability Scan", ["Looking for vulnerabilities..."], term)
    time.sleep(3)
    clear_term(term)
    # selects random vulnerability
    chosen_vulnerability = random.choice(VULNERABILITIES)
    # display our selected vulnerability.
    print_box("Vulnerability Scan", [f"Vulnerability found: {chosen_vulnerability}"], 'term')
    # removes vulnerability from the list.
    remove_vulnerabillity(chosen_vulnerability)
    # add 1 failure point.
    add_failure(10)
    OSlog.append("unknown user: found vulnerability,")
    OSlog.append("SECURITY AI: detecting unknown user,")


@add_function(("write", ), "user_input", "fs", "user")
@expand_args(0, "file", "content", "bin")
def write(file: str, content: str, fs, user, bin: Flag(True) = False):
    """write [file:string] [content]
    [EXTEND]
    write - overwrite file with specified content
    """
    fs.getFile(user, file.split("/")).write(user, " ".join(content), bin)
