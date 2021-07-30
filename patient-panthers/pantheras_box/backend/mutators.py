import random
from abc import ABC, abstractmethod
from typing import List

from pantheras_box.backend.core import CoreBackend
from pantheras_box.backend.events import BaseEvent, MutatorEvent
from pantheras_box.file_logging import logger


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


class InvertControls(BaseMutator):
    """Invert redirector controls"""

    def _toggle(self) -> None:
        self.backend.CONTROL_PAIRS = [(k2, k1) for k1, k2 in self.backend.CONTROL_PAIRS]
        self.backend._gen_controls()

    _activate = _toggle
    _deactivate = _toggle


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
            "Invert Controls": InvertControls(self.backend),
        }

    def event_callback(self, event: BaseEvent) -> None:
        """Consume all events and apply the matching mutator"""
        # Call matching method
        if not isinstance(event, MutatorEvent):
            return

        try:
            if not (name := event.name):
                mutator = self
            elif name == MutatorEvent._RANDOM:
                self._activate_random_mutators()
                return
            else:
                mutator = self._mutators[name]
            state = event.state
        except KeyError as key_error:
            logger.warning(
                f"[Mutators] No matching mutator method for event {event} "
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

    def _activate_random_mutators(self) -> None:
        """Activate random mutators, up to max_mutators"""
        n = random.choices(
            [0, 1, 2, 3],
            weights=[50, 30, 15, 5],
        )[0]
        for _ in range(n):
            mutator = random.choice(self.mutators)
            while mutator in self.active_mutators:
                mutator = random.choice(self.mutators)
            self._mutators[mutator].activate()

    def _activate(self) -> None:
        for mutator in self._mutators.values():
            if not mutator.state:
                mutator.activate()

    def _deactivate(self) -> None:
        for mutator in self._mutators.values():
            if mutator.state:
                mutator.deactivate()
