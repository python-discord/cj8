import sys
from pathlib import Path

from playsound import PlaysoundException, playsound

from src.backend.core import CoreBackend
from src.backend.events import BaseEvent, EventTypes
from src.file_logging import logger


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
            logger.warning(
                f"[Sounds] No matching sound method for event {event} "
                f"- {key_error.args}"
            )
        except PlaysoundException as playsound_error:
            logger.warning(
                f"[Sounds] Failed to play sound for event {event} "
                f"- {playsound_error.args}"
            )

    def play_sound(self, sound_name: str) -> None:
        """Play sound with specified name."""
        sound = self.SOUNDS_DIR / sound_name
        # Currently, playsound does not support non-blocking mode on Linux
        # https://github.com/TaylorSMarks/playsound/pull/72
        playsound(str(sound), block=sys.platform == "linux")

    def _play_story_sound(self) -> None:
        self.play_sound("story.wav")

    def _play_pause_sound(self) -> None:
        self.play_sound("pause.wav")

    def _play_victory_sound(self) -> None:
        self.play_sound("victory.wav")

    def _play_failed_sound(self) -> None:
        self.play_sound("failed.wav")

    def _play_ambient_sounds(self) -> None:
        self.play_sound("ambient.wav")
