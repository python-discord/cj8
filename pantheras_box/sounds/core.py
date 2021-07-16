from pathlib import Path

from boombox import BoomBox

from pantheras_box.backend.core import CoreBackend
from pantheras_box.backend.events import BaseEvent, EventTypes
from pantheras_box.file_logging import logger


class CoreSounds:
    """Handles playing sounds that match an event"""

    SOUNDS_DIR = Path(__file__).absolute().parent / "static"

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
            logger.debug(
                f"[Sounds] No matching sound method for event {event} "
                f"- {key_error.args}"
            )
        except FileNotFoundError as file_not_file_error:
            logger.warning(
                f"[Sounds] Sound not found for event {event} "
                f"- {file_not_file_error.args}"
            )

    def play_sound(self, sound_name: str) -> None:
        """Play sound with specified name."""
        sound = self.SOUNDS_DIR / sound_name
        BoomBox(str(sound)).play()

    def _play_story_sound(self) -> None:
        self.play_sound("story.wav")

    def _play_pause_sound(self) -> None:
        self.play_sound("pause.wav")

    def _play_victory_sound(self) -> None:
        self.play_sound("victory.wav")

    def _play_failed_sound(self) -> None:
        self.play_sound("failed.wav")
