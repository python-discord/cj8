from collections.abc import Iterable
from typing import Any, Callable

from virtualbox.exceptions import NoSuchIndex

# Wrappers


def restrictRange(min: int, max: int, keyword: str) -> Callable[[...], Any]:
    """Wrapper that restricts range of keyword"""
    def decorator(function: Callable[[Callable[[...], Any]], Any]) -> Callable[[Callable[[...], Any]], Any]:
        def check(*args, **kwargs) -> Callable[[...], Any]:
            if min <= kwargs[keyword] < max:
                return function(*args, **kwargs)
            raise NoSuchIndex()
        return check
    return decorator


# array related


def shiftArray(array: Iterable, num: int) -> Iterable:
    """Shifts iterable that is indexable by number to left"""
    num %= len(array)
    return array[num:] + array[:num]


def rshiftArray(array: Iterable, num: int) -> Iterable:
    """Shifts iterable that is indexable by number to right"""
    num %= len(array)
    return array[len(array) - num:] + array[:len(array) - num]


def loop(x: int, maxNum: int) -> int:
    """Function that ensures that x stays in 0 < x < maxNum boundary if x < 0"""
    if x < 0:
        return maxNum + x
    return x


def flatmap(x: Iterable) -> list:
    """HYMMMM"""
    return sum([flatmap(x) if isinstance(x, Iterable) else [x] for i in x], [])


def fill(list: list, to: int) -> list:
    """If list does not have requested lenght fills it with None until it does have it"""
    return list + [None]*(to - len(list))


def inAny(what: Iterable, inWhat: Iterable) -> bool:
    """Check if any content of what is in inWhat list"""
    return any(map(lambda x: x in inWhat, what))
