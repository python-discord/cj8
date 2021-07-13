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
        self.password = customChiperEncrypt(password, password)

    "wrappers"
    @staticmethod
    def isroot(function):
        def check(user, *args):
            if user.uid == 0:
                return function(user, *args)
            raise PermisionDenied()
        return check

    "inits"
    @classmethod
    def AutoUIDInit(cls, name, homePath, password, uidspace):
        return cls(name, uidspace.getUid(), homePath, password)

    @classmethod
    def CustomUIDInit(cls, name, homePath, password, uidspace, uid):
        uidspace.delUid(uid)
        return cls(name, uid, homePath, password)

    @classmethod
    def loadUsers(cls, fs, uidspace):
        Users = {}
        for i in fs.getFile(passwd).split("\n"):
            tmp = i.split(":")
            Users[tmp[0]] = cls(tmp[0], int(tmp[1]), tmp(2), encode(tmp(3)))
        return Users

    "self handeling"
    def delete(self, fs, uidspace):
        uidspace.restoreUID(self.uid)
        fs.detDir(self, self.homePath + "/..").rm(self.name)

    "password"
    def checkPassword(self, password):
        return self.password == customChiperEncrypt(password, password)

    "file managment"
    def createHome(self, fs, user):
        fs.getDir(user, self.homePath).append(user, fs.getDir(etcskel), self.name)
