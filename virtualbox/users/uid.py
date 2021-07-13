import bisect
from virtualbox.exceptions import UIDAlreadyExist


class Uidspace:
    def __init__(self, start):
        self.start = start
        self.queue = []

    def getUid(self):
        if len(self.queue) == 0:
            self.start += 1
            return self.start - 1
        else:
            return self.queue.pop(0)

    def delUid(self, uid):
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

    def restoreUid(self, uid):
        bisect.insort(self.queue, uid)
        for i in range(len(self.queue)):
            if self.queue[-1] != self.start - 1:
                break
            self.start -= 1
            del self.queue[-1]
