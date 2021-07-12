from .AbstractDungeonEntity import AbstractDungeonEntity
from .level import Level


class Enemy(AbstractDungeonEntity):
    """Enemy entity and hostile to players"""

    def __init__(self, current_level: Level, symbol: str = '^') -> None:
        super().__init__(
            ground_symbol=current_level.board[5][5],
            x=5,
            y=5,
            symbol=symbol
        )
        self.current_level = current_level

    def draw(self) -> None:
        """Draws enemies to board"""
        self.current_level.board[self.y][self.x] = self.symbol
