from random import choice

from .AbstractDungeonEntity import AbstractDungeonEntity


class Enemy(AbstractDungeonEntity):
    """Enemy entity and hostile to players"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def update(self, x: int, y: int) -> None:
        """Update enemy. Chooses mill or follow based on passed position."""
        self.level.board[self.y][self.x] = self.ground_symbol
        if self.is_in_radius(x, y, 3):
            self.follow(x, y)
        else:
            self.mill()

    def mill(self) -> None:
        """Random enemy movement"""
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

    def follow(self, x: int, y: int) -> None:
        """Enemy movement function to chase player"""
        move_x = 0
        move_y = 0

        if self.x > x:
            move_x = -1
        if self.x < x:
            move_x = 1

        if self.y > y:
            move_y = -1
        if self.y < y:
            move_y = 1

        self.x += move_x
        self.y += move_y

    def is_in_radius(self, x: int, y: int, radius: int) -> bool:
        """Check if player is in 'aggro' radius"""
        if (y - radius <= self.y <= y + radius) and (x - radius <= self.x <= x + radius):
            self.symbol.stylize("bold red")
            return True
        else:
            self.symbol.stylize("bold white")
            return False

    def draw(self) -> None:
        """Places entity on map"""
        self.level.board[self.y][self.x] = self.symbol
