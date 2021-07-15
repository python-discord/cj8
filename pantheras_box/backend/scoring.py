from datetime import datetime
from typing import Dict, Optional

import yaml

from pantheras_box.backend.core import CoreBackend
from pantheras_box.backend.events import BaseEvent, EventTypes, FailedEvent, \
    LevelLoadedEvent
from pantheras_box.config import SCORE_FILE


class CoreScoring:
    """
    Scoring Module

    Scoring algorithm tbd.
    """

    _SCORE_FILE = SCORE_FILE

    def __init__(self, backend: CoreBackend):
        self.backend = backend
        backend.register_hook(self._event_handler)
        self._max_score = 0
        self._tiles_visited = 0
        self._level_start_time: Optional[datetime] = None
        self._level_finished_time: Optional[datetime] = None
        self._multiplier = 1
        self._current_level_name: str

        self.high_scores: Dict[str, int] = self._load_score_file()

    def _event_handler(self, event: BaseEvent) -> None:
        event_dispatcher = {
            EventTypes.level_loaded.value: self._handle_level_loaded,
            EventTypes.ball.value: self._handle_ball_movement,
            EventTypes.victory.value: self._handle_level_finished,
            EventTypes.failed.value: self._handle_level_finished,
        }
        event_type = event.type

        if event_type in event_dispatcher:
            event_dispatcher[event_type](event)

    def _write_to_file(self) -> None:
        with open(self._SCORE_FILE, "w") as score_file:
            yaml.dump(self.high_scores, score_file)

    def _load_score_file(self) -> Dict:
        # If the file does not exist
        if not self._SCORE_FILE.is_file():
            return {}

        with open(self._SCORE_FILE, "r") as score_file:
            high_scores = yaml.safe_load(score_file)

        # If the file is empty and not a dict
        if not high_scores:
            return {}

        return high_scores

    @property
    def level_high_score(self) -> str:
        """
        Return the high score for this level

        If no high score is found for this level return '-'
        """
        if self._current_level_name in self.high_scores:
            return str(self.high_scores[self._current_level_name])
        return "-"

    def _handle_level_finished(self, event: BaseEvent) -> None:
        self._level_finished_time = datetime.now()

        level_name = self._current_level_name
        current_score = self.current_score

        # Check if current score should be added to high scores
        if level_name not in self.high_scores:
            self.high_scores[level_name] = self.current_score
        else:
            if current_score > self.high_scores[level_name]:
                self.high_scores[level_name] = current_score

        self._write_to_file()

    def _handle_level_loaded(self, event: BaseEvent) -> None:
        event: LevelLoadedEvent
        self._level_start_time = datetime.now()
        self._level_finished_time = None
        self._max_score = self.backend.board.size[0] * self.backend.board.size[1]
        self._tiles_visited = 0
        self._current_level_name = event.level_name

    def _handle_ball_movement(self, event: BaseEvent) -> None:
        self._tiles_visited += 1
        self._max_score -= 1
        if self.current_score <= 0:
            self.backend.emit_event(FailedEvent())

    @property
    def current_score(self) -> int:
        """Return the current score for the level"""
        return int(self._max_score * self._multiplier) - self.elapsed_seconds

    @property
    def elapsed_seconds(self) -> int:
        """Return int of seconds since starting level"""
        if self._level_start_time:
            return (datetime.now() - self._level_start_time).seconds
        return 0
