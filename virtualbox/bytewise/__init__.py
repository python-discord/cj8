def sxor(content: bytes, element: int) -> bytearray:
    """Prefroms sxor used in custom chiper"""
    return bytearray(map(lambda x: shift(x[1], element) ^ (x[0] % 256), enumerate(content)))


def rsxor(content: bytes, element: int) -> bytes:
    """Reverse sxor"""
    for index, item in enumerate(content):
        content[index] = rshift(content[index] ^ (index % 256), element)
    return content


def shift(byte: int, MN: int) -> int:
    """Shift byte to increasing side"""
    MN %= 8
    return ((byte << MN) | ((byte & ~(255 >> MN)) >> (8 - MN))) & 255


def rshift(byte: int, MN: int) -> int:
    """Shifts byte to decreasing side"""
    MN %= 8
    return ((byte >> MN) | ((byte & ~(255 << MN)) << (8 - MN))) & 255


def Hash(password: bytes) -> int:
    """Generates xor hash"""
    result = password[0]
    for i in password[1:]:
        result ^= i
    return result