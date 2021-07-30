from fs.fs_acl import ACL
from fs.fs_ac import AC
from fs.fs_file import File
from fs.fs_config import sep
from fs.fs_exceptions import NoSuchFileOrDirectory
from fs.fs_exceptions import FileOrDirectoryAlreadyExist
from fs.fs_exceptions import NotAnDirectory
from fs.fs_exceptions import NotAnFile
import os
import shutil


class Dir(AC):
    def __init__(self, up, op, uid, sub, path, acl):
        super().__init__(up, op, uid)
        self.sub = sub
        self.path = path
        self.acl = acl

    @classmethod
    def FromPath(cls, path, father, up, op, uid):
        acl = ACL.InitRead(path + sep + "acl.xml")
        self = Dir(up, op, uid, {} if father is None else {"..": father}, path, acl)

        for name, perm in acl:
            if os.path.isdir(path + sep + name):
                self.sub[name] = Dir.FromPath(path + sep + name, self, *perm)
            else:
                self.sub[name] = File(path + sep + name, *perm)

        return self

    @classmethod
    def MkDirInit(cls, up, op, user, path, father):
        self = cls(up, op, user.uid, {"..": father}, path, ACL({}))
        self.create()

        return self
    "wrapper checks"
    def alreadyexist(function):
        def check(self, user, name, *args):
            if name in self.sub:
                raise FileOrDirectoryAlreadyExist()
            return function(self, user, name, *args)
        return check

    def doesnotexist(function):
        def check(self, user, name, *args):
            if name not in self.sub:
                raise NoSuchFileOrDirectory()
            return function(self, user, name, *args)
        return check

    "auto update acl"
    def update(function):
        def check(self, *args):
            tmp = function(self, *args)
            self.aclsave()
            return tmp
        return check

    "file managment"
    @AC.writecheck
    @alreadyexist
    @update
    def mkdir(self, user, name):
        self.sub[name] = Dir.MkDirInit(self.up, self.op, user, self.path + sep + name, self)
        self.acl.add(name, (self.up, self.op, user.uid))

        return True

    @AC.writecheck
    @alreadyexist
    @update
    def touch(self, user, name):
        self.sub[name] = File.TouchInit(self.up, self.op, user.uid, self.path + sep + name)
        self.acl.add(name, (self.up, self.op, user.uid))
        return True

    @AC.writecheck
    @doesnotexist
    @update
    def rm(self, user, name):
        self.sub[name].delete()
        del self.sub[name]
        if name in self.acl:
            self.acl.remove(name)

    @AC.readcheck
    def ls(self, user):
        return self.sub

    "change directory"
    @doesnotexist
    @AC.readcheck
    def shallowget(self, user, name):
        return self.sub[name]

    def get(self, user, path):
        result = self
        for i in path.split("/"):
            result = result.shallowget(user, i)
        return result

    def getType(self, user, path, Type, exception):
        result = self
        for i in path.split("/"):
            result = result.shallowget(user, i)
            if type(result) != Type:
                raise exception()
        return result

    def getDir(self, user, path):
        return self.getType(user, path, Dir, NotAnDirectory)

    def getFile(self, user, path):
        return self.getType(user, path, File, NotAnFile)

    "permisions managment"
    @AC.owncheck
    @update
    def chown(self, user, name, chuser=None, chgroup=None):
        if chuser is not None:
            self.uid = chuser.id
        if chgroup is not None:
            self.gid = chgroup.id

    @AC.owncheck
    @update
    def chmod(self, user, up, op):
        if self.up is not None:
            self.up = up
        if self.op is not None:
            self.op = op

    @AC.owncheck
    @update
    def chadd(self, user, up, op):
        if self.up is not None:
            self.up |= up
        if self.op is not None:
            self.op |= op

    "self managment"
    def delete(self):
        shutil.rmtree(self.path)

    def create(self):
        os.mkdir(self.path)
        self.aclsave()
        return self

    "properties"
    @property
    def aclpath(self):
        return self.path + sep + "acl.xml"

    "save acl"
    def aclsave(self):
        self.acl.save(self.aclpath)
