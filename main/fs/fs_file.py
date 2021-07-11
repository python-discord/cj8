from fs.fs_ac import AC
from fs.fs_cryptology import encrypt
from fs.fs_cryptology import decrypt
import os


class File(AC):
    def __init__(self, path, up, op, uid):
        super().__init__(up, op, uid)
        self.path = path

    @classmethod
    def TouchInit(cls, up, op, uid, path):
        tmp = cls(path, up, op, uid)
        tmp.create()

        return tmp

    "writing and reading"
    @AC.writecheck
    def write(self, user, content, binary=False):
        with open(self.path, "wb" if binary else "w") as f:
            f.write(content)
        return True

    @AC.writecheck
    def append(self, user, content, binary=False):
        with open(self.path, "ab" if binary else "a") as f:
            f.write(content)
        return True

    @AC.readcheck
    def read(self, user, binary=False):
        Content = ""
        with open(self.path, "rb" if binary else "r") as f:
            Content = f.read()
        return Content

    "cryptography"
    def encrypt(self, user, password, mode=2):
        self.write(user, encrypt(self.read(user, True), password, mode=mode), True)

    def decrypt(self, user, password, mode=2):
        self.write(user, decrypt(self.read(user, True), password, mode=mode), True)

    def decryptRead(self, user, password, mode=2):
        return decrypt(self.read(user, True), password, mode=mode)

    "self managment"
    def delete(self):
        os.remove(self.path)

    def create(self):
        with open(self.path, "wb") as f:
            f.write(b"")
