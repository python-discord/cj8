from .fs_parser import readxml, savexml


class ACL:
    """
    access control list

    stores permisions in tuple with folowing order other perrmision, user permision, user indentification id
    """

    def __init__(self, dicit: dict) -> None:
        self.dicit = dicit

    def add(self, name: str, perm: tuple) -> None:
        """Adds permison to ACL"""
        self.dicit[name] = perm

    def remove(self, name: str) -> None:
        """Removes permison from ACL"""
        del self.dicit[name]

    # file handeling
    def save(self, path: str) -> None:
        """Saves ACL to XML file"""
        savexml(self.dicit, path, ("op", "up", "uid"), "acl")

    @classmethod
    def InitRead(cls, path: str):
        """Inicialization method that reads saved file"""
        return cls(readxml(path, int))

    # diciti like
    def __iter__(self) -> iter:
        return iter(self.dicit.items())

    def __getitem__(self, key: str) -> tuple:
        return self.dicit[key]

    def __setitem__(self, key: str, item: tuple) -> None:
        self.dicit[key] = item

    def items(self) -> list:
        """Equivalent of dicit.list"""
        return self.dicit.items()

    def __delitem__(self, key: str) -> None:
        del self.dicit[key]

    # debug
    def __repr__(self) -> str:
        return str(self.dicit)
