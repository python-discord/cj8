class Drawable:

    def __init__(self):
        self.parts = []

    def draw(self):
        wholePart = ""
        for part in self.parts:
            wholePart+=part
        return wholePart

    
class Player(Drawable):

    """
        Every draw, create_body and delete function works the same.
        Draw function prints everything in parts list.
        Create body puts every character at the needed position and puts them in parts list.
        Delete writes with whitespace and changes text color to background color and puts blue background back.

    """
    def __init__(self, x, y, terminal):
        super().__init__()
        self.x = x
        self.y = y
        self.terminal = terminal

    def create_body(self):  # Creates the body of the player. Puts all the characters toghether in parts list
        self.parts = []
        eye1 = self.terminal.move_xy(self.x + 1, self.y + 1) + self.terminal.white(self.terminal.on_blue('▘'))
        self.parts.append(eye1)
        eye2 = self.terminal.move_xy(self.x + 2, self.y + 1) + self.terminal.white(self.terminal.on_blue('▝'))
        self.parts.append(eye2)
        left = self.terminal.move_xy(self.x, self.y + 1) + self.terminal.blue(self.terminal.on_blue(' '))
        self.parts.append(left)
        right = self.terminal.move_xy(self.x + 3, self.y + 1) + self.terminal.blue(self.terminal.on_blue(' '))
        self.parts.append(right)
        up1 = self.terminal.move_xy(self.x, self.y) + self.terminal.blue(self.terminal.on_midnightblue('▟'))
        self.parts.append(up1)
        up2 = self.terminal.move_xy(self.x + 1, self.y) + self.terminal.blue(self.terminal.on_blue(' '))
        self.parts.append(up2)
        up3 = self.terminal.move_xy(self.x + 2, self.y) + self.terminal.blue(self.terminal.on_blue(' '))
        self.parts.append(up3)
        up4 = self.terminal.move_xy(self.x + 3, self.y) + self.terminal.blue(self.terminal.on_midnightblue('▙'))
        self.parts.append(up4)
        leg1 = self.terminal.move_xy(self.x, self.y + 2) + self.terminal.blue(self.terminal.on_midnightblue('▞'))
        self.parts.append(leg1)
        leg4 = self.terminal.move_xy(self.x + 3, self.y + 2) + self.terminal.blue(self.terminal.on_midnightblue('▚'))
        self.parts.append(leg4)
        leg2 = self.terminal.move_xy(self.x + 1, self.y + 2) + self.terminal.blue(self.terminal.on_midnightblue('▍'))
        self.parts.append(leg2)
        leg3 = self.terminal.move_xy(self.x + 2, self.y + 2) + self.terminal.blue(self.terminal.on_midnightblue('▍'))
        self.parts.append(leg3)

    def draw(self):
        self.create_body()
        return super().draw()
    
    def draw_inside_box(self):
        string = ""
        eye1 = self.terminal.move_xy(self.x + 1, self.y + 1) + self.terminal.white(self.terminal.on_gray15('▘'))
        string += eye1
        eye2 = self.terminal.move_xy(self.x + 2, self.y + 1) + self.terminal.white(self.terminal.on_gray15('▝'))
        string += eye2
        print(string, flush=True)

class Box(Drawable):
    def __init__(self, x, y, terminal):
        super().__init__()
        self.x = x
        self.y = y
        self.terminal = terminal
        self.create_body()

    def create_body(self):
        self.parts = []
        up1 = self.terminal.move_xy(self.x, self.y) + self.terminal.navajowhite4(self.terminal.on_navajowhite3('▛'))
        self.parts.append(up1)
        up2 = self.terminal.move_xy(self.x + 1, self.y) + self.terminal.navajowhite4(self.terminal.on_navajowhite3('▔'))
        self.parts.append(up2)
        up3 = self.terminal.move_xy(self.x + 2, self.y) + self.terminal.navajowhite4(self.terminal.on_navajowhite3('▔'))
        self.parts.append(up3)
        up4 = self.terminal.move_xy(self.x + 3, self.y) + self.terminal.navajowhite4(self.terminal.on_navajowhite3('▜'))
        self.parts.append(up4)
        up1 = self.terminal.move_xy(self.x, self.y + 1) + self.terminal.navajowhite4(self.terminal.on_navajowhite3('▙'))
        self.parts.append(up1)
        up2 = self.terminal.move_xy(self.x + 1, self.y + 1) + self.terminal.navajowhite4(self.terminal.on_navajowhite3('▁'))
        self.parts.append(up2)
        up3 = self.terminal.move_xy(self.x + 2, self.y + 1) + self.terminal.navajowhite4(self.terminal.on_navajowhite3('▁'))
        self.parts.append(up3)
        up4 = self.terminal.move_xy(self.x + 3, self.y + 1) + self.terminal.navajowhite4(self.terminal.on_navajowhite3('▟'))
        self.parts.append(up4)

    def draw(self):
        self.create_body()
        return super().draw()

