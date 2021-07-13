from backend.core import CoreBackend
from backend.events import BaseEvent


class CoreStory:
    """
    Core story module

    Responsible for loading, storing and progressing the story when required.
    """

    def __init__(self, backend: CoreBackend):
        self.backend = backend
        self.backend.register_hook(self.story_callback)

    def story_callback(self, event: BaseEvent) -> None:
        """Callback to handle StoryEvents"""
        ...
