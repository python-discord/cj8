from src.backend.core import CoreBackend
from src.backend.events import BaseEvent, EventTypes, StoryEvent


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
        if event.type == EventTypes.story.value:
            event: StoryEvent
            self.move_story_forward(event.level_name)

    def move_story_forward(self, level_name: str) -> None:
        """Progress the story by providing the next block of text for the frontend"""
        ...
