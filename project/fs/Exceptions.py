class NoSuchFileOrDirectory(Exception):
    def __init__(self):
        super().__init__("no such file or directory")


class FileOrDirectoryAlreadyExist(Exception):
    def __init__(self):
        super().__init__("file or directory already exist")


class NotAnDirectory(Exception):
    def __init__(self):
        super().__init__("not an directory")


class PermisionDenied(Exception):
    def __init__(self):
        super().__init__("permision denied")
