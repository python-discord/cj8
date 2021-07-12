class Player:
    """
        Every draw, create_body and delete function works the same.
        Draw function prints everything in parts list.
        Create body puts every character at the needed position and puts them in parts list.
        Delete writes with whitespace and changes text color to background color and puts blue background back.

    """
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.parts = []

    def create_body(self, terminal):  # Creates the body of the player. Puts all the characters toghether in parts list
        self.parts = []
        eye1 = terminal.move_xy(self.x + 1, self.y + 1) + terminal.white(terminal.on_blue('▘'))
        self.parts.append(eye1)
        eye2 = terminal.move_xy(self.x + 2, self.y + 1) + terminal.white(terminal.on_blue('▝'))
        self.parts.append(eye2)
        left = terminal.move_xy(self.x, self.y + 1) + terminal.blue(terminal.on_blue(' '))
        self.parts.append(left)
        right = terminal.move_xy(self.x + 3, self.y + 1) + terminal.blue(terminal.on_blue(' '))
        self.parts.append(right)
        up1 = terminal.move_xy(self.x, self.y) + terminal.blue(terminal.on_midnightblue('▟'))
        self.parts.append(up1)
        up2 = terminal.move_xy(self.x + 1, self.y) + terminal.blue(terminal.on_blue(' '))
        self.parts.append(up2)
        up3 = terminal.move_xy(self.x + 2, self.y) + terminal.blue(terminal.on_blue(' '))
        self.parts.append(up3)
        up4 = terminal.move_xy(self.x + 3, self.y) + terminal.blue(terminal.on_midnightblue('▙'))
        self.parts.append(up4)
        leg1 = terminal.move_xy(self.x, self.y + 2) + terminal.blue(terminal.on_midnightblue('▞'))
        self.parts.append(leg1)
        leg4 = terminal.move_xy(self.x + 3, self.y + 2) + terminal.blue(terminal.on_midnightblue('▚'))
        self.parts.append(leg4)
        leg2 = terminal.move_xy(self.x + 1, self.y + 2) + terminal.blue(terminal.on_midnightblue('▍'))
        self.parts.append(leg2)
        leg3 = terminal.move_xy(self.x + 2, self.y + 2) + terminal.blue(terminal.on_midnightblue('▍'))
        self.parts.append(leg3)

    def move(self, val, terminal):  # Move player, pass val variable from main loop
        if val.name == "KEY_UP":
            self.delete(terminal)
            self.y -= 1
            self.create_body(terminal)
        if val.name == "KEY_DOWN":
            self.delete()
            self.y += 1
            self.create_body(terminal)
        if val.name == "KEY_RIGHT":
            self.delete()
            self.x += 1
            self.create_body(terminal)
        if val.name == "KEY_LEFT":
            self.delete()
            self.x -= 1
            self.create_body(terminal)

    def delete(self, terminal):  # delete the player at the current location
        for y in range(self.y, self.y+3):
            deleted = terminal.move_xy(self.x, y) + terminal.midnightblue(terminal.on_midnightblue('    '))
            print(deleted, end='', flush=True)

    def draw(self, terminal):  # draws the player at it's x and y location
        self.create_body(terminal)
        for part in self.parts:
            print(part, end='', flush=True)


