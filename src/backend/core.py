from typing import List, Tuple, Union

from src.backend.tiles import BaseTile


class BoardCollection:
    """Representation of the game board"""


class CoreBackend:
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

    def get_ball(self, surrounding_radius: float) -> Tuple[BaseTile, List[BaseTile]]:
        """
        Gets the ball tile

        Retrieves the ball tile as well as any tiles within an area with a radius of
        surrounding_radius.

        """

    def key_press(self, key: Union[str, None]) -> None:
        """
        Let the backend know when a key press has happened.

        This will trigger any actions that need to happen on the tiles.

        :param key: keyboard character that was pressed

        If the action is none then just move to the next frame with no input. This would
        be to advance the game by one step.
        """
