" ENCRYPTION LIBRARY - DEVELOPED BY CHEERFUL CHEETAHS (Contributed by Coder400, SirArthurWelesley)"
from virtualbox.config import ALL_CHARACTERS
from virtualbox.exceptions import NotAnIntiger
from virtualbox.functions.generalfunctions import restrictRange
from virtualbox.functions.generalfunctions import shiftArray
from virtualbox.functions.generalfunctions import rshiftArray
from virtualbox.unicode import decode
from virtualbox.unicode import encode
from virtualbox.bytewise import sxor
from virtualbox.bytewise import rsxor
from virtualbox.bytewise import Hash

"encrytption functions"


def customChiperEncrypt(content, password):
    content = bytearray(content)
    for i in password:
        content = shiftArray(sxor(content, i), i)
    return bytes(content)


def customChiperDecrypt(content, password):
    content = bytearray(content)
    for i in reversed(password):
        content = rsxor(rshiftArray(content, i), i)
    return bytes(content)


def basicXor(content, password):
    return bytes(map(lambda x: x ^ Hash(password), content))


def xorEncrypt(content, password):
    return bytes(map(lambda x: x[1] ^ password[x[0] % len(password)], enumerate(content)))


def cesar_chiper(characters, msg, shift, reverse=False):
    encrypted_msg = ""
    try:
        shift = int(shift)
    except ValueError:
        raise NotAnIntiger
    "If reversed, make the factor negative."
    factor = 1
    if reverse:
        factor = -1
    "for each character in message."
    for character in msg:
        "Find character, shift it and then add it to the message."
        character_index = characters.index(character)
        encrypted_msg += characters[(character_index+(shift*factor)) % len(characters)]
    "Return the encrypted message"
    return encode(encrypted_msg)


"encrypt/decrypt funcions"


@restrictRange(min=0, max=4, keyword="mode")
def encrypt(content, password, mode=2):
    return [basicXor,
            xorEncrypt,
            customChiperEncrypt,
            lambda x, y: cesar_chiper(ALL_CHARACTERS, decode(x), y)][mode](content, password)


@restrictRange(min=0, max=4, keyword="mode")
def decrypt(content, password, mode=2):
    return [basicXor,
            xorEncrypt,
            customChiperDecrypt,
            lambda x, y: cesar_chiper(ALL_CHARACTERS, decode(y), y, reverse=True)
            ][mode](content, password)
