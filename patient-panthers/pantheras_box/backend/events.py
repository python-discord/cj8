import logging
from abc import ABC, abstractmethod
from enum import Enum
from typing import Callable, Optional, Set

from pantheras_box.file_logging import logger


class EventTypes(Enum):
    """Enum type for event types"""

    level_loaded = "level_loaded"
    story = "story"
    pause = "pause"
    victory = "victory"
    failed = "failed"
    mutator = "mutator"
    ball = "ball_movement"


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
        return EventTypes.pause.value


class StoryEvent(BaseEvent):
    """
    A story tile triggers the story to move forwards

    If level_name is None, reset current story.
    """

    def __init__(self, level_name: Optional[str] = None) -> None:
        super().__init__()
        self.level_name = level_name

    @property
    def _type(self) -> str:
        return EventTypes.story.value

    def __str__(self):
        return f"Story Event for level {self.level_name}"


class VictoryEvent(BaseEvent):
    """Represents the player winning a level"""

    def __init__(self, score: int) -> None:
        super().__init__()
        self.score = score

    @property
    def _type(self) -> str:
        return EventTypes.victory.value


class FailedEvent(BaseEvent):
    """Represents the player losing a level"""

    @property
    def _type(self) -> str:
        return EventTypes.failed.value


class MutatorEvent(BaseEvent):
    """
    Set a mutator with name to state

    If name is None, affect all mutators.
    Default action is to enable.
    """

    _RANDOM = "RANDOM"

    def __init__(self, name: Optional[str] = None, state: bool = True) -> None:
        super().__init__()
        self.name = name
        self.state = state

    @property
    def _type(self) -> str:
        return EventTypes.mutator.value

    @classmethod
    def activate_random_mutator(cls) -> "MutatorEvent":
        """Return event to trigger random mutator"""
        return cls(name=cls._RANDOM, state=True)


class BallMovementEvent(BaseEvent):
    """Indicate the ball have moved"""

    @property
    def _type(self) -> str:
        return EventTypes.ball.value


class LevelLoadedEvent(BaseEvent):
    """Indicates a level has been loaded"""

    def __init__(self, level_name: str) -> None:
        super().__init__()
        self.level_name = level_name

    @property
    def _type(self) -> str:
        return EventTypes.level_loaded.value


class EventsMixin:
    """
    Class handling the events the backend generates

    Serves as a communication pattern to pass events between each module so each module
    can react to each event without the backend module needing any context.
    """

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
            logger.debug(f"[Event] Emitting event: {event!s}")

        for callback in self._registered_hooks:
            callback(event)
