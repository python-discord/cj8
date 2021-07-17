from __future__ import annotations

import copy
import os
import shutil
from typing import TYPE_CHECKING, Type, Union

from virtualbox.cryptology import decrypt, encrypt
from virtualbox.exceptions import CannotReadFileInTextMode

from .fs_ac import AC

if TYPE_CHECKING:
    from virtualbox.users.user import User


class File(AC):
    """File class"""

    def __init__(self, path: str, up: int, op: int, uid: int):
        super().__init__(up, op, uid)
        self.path = path

    @classmethod
    def TouchInit(cls, up: int, op: int, uid: int, path: str) -> 'File':
        """Inicialization method that creates empty File on host OS + file object"""
        tmp = cls(path, up, op, uid)
        tmp.create()

        return tmp

    # writing and reading
    @AC.writecheck
    def write(self, user: Type['User'], content: Union[bytes, str], binary: bool = False) -> None:
        """Writes content into file, in 2 modes text or binary"""
        with open(self.path, "wb" if binary else "w") as f:
            f.write(content)

    @AC.writecheck
    def append(self, user: Type['User'], content: Union[bytes, str], binary: bool = False) -> None:
        """Appends content to file, in 2 modes text or binary"""
        with open(self.path, "ab" if binary else "a") as f:
            f.write(content)

    @AC.readcheck
    def read(self, user: Type['User'], binary: bool = False) -> Union[str, bytes]:
        """Reads content of file, in 2 modes text or binary"""
        Content = ""
        try:
            with open(self.path, "rb" if binary else "r") as f:
                Content = f.read()
        except UnicodeDecodeError:
            raise CannotReadFileInTextMode()
        return Content

    @AC.execcheck
    def mvSelf(self, user: Type['User'], to: str) -> None:
        """Moves self into other path"""
        shutil.move(self.path, to)
        self.path = to

    @AC.execcheck
    def cpSelf(self, user: Type['User'], to: str) -> None:
        """Copies self into other path"""
        shutil.copy(self.path, to)
        result = copy.copy(self)
        result.path = to
        return result

    "cryptography"
    def encrypt(self, user: Type['User'], password: bytes, mode: int = 2) -> None:
        """Encrypts file content with given password"""
        self.write(user, encrypt(self.read(user, True), password, mode=mode), True)

    def decrypt(self, user: Type['User'], password: bytes, mode: int = 2) -> None:
        """Decrypts file content with given password"""
        self.write(user, decrypt(self.read(user, True), password, mode=mode), True)

    def decryptRead(self, user: Type['User'], password: bytes, mode: int = 2) -> bytes:
        """Decrypts contenct of the file and returns it with given password"""
        return decrypt(self.read(user, True), password, mode=mode)

    "self managment"
    def delete(self) -> None:
        """Deletes self"""
        os.remove(self.path)

    def create(self) -> None:
        """Creates self"""
        with open(self.path, "wb") as f:
            f.write(b"")
