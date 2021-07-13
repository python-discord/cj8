from random import choice

from .AbstractDungeonEntity import AbstractDungeonEntity


class Enemy(AbstractDungeonEntity):
    """Enemy entity and hostile to players"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def update(self) -> None:
        """Update enemy"""
        self.level.board[self.y][self.x] = self.ground_symbol
        self.mill()

    def mill(self) -> None:
        """Enemy randomly moves around"""
        movement_axis = choice(['x', 'y'])
        direction_axis = (1, -1)
        movement = choice(direction_axis)  # up or down (1, -1), left or right (1, -1)
        if movement_axis == 'x':  # movement will be on the x axis
            if (self.x <= 1 and movement == -1) or (self.x >= self.level.width - 2 and movement == 1):
                self.x += 1 if movement == -1 else -1
            else:
                self.x += movement
        if movement_axis == 'y':  # movement will be on the y axis
            if (self.y <= 1 and movement == -1) or (self.y >= self.level.height - 2 and movement == 1):
                self.y += 1 if movement == -1 else -1
            else:
                self.y += movement

    def draw(self) -> None:
        """Places entity on map"""
        self.level.board[self.y][self.x] = self.symbol
