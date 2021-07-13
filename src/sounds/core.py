from src.backend.core import CoreBackend
from src.backend.events import BaseEvent, EventTypes
from src.file_logging import logger


class CoreSounds:
    """Handles playing sounds that match an event"""

    def __init__(self, backend: CoreBackend):
        self.backend = backend
        self.backend.register_hook(self.event_callback)

    def event_callback(self, event: BaseEvent) -> None:
        """Consume all events and produce the matching sound"""
        event_dispatcher = {
            EventTypes.story.value: self._play_story_sound,
            EventTypes.pause.value: self._play_pause_sound,
            EventTypes.victory.value: self._play_victory_sound,
            EventTypes.failed.value: self._play_failed_sound,
        }

        # Call matching method
        try:
            event_dispatcher[event.type]()
        except KeyError as key_error:
            logger.warning(
                f"""
                [Sounds] No matching sound method for event {event}
                - {key_error.args}"""
            )

    def _play_story_sound(self) -> None:
        ...

    def _play_pause_sound(self) -> None:
        ...

    def _play_victory_sound(self) -> None:
        ...

    def _play_failed_sound(self) -> None:
        ...

    def _play_ambient_sounds(self) -> None:
        ...
