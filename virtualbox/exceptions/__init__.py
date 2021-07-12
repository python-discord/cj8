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
