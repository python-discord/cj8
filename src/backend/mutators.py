from abc import ABC, abstractmethod
from typing import List

from src.backend.core import CoreBackend
from src.backend.events import BaseEvent, MutatorEvent
from src.file_logging import logger


class BaseMutator(ABC):
    """Base mutator class"""

    def __init__(self, backend: CoreBackend):
        self.backend = backend
        self.state = False

    def activate(self) -> None:
        """Activate the mutator effect"""
        self.state = True
        return self._activate()

    def deactivate(self) -> None:
        """Deactivate the mutator effect"""
        self.state = False
        return self._deactivate()

    @abstractmethod
    def _activate(self) -> None:
        """Private method so it does not need a docstring in all subclasses"""
        ...

    @abstractmethod
    def _deactivate(self) -> None:
        """Private method so it does not need a docstring in all subclasses"""
        ...


class FOVReduce(BaseMutator):
    """Reduce the field of vision"""

    value = 2

    def _activate(self) -> None:
        self.backend.FOV -= self.value

    def _deactivate(self) -> None:
        self.backend.FOV += self.value


class SpeedIncrease(BaseMutator):
    """Increase the tick speed"""

    value = 2

    def _activate(self) -> None:
        self.backend.TICKS_PER_MOVE -= self.value

    def _deactivate(self) -> None:
        self.backend.TICKS_PER_MOVE += self.value


class CoreMutators(BaseMutator):
    """
    Handles applying mutators that match an event

    Calling mutator methods on CoreMutators will affect all registered mutators.
    """

    def __init__(self, backend: CoreBackend):
        super().__init__(backend)
        self.backend.register_hook(self.event_callback)
        self._mutators = {
            "FOV Reduce": FOVReduce(self.backend),
            "Speed Increase": SpeedIncrease(self.backend),
        }

    def event_callback(self, event: BaseEvent) -> None:
        """Consume all events and apply the matching mutator"""
        # Call matching method
        if not isinstance(event, MutatorEvent):
            return

        try:
            if name := event.name:
                mutator = self._mutators[name]
            else:
                mutator = self
            state = event.state
        except KeyError as key_error:
            logger.warning(
                f"[Sounds] No matching mutator method for event {event} "
                f"- {key_error.args}"
            )
        else:
            self.set_mutator_state(mutator, state)

    @staticmethod
    def set_mutator_state(mutator: BaseMutator, state: bool) -> None:
        """Set mutator to state"""
        if state:
            mutator.activate()
        else:
            mutator.deactivate()

    @property
    def mutators(self) -> List[str]:
        """Return list of all mutator names"""
        return list(self._mutators.keys())

    @property
    def active_mutators(self) -> List[str]:
        """Return list of active mutator names"""
        active_mutators = []
        for name, mutator in self._mutators.items():
            if mutator.state:
                active_mutators.append(name)
        return active_mutators

    def _activate(self) -> None:
        for mutator in self._mutators.values():
            mutator.activate()

    def _deactivate(self) -> None:
        for mutator in self._mutators.values():
            mutator.deactivate()
