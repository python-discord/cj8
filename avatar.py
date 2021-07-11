from collections import namedtuple
from blessed import Terminal
from blessed.colorspace import X11_COLORNAMES_TO_RGB

DEFAULT_COLOUR = X11_COLORNAMES_TO_RGB["aqua"]

class Point:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
    
    def __iter__(self):
        self.n = 0
        return self
    
    def __next__(self):
        if self.n < 2:
            result = [self.x, self.y][self.n]
            self.n += 1
            return result
        else:
            raise StopIteration
    
    def __add__(self, other: any):
        if type(other).__name__ == "Point":
            x = self.x + other.x
            y = self.y + other.y
        else:
            x = self.x + other[0]
            y = self.y + other[1]
        return Point(x, y)

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"


class Cursor:
    def __init__(self, coords: Point, term: Terminal, fill="██",
                colour=DEFAULT_COLOUR, speed=2) -> None:
        """creates a Cursor Object that can be moved on command"""
        self.coords = coords
        self.fill = fill
        self.colour = colour
        self.speed = speed
        self.term = term
        self.commands = {"r": self.render, "c": self.clear}

    directions = {
        "KEY_UP": Point(0,-1),
        "KEY_DOWN": Point(0, 1),
        "KEY_LEFT": Point(-1, 0),
        "KEY_RIGHT": Point(1, 0)
        }
    
    def move(self, direction: str):
        render_string = []
        render_string.append(self.clear())
        directions = Cursor.directions[direction]
        self.coords.x = min(max(self.coords.x + directions.x*self.speed, 0), self.term.width-2)
        self.coords.y = min(max(self.coords.y + directions.y*self.speed, 0), self.term.height-2)
        # self.coords += Avatar.directions[direction]
        render_string.append(self.render())
        return "".join(render_string)
    
    def clear(self):
        return f"{self.term.move_xy(*self.coords)}  "
    
    def render(self):
        render_string = []
        render_string.append(f"{self.term.move_xy(*self.coords)}")
        render_string.append(f"{self.term.color_rgb(*self.colour)}")
        render_string.append(f"{self.fill}{self.term.normal}")
        return "".join(render_string)


def main():
    from blessed import Terminal
    term = Terminal()
    Coords = Point(5, 10)
    avi = Cursor(Coords, term)
    print(term.home+term.clear+term.normal, end="")
    print(term.height, term.width)
    print(f"{term.move_xy(*avi.coords)}{term.color_rgb(*avi.colour)}{avi.fill}{term.normal}")
    with term.cbreak():
        val = ""
        while val.lower() != 'q':
            val = term.inkey(timeout=3)
            if val.is_sequence:
                if 257 < val.code < 262:
                    print(term.home+term.clear_eol+str(avi.coords))
                    print(avi.move(val.name))
            else:
                if val.lower() == "r":
                    print(avi.render())
                elif val.lower() == "c":
                    print(avi.clear())
        print(f'bye!{term.normal}')
    print(max(Coords))


if __name__ == "__main__":
    main()