from typing import List, Tuple, Union

from src.backend.level_loader import CoreLevelLoader
from src.backend.tiles import (
    BaseTile,
    CardinalDirection,
    GoalTile,
    PathTile,
    RedirectorTile,
    WallTile,
)


class DebugMixin:
    """Debugging mixin methods for the backend module"""


class CoreBackend(DebugMixin):
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

    def __init__(self) -> None:
        self._board = None

    def new_level(self) -> None:
        """Load a new random level."""
        self._board = CoreLevelLoader.random_level()

    def get_ball(self, surrounding_radius: float) -> Tuple[BaseTile, List[BaseTile]]:
        """
        Gets the ball tile

        Retrieves the ball tile as well as any tiles within an area with a radius of
        surrounding_radius.
        """
        ball = self._board.ball
        visible_tiles = []
        for row in self._board.all_tiles:
            for tile in row:
                if ball.calc_distance(tile) <= surrounding_radius:
                    visible_tiles.append(tile)
        return ball, visible_tiles

    def rotate_redirector(
        self, color: Tuple[int, int, int], clockwise: bool = True
    ) -> None:
        """Rotate redirector tiles of specified color clockwise by cw_angle."""
        for row in self._board.all_tiles + [[self._board.under_ball]]:
            for x, tile in enumerate(row):
                if isinstance(tile, RedirectorTile) and tile.color == color:
                    tile.rotate(clockwise)

    def move_ball(self) -> None:
        """Handle moving the ball in an appropriate direction."""
        ball = self._board.ball
        if isinstance(self._board.under_ball, RedirectorTile):
            ball.direction = self._board.under_ball.direction
        # This will cause gravity to affect the ball immediately after travelling up
        # elif not isinstance(ball.adjacent_tiles.down, WallTile):
        #     ball.direction = CardinalDirection.down
        self._move_ball()
        if isinstance(self._board.under_ball, GoalTile):
            self.new_level()

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

    def key_press(self, key: Union[str, None]) -> None:
        """
        Let the backend know when a key press has happened.

        This will trigger any actions that need to happen on the tiles.

        :param key: keyboard character that was pressed

        If the action is none then just move to the next frame with no input. This would
        be to advance the game by one step.
        """
