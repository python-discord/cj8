from virtualbox.exceptions import PermisionDenied
from virtualbox.generalclasses import copy


class AC(copy):
    def __init__(self, up, op, uid):
        self.up = up
        self.op = op

        self.uid = uid

    """properties"""
    @property
    def perm(self):
        return (self.up, self.op, self.uid)

    """permisons check"""
    def p_check(self, perm, user):
        if self.uid == user.uid and self.up & perm == perm:
            return True
        if self.op & perm == perm:
            return True
        return False

    """wraper permisons check"""
    @staticmethod
    def owncheck(function):
        def check(self, user, *args):
            if user.id == self.uid or user.uid == 0:
                return function(self, user, *args)
            raise PermisionDenied()
        return check

    @staticmethod
    def execcheck(function):
        def check(self, user, *args):
            if self.p_check(1, user) or user.uid == 0:
                return function(self, user, *args)
            raise PermisionDenied()
        return check

    @staticmethod
    def writecheck(function):
        def check(self, user, *args):
            if self.p_check(2, user) or user.uid == 0:
                return function(self, user, *args)
            raise PermisionDenied()
        return check

    @staticmethod
    def readcheck(function):
        def check(self, user, *args):
            if self.p_check(4, user) or user.uid == 0:
                return function(self, user, *args)
            return PermisionDenied()
        return check
