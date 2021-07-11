import bisect
from virtualbox.exceptions import UIDAlreadyExist


class Uidspace:
    def __init__(self, start):
        self.start = start
        self.queue = []

    def genUid(self):
        if len(self.queue) == 0:
            return self.start
        else:
            return self.queue.pop(0)

    def delUid(self, uid):
        if uid > self.start:
            self.queue += list(range(self.start, uid + 1))
            self.start = uid + 1
            return

        tmp = bisect(self.queue, uid)
        if tmp < len(self.queue) and self.queue[tmp] == uid:
            del self.queue[tmp]
            return
        raise UIDAlreadyExist()

    def restoreUid(self, uid):
        bisect.insort(uid, self.queue)
        for i in range(1, len(self.queue) + 1):
            if self.queue[-i] != self.start - 1:
                break
            self.start -= 1
            del self.queue[-i]
