from fs.fs_exceptions import NoSuchIndex


def restrictRange(min, max, keyword):
    def decorator(function):
        def check(*args, **kwargs):
            if min <= kwargs[keyword] < max:
                return function(*args, **kwargs)
            raise NoSuchIndex()
        return check
    return decorator


"array shfting"


def shiftArray(array, num):
    num %= len(array)
    return array[num:] + array[:num]


def rshiftArray(array, num):
    num %= len(array)
    return array[len(array) - num:] + array[:len(array) - num]


def loop(x, maxNum):
    if x < 0:
        return maxNum + x
    return x
