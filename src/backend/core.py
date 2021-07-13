from typing import List, Optional, Tuple, Union

from src.backend.events import EventsMixin, PauseEvent, StoryEvent
from src.backend.level_loader import BoardCollection, CoreLevelLoader
from src.backend.tiles import (
    BaseTile,
    BlindTile,
    CardinalDirection,
    GoalTile,
    PathTile,
    RedirectorTile,
    StoryTile,
    WallTile,
)


class DebugMixin:
    """Debugging mixin methods for the backend module"""


class CoreBackend(DebugMixin, EventsMixin):
    """
    Backend Module

    Responsible for storing the state of the game as well as update the state once
    action have taken place.

    Should return the tile object which represents the ball as well and any tiles
    within a certain distance from the ball.

    Should generate a random board that is solvable.

    Should return the position of the box at the end.

    Should list mutators as well as being able to apply and remove these mutators.

    Should keep track of elapsed time and current score.
    """

    CONTROL_PAIRS = [
        ("1", "3"),
        ("q", "e"),
        ("a", "d"),
        ("z", "c"),
    ]

    def __init__(self) -> None:
        super().__init__()
        self._board: Union[BoardCollection, None] = None
        self._controls = {}
        self._FOV = 5
        self.win_count = 0
        self.mutators = {}

    def new_level(self, level_name: Optional[str] = None) -> None:
        """
        Load level with the specified name.

        If level_name is None, load a random level.
        """
        self._controls = {keys: None for keys in self.CONTROL_PAIRS}
        if not level_name:
            self._board = CoreLevelLoader.random_level()
        else:
            self._board = CoreLevelLoader.load(level_name)
        self._gen_controls()

    def restart_level(self) -> None:
        """Reload the current level."""
        if not self._board:
            return
        self.new_level(self._board.level_path.name)

    def get_board(self) -> List[List[BaseTile]]:
        """Return list of visible tiles within FOV."""
        ball = self._board.ball
        all_tiles = [row[:] for row in self._board.all_tiles]
        for row in all_tiles:
            for x, tile in enumerate(row):
                if isinstance(tile, GoalTile):
                    continue
                if ball.calc_distance(tile) > self._FOV:
                    row[x] = BlindTile(pos=(tile.pos.x, tile.pos.y))
        return all_tiles

    def rotate_redirector(
        self, color: Tuple[int, int, int], clockwise: bool = True
    ) -> None:
        """Rotate redirector tiles of specified color clockwise."""
        for row in self._board.all_tiles + [[self._board.under_ball]]:
            for x, tile in enumerate(row):
                if isinstance(tile, RedirectorTile) and tile.color == color:
                    tile.rotate(clockwise)

    def move_ball(self) -> None:
        """Handle moving the ball in an appropriate direction."""
        if not self._board:
            return
        ball = self._board.ball
        if isinstance(self._board.under_ball, RedirectorTile):
            ball.direction = self._board.under_ball.direction
        # This will cause gravity to affect the ball immediately after travelling up
        # elif not isinstance(ball.adjacent_tiles.down, WallTile):
        #     ball.direction = CardinalDirection.down
        self._move_ball()
        under_ball_tile = self._board.under_ball

        self._is_ball_on_goal(under_ball_tile)

        self._is_ball_on_story_tile(under_ball_tile)

    def _is_ball_on_goal(self, under_ball: BaseTile) -> None:
        """Test if the ball is on the goal tile"""
        if isinstance(under_ball, GoalTile):
            self.win_count += 1
            self.new_level()

    def _is_ball_on_story_tile(self, under_ball: BaseTile) -> None:
        if isinstance(under_ball, StoryTile):
            if not under_ball.visited:
                self.emit_event(StoryEvent(self._board.level_name))
                under_ball.visited = True

    def _move_ball(self) -> None:
        ball = self._board.ball
        x, y = 0, 0
        if ball.direction == CardinalDirection.up:
            y = -1
        elif ball.direction == CardinalDirection.right:
            x = 1
        elif ball.direction == CardinalDirection.down:
            y = 1
        elif ball.direction == CardinalDirection.left:
            x = -1

        y_idx = ball.pos.y
        x_idx = ball.pos.x

        # Return if the next tile will be a wall
        next_tile = self._board.all_tiles[y_idx + y][x_idx + x]
        if isinstance(next_tile, WallTile):
            ball.direction = CardinalDirection.down  # Apply gravity again
            return

        if not self._board.under_ball:
            self._board.all_tiles[y_idx][x_idx] = PathTile(
                pos=(y_idx, x_idx), color=(0, 0, 0)
            )
        else:
            self._board.all_tiles[y_idx][x_idx] = self._board.under_ball
        self._board.under_ball = next_tile
        self._board.all_tiles[y_idx + y][x_idx + x] = ball
        ball.pos.y += y
        ball.pos.x += x
        self._board.link_adjacents()

    def _gen_controls(self) -> None:
        redirectors = [
            tile
            for row in self._board.all_tiles
            for tile in row
            if isinstance(tile, RedirectorTile)
        ]
        for tile in redirectors:
            if tile.color in self._controls.values():
                continue
            for k, v in self._controls.items():
                if not v:
                    self._controls[k] = tile.color
                    break

    def key_press(self, key: str) -> None:
        """
        Let the backend know when a key press has happened.

        This will trigger any actions that need to happen on the tiles.

        :param key: keyboard character that was pressed
        """
        if key == "[":
            self.new_level()
            return
        elif key == "]":
            self.restart_level()
            return

        if key == "p":
            event = PauseEvent()
            self.emit_event(event)

        for key_pair, color in self._controls.items():
            try:
                direction = bool(key_pair.index(key))
                break
            except ValueError:
                continue
        else:
            return
        self.rotate_redirector(color, clockwise=direction)
