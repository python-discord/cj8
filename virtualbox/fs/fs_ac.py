from typing import Any, Callable, Tuple

from virtualbox.exceptions import PermisionDenied
from virtualbox.generalclasses import copy
from virtualbox.users.user import User


class AC(copy):
    """Acces control class

    it is father class for directories and files
    """

    def __init__(self, up: int, op: int, uid: int):
        self.up = up
        self.op = op

        self.uid = uid

    # properties

    def perms(self) -> Tuple[int, int, int]:
        """Returns tuple of permisonss. used in ACL class"""
        return (self.up, self.op, self.uid)

    # permisons check
    def p_check(self, perm: int, user: User) -> bool:
        """Checks if user have permission"""
        if self.uid == user.uid and self.up & perm == perm:
            return True
        if self.op & perm == perm:
            return True
        return False

    """wraper permisons check"""
    def owncheck(function: Callable[['AC', User, ...], Any]) -> Callable[['AC', User, ...], Any]:
        """Wrapper that check if user is owner if not it runs inside function if not then raises PermissioDenied"""
        def check(self: 'AC', user: User, *args: Any) -> Any:
            if user.id == self.uid or user.uid == 0:
                return function(self, user, *args)
            raise PermisionDenied()
        return check

    def execcheck(function: Callable[['AC', User, ...], Any]) -> Callable[['AC', User, ...], Any]:
        """Wrapper that check if user is owner if not it runs inside function if not then raises PermissioDenied"""
        def check(self: 'AC', user: User, *args: Any) -> Any:
            if self.p_check(1, user) or user.uid == 0:
                return function(self, user, *args)
            raise PermisionDenied()
        return check

    def writecheck(function: Callable[['AC', User, ...], Any]) -> Callable[['AC', User, ...], Any]:
        """Wrapper that check if user is owner if not it runs inside function if not then raises PermissioDenied"""
        def check(self: 'AC', user: User, *args: Any) -> Any:
            if self.p_check(2, user) or user.uid == 0:
                return function(self, user, *args)
            raise PermisionDenied()
        return check

    def readcheck(function: Callable[['AC', User, ...], Any]) -> Callable[['AC', User, ...], Any]:
        """Wrapper that check if user is owner if not it runs inside function if not then raises PermissioDenied"""
        def check(self: 'AC', user: User, *args: Any) -> Any:
            if self.p_check(4, user) or user.uid == 0:
                return function(self, user, *args)
            return PermisionDenied()
        return check

    # permisions managment

    @owncheck
    def chown(self, user: User, chuser: User) -> None:
        """Changes owner"""
        self.uid = chuser.uid

    @owncheck
    def chmod(self, user: User, up: int, op: int) -> None:
        """Changes permissions"""
        self.up = up
        self.op = op

    @owncheck
    def chadd(self, user: User, up: int, op: int) -> None:
        """Executes or on permissions"""
        self.up |= up
        self.op |= op
