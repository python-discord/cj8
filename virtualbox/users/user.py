from typing import Any, Callable

from virtualbox.config import etcskel, passwd
from virtualbox.cryptology import customChiperEncrypt
from virtualbox.exceptions import PermisionDenied
from virtualbox.unicode import encode

from .uid import Uidspace


class User:
    """User class"""

    def __init__(self, name: str, uid: int, homePath: str, password: bytes):
        self.name = name
        self.uid = uid
        self.homePath = homePath
        self.password = password

    # wrappers
    @staticmethod
    def isroot(function: Callable[['User', ...], Any]) -> Any:
        """Wraper that check is user is root if it is runs function"""
        def check(user: 'User', *args: Any) -> Any:
            if user.uid == 0:
                return function(user, *args)
            raise PermisionDenied()
        return check

    def passwordcheck(func: Callable[['User', str], Any]) -> Any:
        """Wraper that check password if it is corects runs function"""
        def check(self: 'User', password: str, *args: Any, **kwargs: Any) -> Any:
            if self.checkPassword(password):
                raise PermisionDenied
            return func(self, password, *args, **kwargs)
        return check

    # inits
    @classmethod
    def AutoUIDInit(cls, name: str, homePath: str, passwordhash: bytes, uidspace: Uidspace) -> 'User':
        """Creates user with defautlt generated uid"""
        return cls(name, uidspace.getUid(), homePath, passwordhash)

    @classmethod
    def CustomUIDInit(cls, name: str, homePath: str, passwordhash: bytes, uidspace: Uidspace, uid: int) -> 'User':
        """Creates user with custom uid"""
        uidspace.delUid(uid)
        return cls(name, uid, homePath, passwordhash)

    @classmethod
    def loadUsers(cls, ROOT: 'User', fs: 'dir', uidspace: Uidspace) -> dict:
        """Loads users from passwd"""
        Users = {}
        for i in fs.getFile(ROOT, passwd).read(ROOT).strip().split("\n"):
            tmp = i.split(":")
            password = b''

            for i in map(lambda x: int(x).to_bytes(1, 'little'), tmp[3:]):
                password += i

            Users[tmp[0]] = cls(tmp[0], int(tmp[1]), tmp[2], password)
        return Users

    # self handeling
    def delete(self, fs: 'dir', uidspace: Uidspace) -> None:
        """Deletes self"""
        uidspace.restoreUID(self.uid)
        fs.detDir(self, self.homePath + "/..").rm(self.name)

    def copy(self, other: 'User') -> None:
        """Copies ohter to self"""
        self.name = other.name
        self.homePath = other.homePath
        self.uid = other.uid
        self.password = other.password

    @passwordcheck
    def get(self, password: str) -> 'User':
        """Retuns self if password is correct"""
        return self

    # password
    def checkPassword(self, password: str) -> bool:
        """Check if passwords is corectss"""
        return self.password == customChiperEncrypt(encode(password), encode(password))

    # file managment
    def createHome(self, fs: 'dir', user: 'User') -> None:
        """Creates home"""
        fs.getDir(user, self.homePath).append(user, fs.getDir(etcskel), self.name)


ROOT = User("root", 0, "/root", b'\x14\x02\xfe9\xd6\xdd\x03\x020n\x1a5}\x92')

