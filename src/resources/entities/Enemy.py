from random import choice

from .AbstractDungeonEntity import AbstractDungeonEntity


class Enemy(AbstractDungeonEntity):
    """Enemy entity and hostile to players"""

    def __init__(self, aggro_radius: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.aggro_radius = aggro_radius
        self.target: dict = {}

    def mill(self) -> None:
        """Random enemy movement"""
        movement_axis = choice(['x', 'y'])
        direction_axis = (1, -1)
        movement = choice(direction_axis)  # up or down (1, -1), left or right (1, -1)
        if movement_axis == 'x':  # movement will be on the x axis
            self.new_positions["x"] += movement
        if movement_axis == 'y':  # movement will be on the y axis
            self.new_positions["y"] += movement

    def follow(self) -> None:
        """Enemy movement function to chase player"""
        x = self.target['x']
        y = self.target['y']
        move_x = 0
        move_y = 0

        # find direction
        if self.x < x:
            move_x = 1
        if self.x > x:
            move_x = -1

        if self.y < y:
            move_y = 1
        if self.y > y:
            move_y = -1

        # move in that direction
        self.new_positions["x"] = move_x
        self.new_positions["y"] = move_y

    def is_in_radius(self, x: int, y: int) -> bool:
        """Check if player is in 'aggro' radius"""
        radius = self.aggro_radius
        if (y - radius <= self.y <= y + radius) and \
                (x - radius <= self.x <= x + radius):
            self.symbol.stylize("bold red")
            self.target = {'x': x, 'y': y}
            return True
        else:
            self.symbol.stylize("bold white")
            return False
