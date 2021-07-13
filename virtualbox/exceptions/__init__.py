class NoSuchFileOrDirectory(Exception):
    def __init__(self):
        super().__init__("no such file or directory")


class FileOrDirectoryAlreadyExist(Exception):
    def __init__(self):
        super().__init__("file or directory already exist")


class NotAnDirectory(Exception):
    def __init__(self):
        super().__init__("not an directory")


class NotAnFile(Exception):
    def __init__(self):
        super().__init__("not an file")


class NotAnIntiger(Exception):
    def __init__(self):
        super().__init__("not an intiger")


class PermisionDenied(Exception):
    def __init__(self):
        super().__init__("permision denied")


class NoSuchIndex(Exception):
    def __init__(self):
        super().__init__("no such index")


class UIDAlreadyExist(Exception):
    def __init__(self):
        super().__init__("uid already exist")


class CannotFullFillFunction(Exception):
    def __init__(self):
        super().__init__("function argument request cannot be fullfiled!")


class CannotReadFileInTextMode(Exception):
    def __init__(self):
        super().__init__("file content cannot be red in text mode. try binary mode insted")


class CommandNotFound(Exception):
    def __init__(self):
        super().__init__("command not found!")


class WrongAmmountOfArguments(Exception):
    def __init__(self, reqLen, Len):
        super().__init__("minimum required argument count is {} supplied count is {}".format(reqLen, Len))


class NoSuchFlagOrOption(Exception):
    def __init__(self, flag):
        super().__init__("no such flag or option {}".format(flag))


class ConversionError(Exception):
    def __init__(self, type, what):
        super().__init__("{} cannot be converted to {} type".format(what, type))


class ConversionErrorMulti(Exception):
    def __init__(self, types, what):
        super().__init__("{} cannot be converted to any of those {} types".format(what, types))


class WrongKeywordUsage(Exception):
    def __init__(self, name):
        super().__init__("bad keyword syntax! peroper keyword syntax is {}:value".format(name))
