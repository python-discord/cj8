class NoSuchFileOrDirectory(Exception):
    def __init__(self):
        super().__init__("no such file or directory")


class FileOrDirectoryAlreadyExist(Exception):
    def __init__(self):
        super().__init__("file or directory already exists")


class NotAnDirectory(Exception):
    def __init__(self):
        super().__init__("not a directory")


class NotAnFile(Exception):
    def __init__(self):
        super().__init__("not a file")


class NotAnIntiger(Exception):
    def __init__(self):
        super().__init__("not an integer")


class PermisionDenied(Exception):
    def __init__(self):
        super().__init__("permission denied")


class NoSuchIndex(Exception):
    def __init__(self):
        super().__init__("no such index")


class UIDAlreadyExist(Exception):
    def __init__(self):
        super().__init__("uid already exists")


class CannotFullFillFunction(Exception):
    def __init__(self):
        super().__init__("function argument request cannot be fullfiled")


class CannotReadFileInTextMode(Exception):
    def __init__(self):
        super().__init__("file content cannot be read in text mode. try binary mode instead")


class CommandNotFound(Exception):
    def __init__(self):
        super().__init__("command not found")


class WrongAmmountOfArguments(Exception):
    def __init__(self, reqLen, Len):
        super().__init__("minimum required argument count is {}. supplied count is {}".format(reqLen, Len))


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
        super().__init__("bad keyword syntax. proper keyword syntax is {}:value".format(name))


class InvalidLoginOrPassword(Exception):
    def __init__(self):
        super().__init__("invalid login or password")


class NoSuchUser(Exception):
    def __init__(self, name):
        super().__init__(f"user {name} does not exist")
