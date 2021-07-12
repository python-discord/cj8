from .fs_parser import readxml
from .fs_parser import savexml


class ACL:
    def __init__(self, dicit):
        self.dicit = dicit

    def add(self, name, perm):
        self.dicit[name] = perm

    def remove(self, name):
        del self.dicit[name]

    "file handeling"
    def save(self, path):
        savexml(self.dicit, path, ("op", "up", "uid"), "acl")

    @classmethod
    def InitRead(cls, path):
        return cls(readxml(path, int))


    "diciti like"
    def __iter__(self):
        return iter(self.dicit.items())

    def __getitem__(self, key):
        return self.dicit[key]

    def __setitem__(self, key, item):
        self.dicit[key] = item

    def items(self):
        return self.dicit.items()

    def __delitem__(self, key):
        del self.dicit[key]

    # debug
    def __repr__(self):
        return str(self.dicit)

