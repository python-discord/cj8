import itertools
from dataclasses import dataclass
from typing import Iterator, Optional


@dataclass
class Credential:
    username: str
    password: str
    id: int
    platform: str
    notes: str = ""


class ExampleDB:
    """
    Simple Example database to work with the publiccly facing functions. Not to
    be used in real code.
    """

    _cred_ids = itertools.count()

    def __init__(self):
        self._db = [
            Credential("sofi", "password", id=next(self._cred_ids), platform="google.com"),
            Credential("greg", "12345678", id=next(self._cred_ids), platform="google.com"),
            Credential("bob", "123asd123asd", id=next(self._cred_ids), platform="google.com"),
            Credential("sofi", "password321", id=next(self._cred_ids), platform="pypi.org"),
        ]

    @property
    def platforms(self) -> Iterator[str]:
        return iter(set(cred.platform for cred in self._db))

    @property
    def accounts(self) -> Iterator[Credential]:
        return iter(self._db)

    def match_username(self, username: str) -> Iterator[Credential]:
        return iter(cred for cred in self._db if cred.username == username)

    def match_platform(self, platform: str) -> Iterator[Credential]:
        return iter(cred for cred in self._db if cred.platform == platform)

    def match_password(self, password: str) -> Iterator[Credential]:
        return iter(cred for cred in self._db if cred.password == password)

    def search(self, search: str) -> Iterator[Credential]:
        return iter(
            cred for cred in self._db if search in cred.username or search in cred.platform or search in cred.notes
        )

    def add_account(self, username: str, password: Optional[str] = None, *, platform: str):
        cred = Credential(username, password or "ENCRYPTED_EXAMPLE", id=next(self._cred_ids), platform=platform)
        self._db.append(cred)

    def remove_account(self, account: Credential):
        if account not in self._db:
            raise Exception("Account does not exist in database.")

        self._db.remove(account)


if __name__ == "__main__":
    # TODO: Make a better testing system.

    db = ExampleDB()

    from pprint import pprint

    print("Platforms:")
    pprint(list(db.platforms))
    print("Accounts:")
    pprint(list(db.accounts))
    platform = next(db.platforms)
    print('Match username "sofi":')
    pprint(list(db.match_username("sofi")))
    print("Match Platform", platform)
    pprint(list(db.match_platform(platform)))
    print('Match Password "12345678":')
    pprint(list(db.match_password("12345678")))
    print('Search: "google.com":')
    pprint(list(db.search("google.com")))
    db.add_account("sofi@example.com", "12345678", platform="reddit.com")
    print('Search: "sof":')
    pprint(list(db.search("sof")))
    db.remove_account(next(db.search("sofi@")))
    print('Delete first "sofi@"')
    pprint(list(db.search("sofi@")))
    pprint(list(db.platforms))
