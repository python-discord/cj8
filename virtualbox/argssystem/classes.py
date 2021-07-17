from typing import Any

from virtualbox.exceptions import ConversionError, ConversionErrorMulti


class MultiType:
    """Type that ties to converts varable to specifeied types with specified order.

    if it succeds it returns it if not it raises ConversionErrorMulti
    """

    def __init__(self, *types):
        self.types = types

    def __call__(self, var: Any) -> Any:
        """HYMMMMMMM"""
        for i in self.types:
            try:
                return i(var)
            except TypeError:
                pass
        raise ConversionErrorMulti(var, self.types)


class Optional:
    """Optional argument class"""

    def __init__(self, type: type, default: int):
        self.type = type
        self.default = default

    def __call__(self, var: any):
        """HYMMMMM"""
        if var is None:
            return self.default
        try:
            return self.type(var)
        except TypeError:
            raise ConversionError(self.type, var)


class Flag:
    """Allows for flag creation"""

    def __init__(self, value: Any):
        self.value = value


class Keyword(Flag):
    """Childeren of Flag allows for keywords(name + separator + value) creation"""

    def __init__(self, type: type):
        self.type = type

    def __call__(self, var: Any):
        """HYMMMM"""
        try:
            return self.type(var)
        except TypeError:
            raise ConversionError(self.type, var)
