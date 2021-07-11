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
