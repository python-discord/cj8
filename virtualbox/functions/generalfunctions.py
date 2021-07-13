from virtualbox.exceptions import NoSuchIndex

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
<<<<<<< HEAD


def flatmap(x):
    return sum([flatmap(x) if isinstance(x, Iterable) else [x] for i in x], [])


def inAny(what, inWhat):
    return any(map(lambda x: x in inWhat, what))
=======
>>>>>>> parent of fb517fd (Merge branch 'SirArthur' of https://github.com/cj8-cheerful-cheetahs/project into SirArthur)
