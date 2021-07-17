import copy
import os
import shutil
from typing import Any, Callable, Union

from virtualbox.config import sep
from virtualbox.exceptions import (
    CannotChangePermisionsForFather, FileOrDirectoryAlreadyExist,
    NoSuchFileOrDirectory, NotAnDirectory, NotAnFile, PermisionDenied
)
from virtualbox.users.user import User

from .fs_ac import AC
from .fs_acl import ACL
from .fs_file import File


class Dir(AC):
    """Directory class stores other directories and files in sub dicit and its acceses in acl dicit"""

    def __init__(self, up: int, op: int, uid: int, sub: dict, path: str, acl: ACL):
        super().__init__(up, op, uid)
        self.sub = sub
        self.path = path
        self.acl = acl

    @classmethod
    def FromPath(cls, path: str, father: Union['Dir', None], up: int, op: int, uid: int) -> 'Dir':
        """Creates directory from path"""
        acl = ACL.InitRead(path + sep + "acl.xml")
        self = Dir(up, op, uid, {} if father is None else {"..": father}, path, acl)
        for name, perm in acl:
            if os.path.isdir(path + sep + name):
                self.sub[name] = Dir.FromPath(path + sep + name, self, *perm)
            else:
                self.sub[name] = File(path + sep + name, *perm)

        return self

    @classmethod
    def MkDirInit(cls, up: int, op: int, user: User, path: str, father: 'Dir'):
        """Mkdir inicialization used to create class and directory on Host FS"""
        self = cls(up, op, user.uid, {"..": father}, path, ACL({}))
        self.create()

        return self

    # wrapper checks
    def alreadyexist(function: Callable[['Dir', User, str, ...], Any]) -> Callable[['Dir', User, str, ...], Any]:
        """Wrapper that file or directory is subdirectory of instance.

        if it is the case raises FileOrDirectoryAlreadyExist
        """
        def check(self: 'Dir', user: User, name: str, *args: Any) -> Any:
            if name in self.sub:
                raise FileOrDirectoryAlreadyExist()
            return function(self, user, name, *args)
        return check

    def doesnotexist(function: Callable[['Dir', User, str, ...], Any]) -> Callable[['Dir', User, str, ...], Any]:
        """Wrapper that file or directory is subdirectory of instance.

        if it is the case raises NoSuchFileOrDirectory
        """
        def check(self: 'Dir', user: User, name: str, *args: Any) -> Any:
            if name not in self.sub:
                raise NoSuchFileOrDirectory()
            return function(self, user, name, *args)
        return check

    # auto update acl
    def update(function: Callable[['Dir', ...], Any]) -> Any:
        """Wrapper that pdates acl"""
        def check(self: 'Dir', *args) -> Any:
            tmp = function(self, *args)
            self.aclsave()
            return tmp
        return check

    "file managment"
    @AC.writecheck
    @alreadyexist
    @update
    def mkdir(self, user: str, name: str) -> True:
        """Creates directory of given name as subdir of instance"""
        self.sub[name] = Dir.MkDirInit(self.up, self.op, user, self.path + sep + name, self)
        self.acl.add(name, (self.up, self.op, user.uid))

        return True

    @AC.writecheck
    @alreadyexist
    @update
    def touch(self, user: str, name: str) -> True:
        """Creates file of given name as subfile of instance"""
        self.sub[name] = File.TouchInit(self.up, self.op, user.uid, self.path + sep + name)
        self.acl.add(name, (self.up, self.op, user.uid))
        return True

    @AC.writecheck
    @doesnotexist
    @update
    def rm(self, user: str, name: str) -> None:
        """Removes directory or file of given name from subdirs/subfiles of instance"""
        self.sub[name].delete()
        del self.sub[name]
        if name in self.acl:
            self.acl.remove(name)

    @AC.writecheck
    @alreadyexist
    @update
    def append(self, user: User, object: Union['Dir', File], name: str) -> None:
        """Appends file or directory as subdir/subfile"""
        self.sub[name] = object
        self.acl.add(name, object.perms)

    def mv(self, user: User, name: str, to: str) -> None:
        """Moves instance to given path"""
        father = self.get(user, name[:-1])
        dest = self.getDir(user, to[:-1])

        if name[-1] in dest.acl:
            raise FileOrDirectoryAlreadyExist()

        dest.set(user, to[-1], father.pop(user, name[-1]))
        dest.sub[to[-1]].mvSelf(user, self.path + sep + sep.join(to))

    def cp(self, user: User, path: str, to: str) -> None:
        """Copies instance to given path"""
        dest = self.getDir(user, to[:-1])
        dest.append(user, self.get(user, path).cpSelf(user, self.path + sep + sep.join(to)), to[-1])

    @AC.readcheck
    def ls(self, user: User) -> dict:
        """Listes subdirs/subfiles of instance"""
        return self.sub

    @AC.readcheck
    def stringList(self, user: User) -> list:
        """Listes names of subdir/subfiles of instance"""
        return list(self.sub.keys())

    @AC.readcheck
    def walk(self, user: User) -> list:
        """Listes names of subdirs/subfiles and subsubfiles/subsubdirs etc"""
        try:
            Result = []
            for key, item in self.sub.items():
                if key != "..":
                    Result.append(key if isinstance(item, File) else (key, item.walk(user)))

            return Result
        except PermisionDenied:
            return []

    # change permisons

    @AC.owncheck
    @doesnotexist
    @update
    def chown(self, user: User, name: str, chuser: User) -> None:
        """Changes owner"""
        if name == '..':
            raise CannotChangePermisionsForFather()
        obj = self.sub[name]
        obj.uid = chuser.uid

        self.acl.add(name, obj.perms)

    @AC.owncheck
    @doesnotexist
    @update
    def chmod(self, user: User, name: str, up: int, op: int) -> None:
        """Changes permissions"""
        if name == '..':
            raise CannotChangePermisionsForFather()
        obj = self.sub[name]
        obj.up = up
        obj.op = op

        self.acl.add(name, obj.perms)

    @AC.owncheck
    @doesnotexist
    @update
    def chadd(self, user: User, name: str, up: int, op: int) -> None:
        """Executes or on permissions"""
        if name == '..':
            raise CannotChangePermisionsForFather()
        obj = self.sub[name]
        obj.up |= up
        obj.op |= op

        self.acl.add(name, obj.perms)

    # change directory
    @doesnotexist
    @AC.readcheck
    def shallowget(self, user: User, name: str) -> Union['Dir', 'File']:
        """Returns subdir/subfile of given name

        will raise PerrmisonDenied if user does not have sufficent perrmisions
        or NoSuchFileOrDirectory if subfile/subdirectory does not exist
        """
        return self.sub[name]

    def get(self, user: User, path: str) -> Union['Dir', 'File']:
        """Gets subfile or subdirectory"""
        result = self
        for i in path:
            if len(i) == 0:
                continue
            result = result.shallowget(user, i)
        return result

    def getType(self, user: User, path: str, Type: type, exception: Exception) -> Any:
        """Gets subobject of provided type"""
        result = self
        for i in path:
            if len(i) == 0:
                continue
            result = result.shallowget(user, i)
        if type(result) != Type:
            raise exception()

        return result

    def getDir(self, user: User, path: str) -> 'Dir':
        """Gets directory"""
        return self.getType(user, path, Dir, NotAnDirectory)

    def getFile(self, user: User, path: str) -> File:
        """Gets file"""
        return self.getType(user, path, File, NotAnFile)

    # self managment
    def delete(self) -> None:
        """Deletes dir form host fs"""
        shutil.rmtree(self.path)

    def create(self) -> None:
        """Creates dir on host fs"""
        os.mkdir(self.path)
        self.aclsave()

    @AC.execcheck
    def mvSelf(self, user: User, to: str) -> None:
        """Moves self to other path"""
        shutil.move(self.path, to)
        self.path = to

    @AC.execcheck
    def cpSelf(self, user: User, to: str) -> 'Dir':
        """Copies self to other path"""
        shutil.copy(self.path, to)
        result = copy.copy(self)
        result.path = to
        return result

    # properties"
    @property
    def aclpath(self) -> str:
        """Returns Acces control list paht"""
        return self.path + sep + "acl.xml"

    # save acl"
    def aclsave(self) -> None:
        """Saves acces control list"""
        self.acl.save(self.aclpath)

    # dicit like
    @AC.readcheck
    def getDicit(self, user: User, key: str) -> tuple:
        """Returns tuple of sub and acl results"""
        if key in self.acl.dicit:
            return self.sub[key], self.acl[key]
        raise NoSuchFileOrDirectory()

    @AC.writecheck
    @update
    def set(self, user: User, key: str, value: tuple) -> None:
        """Sets sub and acl"""
        self.sub[key] = value[0]
        self.acl[key] = value[1]

    @AC.writecheck
    @update
    def pop(self, user: User, key: str) -> None:
        """Hymmmmm i wonder what pop does?"""
        tmp = self.getDicit(user, key)

        del self.sub[key]
        del self.acl[key]

        return tmp
