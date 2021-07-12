from typing import Tuple

import pygame
import pymunk
import pymunk.pygame_util
from blessed.keyboard import Keystroke

WINDOW = {'w': 100,
          'h': 30}

COLLISION = {'platform': 0,
             'box': 1,
             'target': 2,
             'player': 3}


def center(topleft: Tuple[float, float], width: int, height: int) -> Tuple[float, float]:
    return topleft[0] + width/2, topleft[1] + height/2


class MySpace:
    def __init__(self):
        self.space = pymunk.Space()
        self.space.gravity = 0, 30
        self.create_borders(self.space.static_body)
        self.player: pymunk.Poly

    # without borders, the items could fall "out of the screen"
    def create_borders(self, b0: pymunk.Body) -> None:
        topleft = 0, 0
        topright = WINDOW['w'], 0
        bottomleft = 0, WINDOW['h']
        bottomright = WINDOW['w'], WINDOW['h']
        corners = [topleft, topright, bottomright, bottomleft]

        for i in range(len(corners)):
            border = pymunk.Segment(b0, corners[i], corners[(i+1) % 4], 0)
            border.elasticity = 0    # we don't want the borders to interact with our moving items
            border.friction = 0
            self.space.add(border)

    def add_object(self, topleft: Tuple[float, float], type: str = 'platform', w: int = 1, h: int = 1) -> pymunk.Poly:
        types = {"platform": {"body_type": pymunk.Body.STATIC, 'w': w, 'h': h, "mass": 0, "mom": 0},
                 "box": {"body_type": pymunk.Body.DYNAMIC, 'w': 4, 'h': 2, "mass": 1, "mom": 10},
                 "target": {"body_type": pymunk.Body.STATIC, 'w': 2, 'h': 0.1, "mass": 1, "mom": 10},
                 "player": {"body_type": pymunk.Body.DYNAMIC, 'w': 4, 'h': 3, "mass": 1, "mom": 10}}

        if type in types.keys():
            body = pymunk.Body(types[type]["mass"], types[type]["mom"], types[type]["body_type"])
            body.position = center(topleft, types[type]['w'], types[type]['h'])

            shape = pymunk.Poly.create_box(body, (types[type]['w'], types[type]['h']), radius=0)
            shape.collision_type = COLLISION[type]
            shape.elasticity = 0
            shape.friction = 5

            self.space.add(body, shape)
            if type == "player":
                self.player = shape
            return shape

    def move_player(self, key: Keystroke) -> None:
        if key.name == "KEY_UP":
            impulse = 0, -20.494
            self.player.body.apply_impulse_at_local_point(impulse)
        if key.name == "KEY_DOWN":
            impulse = 0, 20.494
            self.player.body.apply_impulse_at_local_point(impulse)
        if key.name == "KEY_LEFT":
            self.player.body.position += pymunk.Vec2d(-1, 0)
        if key.name == "KEY_RIGHT":
            self.player.body.position += pymunk.Vec2d(1, 0)

    def get_position(self, item: pymunk.Poly) -> Tuple[int, int]:
        vertices = item.get_vertices()
        topleft = vertices.pop(len(vertices) - 1)
        x, y = topleft + item.body.position

        return round(x), round(y)


if __name__ == "__main__":
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WINDOW['w'], WINDOW['h']))
    draw_options = pymunk.pygame_util.DrawOptions(screen)

    space = MySpace()
    space.add_object((5, 20), type="platform", w=20, h=3)
    box = space.add_object((10, 10), type="box")
    # here you can add testing for the methods

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((255, 255, 255))
        space.space.debug_draw(draw_options)
        print(space.get_position(box))
        # here too

        pygame.display.flip()
        space.space.step(1/60)
        clock.tick(60)

    pygame.quit()
