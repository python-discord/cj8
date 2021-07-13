from src.resources.level import Level

from .AbstractDungeonEntity import AbstractDungeonEntity


class Enemy(AbstractDungeonEntity):
    """Enemy entity and hostile to players"""

    def __init__(self, current_level: Level, x: int = 3, y: int = 3, symbol: str = '^') -> None:
        super().__init__(
            ground_symbol=current_level.board[5][5],
            x=x,
            y=y,
            symbol=symbol
        )
        self.current_level = current_level

    def draw(self) -> None:
        """Draws enemies to board"""
        self.current_level.board[self.y][self.x] = self.symbol
