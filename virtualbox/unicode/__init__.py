from virtualbox.config import unicode


def encode(string):
    return bytes(string, unicode)


def decode(string):
    return string.decode(unicode)
