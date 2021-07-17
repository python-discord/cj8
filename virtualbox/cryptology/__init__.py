"""ENCRYPTION LIBRARY - DEVELOPED BY CHEERFUL CHEETAHS (Contributed by Coder400, SirArthurWelesley)"""
from typing import Union

from virtualbox.bytewise import Hash, rsxor, sxor
from virtualbox.config import ALL_CHARACTERS
from virtualbox.exceptions import NotAnIntiger
from virtualbox.functions.generalfunctions import (
    restrictRange, rshiftArray, shiftArray
)
from virtualbox.unicode import decode, encode

"encryption functions"


def customChiperEncrypt(content: bytes, password: bytes) -> bytes:
    """Encrypts string with custom chyper algorithm"""
    content = bytearray(content)
    for i in password:
        content = shiftArray(sxor(content, i), i)
    return bytes(content)


def customChiperDecrypt(content: bytes, password: bytes) -> bytes:
    """Decrypts string with custom chyper algorithm"""
    content = bytearray(content)
    for i in reversed(password):
        content = rsxor(rshiftArray(content, i), i)
    return bytes(content)


def basicXor(content: bytes, password: bytes) -> bytes:
    """Xor of password hash and content"""
    return bytes(map(lambda x: x ^ Hash(password), content))


def xorEncrypt(content: bytes, password: bytes) -> bytes:
    """Xor of password leater and content on % len(password) position in content"""
    return bytes(map(lambda x: x[1] ^ password[x[0] % len(password)], enumerate(content)))


def cesar_chiper(characters: str, msg: str, shift: int, reverse: bool = False) -> bytes:
    """Encrypts/decrypts cesar's chiper"""
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


# encrypt/decrypt funcions


@restrictRange(min=0, max=4, keyword="mode")
def encrypt(content: str, password: str, mode: int = 2) -> Union[str, bytes]:
    """Encrypts content with password using algorithm specified by mode

    1 = basicXor
    2 = xor
    3 = customChiper
    4 = cesar'chiper
    """
    return [basicXor,
            xorEncrypt,
            customChiperEncrypt,
            lambda x, y: cesar_chiper(ALL_CHARACTERS, decode(x), y)][mode](content, password)


@restrictRange(min=0, max=4, keyword="mode")
def decrypt(content: bytes, password: bytes, mode: int = 2) -> Union[str, bytes]:
    """Decrypts content with password using algorithm specified by mode

    1 = basicXor
    2 = xor
    3 = customChiper
    4 = cesar'chiper
    """
    return [basicXor,
            xorEncrypt,
            customChiperDecrypt,
            lambda x, y: cesar_chiper(ALL_CHARACTERS, decode(y), y, reverse=True)
            ][mode](content, password)
