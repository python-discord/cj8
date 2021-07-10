from ACL import ACL
from AC import AC
from File import File
from config import sep
import os


class Dir(AC):
    def __init__(self, up, op, uid, sub, path, acl):
        super().__init__(up, op, uid)
        self.sub = sub
        self.path = path
        self.acl = acl

    @classmethod
    def FromPath(cls, path, up, op, uid):
        acl = ACL.InitRead(path + sep + "acl.xml")
        sub = {}
        for name, perm in acl:
            if os.path.isdir(path + sep + name):
                sub[name] = Dir.FromPath(path + sep + name, *perm)
            else:
                sub[name] = File(path + sep + name, *perm)

        return Dir(up, op, uid, sub, path, acl)
    "wrapper checks"
    def alreadyexist(function):
        def check(self, user, name, *args):
            if name in self.sub:
                return False
            return function(self, user, name, *args)
        return check

    def doesnotexist(function):
        def check(self, user, name, *args):
            if name not in self.sub:
                return False
            return function(self, user, name, *args)
        return check

    """file managment"""
    @AC.writecheck
    @alreadyexist
    def mkdir(self, user, name):
        self.sub = Dir(self.up, self.op, {}, self.Path + name, {})
        self.acl.add(name, self.up, self.op, user.uid, user.gid)
        return True

    @AC.writecheck
    @alreadyexist
    def touch(self, user, name):
        self.sub = File(self.up, self.op, user.uid, self.Path + name)
        self.acl.add(name, self.up, self.op, user.uid)
        return True

    @AC.writecheck
    @doesnotexist
    def rm(self, user, name):
        self.sub[name].Delete()
        del self.sub[name]
        self.acl.remove(name)

    @AC.readcheck
    def ls(self, user):
        return self.sub

    "permisions managment"
    @AC.owncheck
    def chown(self, user, name, chuser=None, chgroup=None):
        if chuser is not None:
            self.uid = chuser.id
        if chgroup is not None:
            self.gid = chgroup.id

        self.aclsave()

    @AC.owncheck
    def chmod(self, user, up, op):
        if self.up is not None:
            self.up = up
        if self.op is not None:
            self.op = op

        self.aclsave()

    @AC.owncheck
    def chadd(self, user, up, op):
        if self.up is not None:
            self.up |= up
        if self.op is not None:
            self.op |= op

        self.aclsave()

    "self managment"
    def delete(self):
        os.rmdir(self.path)

    def create(self):
        os.mkdir(self.path)
        self.aclsave()

    "properties"
    @property
    def aclpath(self):
        return self.path + sep + "acl.xml"

    "save acl"
    def aclsave(self):
        self.acl.save(self.aclpath)
