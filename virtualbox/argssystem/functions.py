from functools import wraps
from typing import Any, Callable

from virtualbox.exceptions import (
    NoSuchFlagOrOption, WrongAmmountOfArguments, WrongKeywordUsage
)
from virtualbox.functions.generalfunctions import fill

from .classes import Flag, Optional


def expand_args(argpos: int, *names: str, start: int = 1) -> Callable[[...], Any]:
    """Expands function arguments"""
    def wrapper(func: Callable[[...], Any]) -> Callable[[...], Any]:
        arguments = []
        keys = {}
        rlen = 0

        ant = func.__annotations__
        for i in names:
            if isinstance(ant[i], Flag):
                keys[i] = ant[i]
            else:
                arguments.append(ant[i])
                if not isinstance(ant[i], Optional):
                    rlen += 1

        @wraps(func)
        def process(*args: Any) -> Any:
            pargs = []
            pkeys = []
            for i in args[argpos][start:]:
                if i.split(":")[0] in keys:
                    pkeys.append(i.split(":"))
                else:
                    pargs.append(i)

            if len(pargs) < rlen:
                raise WrongAmmountOfArguments(rlen, len(pargs))
            x = fill(pargs, len(arguments))

            passargs = map(lambda x: x[0](x[1]), zip(arguments, x))
            passkeys = {}
            for item in pkeys:
                try:
                    key = keys[item[0]]
                except KeyError:
                    raise NoSuchFlagOrOption(item[0])

                if len(item) == 1:
                    if isinstance(key, Flag):
                        passkeys[item[0]] = key.value
                    else:
                        raise WrongKeywordUsage(item[0])
                else:
                    passkeys[item[0]] = key(item[1])

            return func(*args[:argpos], *passargs, *args[argpos + 1:], **passkeys)

        return process
    return wrapper
