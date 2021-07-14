from .blessed_functions import print_box, print_tree, clear_term, print_loading
from .generalfunctions import inAny
from virtualbox.exceptions import NoSuchFileOrDirectory
from exceptions import CommandNotFound
import time
from blessed import Terminal
import random
import os
import string
term = Terminal()

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

    try:
        to_print = user_commands[user_input[1]].__doc__.split("[EXTEND]")
    except KeyError:
        raise CommandNotFound()

    print_box("help", [f"{to_print[0].strip()}"])
    if len(user_input) > 2 and user_input[2] == "yes":
       print_box("help", [f"{to_print[1].strip()}"])


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
    else:
        # 5-7 to show user a portscanner experience and show hint/ no hint
        print_loading("Scanning Ports")
        print_this = ["Found Ports in Network: "]
        for i in range(random.randint(5, 7)):
            print_this.append(ports[i] + "/TCP [State: open]")
        print_box("PortScanner", print_this)
        time.sleep(1)
        inp = input("Select a port to scan: ")
        with term.cbreak():
            if inp in ports:
                output = random.choice(outputs)
                print_loading(f"Scanning Port {inp}")
                term.clear
                print_box("PortScanner", [f"Port {inp} attackable. ", "Attack launchend. ", f"Output: {output}"])
            else:
                print_box("PortScanner", ["The Port you entered wasnt found in the Network!"])



def dev_reset():
    script_dir = os.path.dirname(__file__)
    script_dir = script_dir.replace('functions/', '')
    file_txt = str(script_dir + 'first_game.txt')
    with open('first_game.txt', 'w') as firstgamefile:
        firstgamefile.truncate()
        firstgamefile.write('0')

VULNERABILITIES = ["clue1","clue2"]


def add_vulnerabillity(vulnerability):
    global VULNERABILITIES
    VULNERABILITIES.append(vulnerability)


def remove_vulnerabillity(vulnerability):
    global VULNERABILITIES
    try:
        VULNERABILITIES.remove(vulnerability)
    except ValueError:
        pass


# @add_function(("morse", ), "user_input")
# @expand_args(0, "code")
def morsescan(user_input, fs, user):
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
        ori_msg.append(user_input[1])
        new_msg = user_input[1].split("*")

        for j in range(0, len(new_msg)):
            if new_msg[j] in morse_dict.keys():
                dec_msg.append(morse_dict[new_msg[j]])

        print_box("morsescan",["Decoded Message is: " + ''.join(dec_msg)])  # end the infinite while loop
        break


def hint(user_input, fs, user):
    """vscan
    vscan - scans for vulnerabilities in network
    [EXTEND]
    """
    global VULNERABILITIES
    print_box("vscan",["Looking for vulnerabilities..."])
    #selects random vulnerability
    chosen_vulnerability = random.choice(VULNERABILITIES)
    #display our selected vulnerability.
    print_box("vscan",[f"Vulnerability found: {chosen_vulnerability}"])
    #removes vulnerability from the list.
    remove_vulnerabillity(chosen_vulnerability)
    #add 1 failure point.
    add_failure()


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


def gethint():
    hints = ['hello hello hello'] # Words split by a space, words cant be longer than 8 letters, wouldnt recommend longer hint than 4-5 words. Best is 3 words
    return random.choice(hints)


def ipsearch(user_input, fs, user):
    hint = gethint()
    hintlist = hint.split()
    hintlist = ipcypher(hintlist)
    for item in hintlist:
        random_int = random.randint(1,2)
        for i in range(random_int):
            randip = str(f"{random.randint(100,99999)}.{random.randint(1000,9999)}.{random.randint(100,9999)}.{random.randint(1,999)}")
            print_box('Found IP', ['Scanning:', randip, 'Not Attackable'])
            time.sleep(0.5)
        print_box('Found IP', ['Scanning:', item, 'Attackable'])
        time.sleep(0.5)
        if random_int == 1:
            randip = str(f"{random.randint(100,99999)}.{random.randint(1000,9999)}.{random.randint(100,9999)}.{random.randint(1,999)}")
            print_box('Found IP', ['Scanning:', randip, 'Not Attackable'])
            time.sleep(0.5)
    time.sleep(0.5)
    randip = str(f"{random.randint(100,99999)}.{random.randint(1000,9999)}.{random.randint(100,9999)}.{random.randint(1,999)}")
    print_box('Found IP', ['Scanning:', randip, 'Not Attackable'])
    time.sleep(1)
    clear_term()
    printlist = []
    for item in hintlist:
        printlist.append(item)
    printlist.append('You can scan these IPs by using "ipscan [ip]!"')
    print_box('Ips found:', printlist)


def ipscan(user_input, fs, user):
    retstring = ''
    list_letters = list(string.ascii_letters)
    ip = user_input[1] # Change to 0?
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
                 "cd": cd,
                 "devresetintro": dev_reset,
                 "vscan" : hint,
                 "morse": morsescan,
                 "ipscan": ipscan,
                 "ipsearch": ipsearch
                 }
