import logging
from abc import ABC, abstractmethod
from typing import Callable, Set

from src.file_logging import logger


class BaseEvent(ABC):
    """Base event class"""

    @property
    def type(self) -> str:
        """
        Return the type of this event

        Used to make it easier to identity what type of event this in instead of having
        to use isinstance() check
        """
        return self._type

    @property
    @abstractmethod
    def _type(self) -> str:
        """Private method so it does not need a docstring in all subclasses"""
        ...


class PauseEvent(BaseEvent):
    """Indicate the pause event to the frontend"""

    @property
    def _type(self) -> str:
        return "pause"


class EventsMixin:
    """Class handling the events the backend generates"""

    def __init__(self):
        self._registered_hooks: Set[Callable] = set()

    def register_hook(self, callback: Callable[[BaseEvent], None]) -> None:
        """
        Register a callback to call for each event that is emitted

        Callback should be: def callback_1(event:BaseEvent)
        """
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug(f"Registering callback: {str(callback)}")

        self._registered_hooks.add(callback)

    def unhook_all(self) -> None:
        """Release all hooks"""
        self._registered_hooks.clear()

    def emit_event(self, event: BaseEvent) -> None:
        """
        Send event to all registered callbacks

        :param event: Event to emit
        """
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug(f"Emitting event: {event!s}")

        for callback in self._registered_hooks:
            callback(event)
