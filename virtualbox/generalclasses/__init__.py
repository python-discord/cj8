class copy:
    """Just soteis copy method"""

    def copy(self, other: 'copy') -> None:
        """Copies other to self(other is 2nd name obvously)"""
        for i in self.__init__.__code__.co_varnames[1:self.__init__.__code__.co_argcount]:
            setattr(self, i, getattr(other, i))
