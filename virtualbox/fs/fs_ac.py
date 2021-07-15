from virtualbox.exceptions import PermisionDenied
from virtualbox.generalclasses import copy


class AC(copy):
    def __init__(self, up, op, uid):
        self.up = up
        self.op = op

        self.uid = uid

    """properties"""

    def perms(self):
        return (self.up, self.op, self.uid)

    """permisons check"""
    def p_check(self, perm, user):
        if self.uid == user.uid and self.up & perm == perm:
            return True
        if self.op & perm == perm:
            return True
        return False

    """wraper permisons check"""
    def owncheck(function):
        def check(self, user, *args):
            if user.id == self.uid or user.uid == 0:
                return function(self, user, *args)
            raise PermisionDenied()
        return check

    def execcheck(function):
        def check(self, user, *args):
            if self.p_check(1, user) or user.uid == 0:
                return function(self, user, *args)
            raise PermisionDenied()
        return check

    def writecheck(function):
        def check(self, user, *args):
            if self.p_check(2, user) or user.uid == 0:
                return function(self, user, *args)
            raise PermisionDenied()
        return check

    def readcheck(function):
        def check(self, user, *args):
            if self.p_check(4, user) or user.uid == 0:
                return function(self, user, *args)
            return PermisionDenied()
        return check

    # permisions managment

    @owncheck
    def chown(self, user, chuser):
        self.uid = chuser.uid

    @owncheck
    def chmod(self, user, up, op):
        if self.up is not None:
            self.up = up
        if self.op is not None:
            self.op = op

    @owncheck
    def chadd(self, user, up, op):
        if self.up is not None:
            self.up |= up
        if self.op is not None:
            self.op |= op
