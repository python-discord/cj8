class copy:
    def copy(self, other):
        for i in self.__init__.__code__.co_varnames[1:self.__init__.__code__.co_argcount]:
            setattr(self, i, getattr(other, i))
