from virtualbox.exceptions import PermisionDenied
from virtualbox.config import etcskel
from virtualbox.config import passwd
from virtualbox.cryptology import customChiperEncrypt
from virtualbox.unicode import encode


class User:
    def __init__(self, name, uid, homePath, password):
        self.name = name
        self.uid = uid
        self.homePath = homePath
        self.password = password

    # wrappers
    @staticmethod
    def isroot(function):
        def check(user, *args):
            if user.uid == 0:
                return function(user, *args)
            raise PermisionDenied()
        return check

    def passwordcheck(func):
        def check(self, password, *args, **kwargs):
            if self.checkPassword(password):
                raise PermisionDenied
            return func(self, password, *args, **kwargs)
        return check

    # inits
    @classmethod
    def AutoUIDInit(cls, name, homePath, passwordhash, uidspace):
        return cls(name, uidspace.getUid(), homePath, passwordhash)

    @classmethod
    def CustomUIDInit(cls, name, homePath, passwordhash, uidspace, uid):
        uidspace.delUid(uid)
        return cls(name, uid, homePath, passwordhash)

    @classmethod
    def loadUsers(cls, ROOT, fs, uidspace):
        Users = {}
        for i in fs.getFile(ROOT, passwd).read(ROOT).strip().split("\n"):
            tmp = i.split(":")
            Users[tmp[0]] = cls(tmp[0], int(tmp[1]), tmp[2], encode("".join(tmp[3:])))
        return Users

    # self handeling
    def delete(self, fs, uidspace):
        uidspace.restoreUID(self.uid)
        fs.detDir(self, self.homePath + "/..").rm(self.name)

    @passwordcheck
    def get(self, password):
        return self

    # password
    def checkPassword(self, password):
        return self.password == customChiperEncrypt(encode(password), encode(password))

    # file managment
    def createHome(self, fs, user):
        fs.getDir(user, self.homePath).append(user, fs.getDir(etcskel), self.name)


ROOT = User("root", 0, "/root", encode(""))
