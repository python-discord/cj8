from AC import AC


class File(AC):
    def __init__(self, path, up, op, uid):
        super().__init__(up, op, uid)
        self.path = path

    @AC.writecheck
    def write(self, content):
        with open(self.path, "w") as f:
            f.write(content)
        return True

    @AC.writecheck
    def append(self, content):
        with open(self.path, "a") as f:
            f.write(content)
        return True

    @AC.readcheck
    def read(self):
        Content = ""
        with open(self.path, "r") as f:
            Content = f.read()
        return Content
