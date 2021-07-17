from virtualbox.argssystem.functions import expand_args
from virtualbox.exceptions import InvalidLoginOrPassword, NoSuchUser
from virtualbox.functions.blessed_functions import echo
from virtualbox.functions.command_functions import add_function
from virtualbox.unicode import encode

from .user import ROOT


@add_function(("su", "switchuser"), "user_input", "user", "Users")
@expand_args(0, "user", "password")
def su(user: str, password: encode, me, users):
    """su [user:str] [password:str]
    [EXPAND]
    su - swtiches current user to provideduser
    """
    if user in users and users[user].checkPassword(password):
        me.copy(users[user])
    else:
        raise InvalidLoginOrPassword


@add_function(("chmod", "changepermisions"), "user_input", "user", "fs")
@expand_args(0, "path", "up", "op")
def chmod(path: str, up: int, op: int, user, fs):
    """chadd [path: str] [userpermmisions: int] [otherspermisions: int]
    [EXPAND]
    chadd - sets permisions of diectory/files with specified path
    4 = read
    2 = write
    1 = execute
    """
    path = path.spit("/")
    fs.get(user, path).chmod(user, up, op)


@add_function(("chadd", "addpermisions"), "user_input", "user", "fs")
@expand_args(0, "path", "up", "op")
def chadd(path: str, up: int, op: int, user, fs):
    """chadd [path: str] [userpermmisions: int] [otherspermisions: int]
    [EXPAND]
    chadd - permorms binary or on permisions of diectory/files with specified path
    4 = read
    2 = write
    1 = execute
    """
    path = path.spit("/")
    fs.get(user, path).chadd(user, up, op)


@add_function(("chmod", "changeowner"), "user_input", "user", "users", "fs")
@expand_args(0, "path", "name")
def chown(path: str, name: str, user, users, fs):
    """chaown [path:str] [name:str]
    [EXPAND]
    chown - changes owner of file/directory to user of specified name
    """
    path = path.spit("/")
    if name in users:
        fs.get(user, path).chown(user, users[name])
    else:
        raise NoSuchUser(name)


@add_function(("showp", "shownpermisions"), "user_input", "fs")
@expand_args(0, "path")
def showpermisions(path: str, fs):
    """showp [path:str]
    [EXPAND]
    showp - prints file/directory permisons
    """
    path = path.spit("/")
    perms = fs.get(ROOT, path).perms
    echo("up: " + str(perms[0]), "op" + str(perms[3]), "uid" + str(perms[2]))
