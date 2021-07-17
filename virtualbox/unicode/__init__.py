from virtualbox.config import unicode


def encode(string: str) -> bytes:
    """Encodes string using default unicode"""
    return string.encode(unicode)


def decode(string: str) -> bytes:
    """Decodes string using default unicode"""
    return string.decode(unicode)
