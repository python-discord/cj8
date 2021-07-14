from virtualbox.exceptions import ConversionError, ConversionErrorMulti


class MultiType:
    def __init__(self, *types):
        self.types = types

    def __call__(self, var):
        for i in self.types:
            try:
                return i(var)
            except TypeError:
                pass
        raise ConversionErrorMulti(var, self.types)


class Optional:
    def __init__(self, type, default):
        self.type = type
        self.default = default

    def __call__(self, var):
        if var is None:
            return self.default
        try:
            return self.type(var)
        except TypeError:
            raise ConversionError(self.type, var)


class Flag:
    def __init__(self, value):
        self.value = value


class Keyword(Flag):
    def __init__(self, type):
        self.type = type

    def __call__(self, var):
        try:
            return self.type(var)
        except TypeError:
            raise ConversionError(self.type, var)