class Target(Drawable):
    def __init__(self, x, y, terminal):
        super().__init__()
        self.x = x
        self.y = y
        self.terminal = terminal
        self.create_body()

    def create_body(self):
        self.parts = []
        up1 = self.terminal.move_xy(self.x, self.y) + self.terminal.gray38(self.terminal.on_midnightblue('▛'))
        self.parts.append(up1)
        up2 = self.terminal.move_xy(self.x + 1, self.y) + self.terminal.gray38(self.terminal.on_midnightblue('▔'))
        self.parts.append(up2)
        up3 = self.terminal.move_xy(self.x + 2, self.y) + self.terminal.gray38(self.terminal.on_midnightblue('▔'))
        self.parts.append(up3)
        up4 = self.terminal.move_xy(self.x + 3, self.y) + self.terminal.gray38(self.terminal.on_midnightblue('▜'))
        self.parts.append(up4)
        up1 = self.terminal.move_xy(self.x, self.y + 1) + self.terminal.gray38(self.terminal.on_midnightblue('▙'))
        self.parts.append(up1)
        up2 = self.terminal.move_xy(self.x + 1, self.y + 1) + self.terminal.gray38(self.terminal.on_midnightblue('▁'))
        self.parts.append(up2)
        up3 = self.terminal.move_xy(self.x + 2, self.y + 1) + self.terminal.gray38(self.terminal.on_midnightblue('▁'))
        self.parts.append(up3)
        up4 = self.terminal.move_xy(self.x + 3, self.y + 1) + self.terminal.gray38(self.terminal.on_midnightblue('▟'))
        self.parts.append(up4)


class Platform(Drawable):
    def __init__(self, x, y, lenght, flat, terminal):
        super().__init__()
        self.x = x
        self.y = y
        self.terminal = terminal
        self.lenght = lenght
        self.flat = flat
        self.create_body()

    def create_body(self):
        if self.flat:  # checks if the platform is horizontal or not and builds it based on that
            up1 = self.terminal.move_xy(self.x, self.y) + self.terminal.orchid4(self.terminal.on_plum4('▛'))
            self.parts.append(up1)
            for i in range(1, self.lenght - 1):
                up2 = self.terminal.move_xy(self.x + i, self.y) + self.terminal.orchid4(self.terminal.on_plum4('▔'))
                self.parts.append(up2)
            up3 = self.terminal.move_xy(self.x + self.lenght - 1, self.y) + self.terminal.orchid4(self.terminal.on_plum4('▜'))
            self.parts.append(up3)
        else:
            for i in range(0, self.lenght):
                up = self.terminal.move_xy(self.x, self.y + i) + self.terminal.orchid4(self.terminal.on_plum4('▚'))
                self.parts.append(up)


class ThinkingBox(Drawable):
    def __init__(self, x, y, terminal):
        super().__init__()
        self.x = x
        self.y = y
        self.terminal = terminal
        self.create_body()

    def create_body(self):
        up1 = self.terminal.move_xy(self.x, self.y) + self.terminal.gray37(self.terminal.on_gray15('▛'))
        self.parts.append(up1)
        for i in range(1, 7):
            up2 = self.terminal.move_xy(self.x + i, self.y) + self.terminal.gray37(self.terminal.on_gray15('▔'))
            self.parts.append(up2)
        up3 = self.terminal.move_xy(self.x + 7, self.y) + self.terminal.gray37(self.terminal.on_gray15('▜'))
        self.parts.append(up3)
        middle1 = self.terminal.move_xy(self.x, self.y + 1) + self.terminal.gray37(self.terminal.on_gray15('▏'))
        self.parts.append(middle1)
        for i in range(1, 7):
            middle2 = self.terminal.move_xy(self.x + i, self.y + 1) + self.terminal.gray37(self.terminal.on_gray15(' '))
            self.parts.append(middle2)
        middle3 = self.terminal.move_xy(self.x + 7, self.y + 1) + self.terminal.gray37(self.terminal.on_gray15('▕'))
        self.parts.append(middle3)
        down1 = self.terminal.move_xy(self.x, self.y + 2) + self.terminal.gray37(self.terminal.on_gray15('▏'))
        self.parts.append(down1)
        for i in range(1, 7):
            down2 = self.terminal.move_xy(self.x + i, self.y + 2) + self.terminal.gray37(self.terminal.on_gray15(' '))
            self.parts.append(down2)
        down3 = self.terminal.move_xy(self.x + 7, self.y + 2) + self.terminal.gray37(self.terminal.on_gray15('▕'))
        self.parts.append(down3)
    
    def draw_inside_box(self):
        string = ""
        for i in self.parts:
            string += i
        print(string, flush=True)
