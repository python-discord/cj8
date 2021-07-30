from base64 import urlsafe_b64decode, urlsafe_b64encode
from datetime import datetime
from os import urandom

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import relationship

Base: DeclarativeMeta = declarative_base()


class User(Base):
    """Class representing a local user of the 'Secret Crate of Grand Geckos'."""

    __tablename__ = "User"
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    salt = Column(String)
    credentials = relationship("Credential", cascade="all, delete")
    last_login = Column(DateTime)

    def __init__(self, username: str, password: str, password_confirm: str) -> None:
        salt_decoded = urandom(16)
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt_decoded, iterations=10000)
        key = urlsafe_b64encode(kdf.derive((password.encode("utf-8"))))
        f = Fernet(key)
        self.username = username
        self.password = f.encrypt(password.encode("utf-8")).decode("utf-8")
        self.salt = urlsafe_b64encode(salt_decoded).decode("utf-8")
        self.last_login = datetime.now()


class Credential(Base):
    """Class representing a credential of a local user of the 'Secret Crate of Grand Geckos'."""

    __tablename__ = "Credential"
    id = Column(Integer, primary_key=True)
    credential_name = Column(String)
    credential_username = Column(String)
    credential_password = Column(String)
    user_id = Column(Integer, ForeignKey("User.id"))
    platform = Column(String)
    user = relationship("User", back_populates="credentials")

    def __init__(
        self,
        credential_name: str,
        credential_username: str,
        credential_password: str,
        platform: str,
        actual_password: str,
        user: User,
    ) -> None:
        salt = urlsafe_b64decode(user.salt)
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=10000)
        key = urlsafe_b64encode(kdf.derive((actual_password.encode("utf-8"))))
        f = Fernet(key)
        self.credential_name = f.encrypt(credential_name.encode("utf-8")).decode("utf-8")
        self.credential_username = f.encrypt(credential_username.encode("utf-8")).decode("utf-8")
        self.credential_password = f.encrypt(credential_password.encode("utf-8")).decode("utf-8")
        self.platform = f.encrypt(platform.encode("utf-8")).decode("utf-8")