class Box:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.parts = []
        self.create_body()

    def create_body(self, terminal):
        self.parts = []
        up1 = terminal.move_xy(self.x, self.y) + terminal.navajowhite4(terminal.on_navajowhite3('▛'))
        self.parts.append(up1)
        up2 = terminal.move_xy(self.x + 1, self.y) + terminal.navajowhite4(terminal.on_navajowhite3('▔'))
        self.parts.append(up2)
        up3 = terminal.move_xy(self.x + 2, self.y) + terminal.navajowhite4(terminal.on_navajowhite3('▔'))
        self.parts.append(up3)
        up4 = terminal.move_xy(self.x + 3, self.y) + terminal.navajowhite4(terminal.on_navajowhite3('▜'))
        self.parts.append(up4)
        up1 = terminal.move_xy(self.x, self.y + 1) + terminal.navajowhite4(terminal.on_navajowhite3('▙'))
        self.parts.append(up1)
        up2 = terminal.move_xy(self.x + 1, self.y + 1) + terminal.navajowhite4(terminal.on_navajowhite3('▁'))
        self.parts.append(up2)
        up3 = terminal.move_xy(self.x + 2, self.y + 1) + terminal.navajowhite4(terminal.on_navajowhite3('▁'))
        self.parts.append(up3)
        up4 = terminal.move_xy(self.x + 3, self.y + 1) + terminal.navajowhite4(terminal.on_navajowhite3('▟'))
        self.parts.append(up4)

    def draw(self):
        for part in self.parts:
            print(part, end='', flush=True)

    def delete(self, terminal):
        for y in range(self.y, self.y+2, terminal):
            deleted = terminal.move_xy(self.x, y) + terminal.midnightblue(terminal.on_midnightblue('    '))
            print(deleted, end='', flush=True)


class Platform:
    def __init__(self, x, y, lenght, flat):
        self.x = x
        self.y = y
        self.parts = []
        self.lenght = lenght
        self.flat = flat
        self.create_body()

    def create_body(self, terminal):
        self.parts = []
        if self.flat:  # checks if the platform is horizontal or not and builds it based on that
            up1 = terminal.move_xy(self.x, self.y) + terminal.orchid4(terminal.on_plum4('▛'))
            self.parts.append(up1)
            for i in range(1, self.lenght - 1):
                up2 = terminal.move_xy(self.x + i, self.y) + terminal.orchid4(terminal.on_plum4('▔'))
                self.parts.append(up2)
            up3 = terminal.move_xy(self.x + self.lenght - 1, self.y) + terminal.orchid4(terminal.on_plum4('▜'))
            self.parts.append(up3)
        else:
            for i in range(0, self.lenght):
                up = terminal.move_xy(self.x, self.y + i) + terminal.orchid4(terminal.on_plum4('▚'))
                self.parts.append(up)

    def draw(self):
        for part in self.parts:
            print(part, end='', flush=True)


class ThinkingBox:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.create_body()
        self.parts = []

    def create_body(self, terminal):
        up1 = terminal.move_xy(self.x, self.y) + terminal.gray37(terminal.on_gray15('▛'))
        self.parts.append(up1)
        for i in range(1, 7):
            up2 = terminal.move_xy(self.x + i, self.y) + terminal.gray37(terminal.on_gray15('▔'))
            self.parts.append(up2)
        up3 = terminal.move_xy(self.x + 7, self.y) + terminal.gray37(terminal.on_gray15('▜'))
        self.parts.append(up3)
        middle1 = terminal.move_xy(self.x, self.y + 1) + terminal.gray37(terminal.on_gray15('▏'))
        self.parts.append(middle1)
        for i in range(1, 7):
            middle2 = terminal.move_xy(self.x + i, self.y + 1) + terminal.gray37(terminal.on_gray15(' '))
            self.parts.append(middle2)
        middle3 = terminal.move_xy(self.x + 7, self.y + 1) + terminal.gray37(terminal.on_gray15('▕'))
        self.parts.append(middle3)
        down1 = terminal.move_xy(self.x, self.y + 2) + terminal.gray37(terminal.on_gray15('▏'))
        self.parts.append(down1)
        for i in range(1, 7):
            down2 = terminal.move_xy(self.x + i, self.y + 2) + terminal.gray37(terminal.on_gray15(' '))
            self.parts.append(down2)
        down3 = terminal.move_xy(self.x + 7, self.y + 2) + terminal.gray37(terminal.on_gray15('▕'))
        self.parts.append(down3)

    def draw(self):
        for part in self.parts:
            print(part, end='', flush=True)
