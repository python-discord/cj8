def sxor(content, element):
    return bytearray(map(lambda x: shift(x[1], element) ^ x[0], enumerate(content)))


def rsxor(content, element):
    for index, item in enumerate(content):
        content[index] = rshift(content[index] ^ index, element)
    return content


def shift(byte, MN):
    MN %= 8
    return ((byte << MN) | ((byte & ~(255 >> MN)) >> (8 - MN))) & 255


def rshift(byte, MN):
    MN %= 8
    return ((byte >> MN) | ((byte & ~(255 << MN)) << (8 - MN))) & 255


def Hash(password):
    result = password[0]
    for i in password[1:]:
        result ^= i
    return result
