import bisect

from virtualbox.exceptions import UIDAlreadyExist


class Uidspace:
    """Queue for users id"""

    def __init__(self, start: int):
        self.start = start
        self.queue = []

    def getUid(self) -> int:
        """Generates UID and makes sure that it wont be generated again"""
        if len(self.queue) == 0:
            self.start += 1
            return self.start - 1
        else:
            return self.queue.pop(0)

    def delUid(self, uid: int) -> None:
        """Deletes specified uid form possible list"""
        if uid > self.start:
            self.queue += list(range(self.start, uid + 1))
            self.start = uid + 1
            return

        tmp = bisect.bisect(self.queue, uid) - 1
        print(self.queue)
        print(tmp)
        if tmp < len(self.queue) and self.queue[tmp] == uid:
            del self.queue[tmp]
            return
        raise UIDAlreadyExist()

    def restoreUid(self, uid: int) -> None:
        """Adds uid again to possible uids"""
        bisect.insort(self.queue, uid)
        for i in range(len(self.queue)):
            if self.queue[-1] != self.start - 1:
                break
            self.start -= 1
            del self.queue[-1]
