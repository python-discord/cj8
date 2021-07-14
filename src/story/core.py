from pathlib import Path
from typing import Dict, Optional

import yaml

from src.backend.core import CoreBackend
from src.backend.events import BaseEvent, EventTypes, StoryEvent


class CoreStory:
    """
    Core story module

    Responsible for loading, storing and progressing the story when required.
    """

    STORY_DIR = Path(__file__).parent.absolute() / "static"
    MANIFEST_FILE = STORY_DIR / "manifest.yaml"

    def __init__(self, backend: CoreBackend):
        self.backend = backend
        self.backend.register_hook(self.story_callback)
        self.manifest_conf: Dict = self._load_manifest()
        self.current_story: Optional[str] = None

    def _load_manifest(self) -> Dict:
        with open(self.MANIFEST_FILE, "r") as manifest:
            manifest_conf = yaml.safe_load(manifest)

        return manifest_conf

    @property
    def prologue(self) -> str:
        """Get the prologue about the game"""
        return self.manifest_conf["main"]["prologue"]

    def story_callback(self, event: BaseEvent) -> None:
        """Callback to handle StoryEvents"""
        if event.type == EventTypes.story.value:
            event: StoryEvent
            self.move_story_forward(event.level_name)

    def move_story_forward(self, level_name: Optional[str]) -> None:
        """Progress the story by providing the next block of text for the frontend"""
        if not level_name:
            self.current_story = None
            return
        self.current_story = self.manifest_conf["main"][level_name]


if __name__ == "__main__":
    backend = CoreBackend()
    story = CoreStory(backend)
