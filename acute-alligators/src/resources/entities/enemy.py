from random import choice

from .abstractdungeonentity import AbstractDungeonEntity


class Enemy(AbstractDungeonEntity):
    """Enemy entity and hostile to players"""

    def __init__(self, aggro_radius: int, file: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.AGGRO_RADIUS = aggro_radius
        self.ENTITY_TYPE = "enemy"
        self.target: dict = {}
        self.player_detected = False
        self.file = file

    def mill(self) -> None:
        """Random enemy movement"""
        movement_axis = choice(['x', 'y'])
        direction_axis = (1, -1)
        # up or down (1, -1), left or right (1, -1)
        movement = choice(direction_axis)
        # movement will be on the x axis
        if movement_axis == 'x':
            self.new_positions["x"] += movement
        # movement will be on the y axis
        if movement_axis == 'y':
            self.new_positions["y"] += movement

    def follow(self, testing: bool = False) -> None:
        """Enemy movement function to chase player"""
        if not testing:
            x = self.target['x']
            y = self.target['y']
            move_x = 0
            move_y = 0

            # find direction
            if abs(x - self.x) > abs(y - self.y):
                if self.x < x:
                    move_x = 1
                if self.x > x:
                    move_x = -1
            elif abs(x - self.x) < abs(y - self.y):
                if self.y < y:
                    move_y = 1
                if self.y > y:
                    move_y = -1

            # move in that direction
            self.new_positions["x"] = move_x
            self.new_positions["y"] = move_y

    def flee(self, testing: bool = False) -> None:
        """Enemy movement function to chase player"""
        if not testing:
            x = self.target['x']
            y = self.target['y']
            move_x = 0
            move_y = 0

            # find direction
            if abs(x - self.x) > abs(y - self.y):
                if self.x < x:
                    move_x = -1
                if self.x > x:
                    move_x = 1
            elif abs(x - self.x) < abs(y - self.y):
                if self.y < y:
                    move_y = -1
                if self.y > y:
                    move_y = 1

            # move in that direction
            self.new_positions["x"] = move_x
            self.new_positions["y"] = move_y

    def run(self, x: int, y: int) -> None:
        """Enemy movement  to run from player"""
        move_x = 0
        move_y = 0

        # find direction
        if abs(x - self.x) > abs(y - self.y):
            if self.x > x:
                move_x = 1
            if self.x < x:
                move_x = -1
        elif abs(x - self.x) < abs(y - self.y):
            if self.y > y:
                move_y = 1
            if self.y < y:
                move_y = -1
        else:
            if self.x > x:
                move_x = 1
            if self.x < x:
                move_x = -1
            if self.y > y:
                move_y = 1
            if self.y < y:
                move_y = -1

        # move in that direction
        self.new_positions["x"] = move_x
        self.new_positions["y"] = move_y

    def is_in_radius(self, x: int, y: int) -> bool:
        """Check if player is in 'aggro' radius"""
        radius = self.AGGRO_RADIUS
        if (y - radius <= self.y <= y + radius) and \
                (x - radius <= self.x <= x + radius):
            self.symbol.stylize("bold " + self.symbol.style)
            self.target = {'x': x, 'y': y}
            self.player_detected = True
            return True
        else:
            self.symbol.stylize(self.symbol.style)
            self.player_detected = False
            return False
