import pymunk
import pymunk.pygame_util
import pygame
from typing import Tuple

WINDOW = {'w': 100,
          'h': 30}


class MySpace:
    def __init__(self):
        self.space = pymunk.Space()
        self.space.gravity = 0, 30
        self.create_borders(self.space.static_body)

    # without borders, the items could fall "out of the screen"
    def create_borders(self, b0):
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

    def add_platform(self, topleft: Tuple[int, int], width: int, height: int):
        body = pymunk.Body(0, 0, body_type=pymunk.Body.STATIC)
        body.position = topleft[0] + width/2, topleft[1] + height/2   # the pymunk library uses center coordinates

        shape = pymunk.Poly.create_box(body, (width, height), radius=0)
        shape.elasticity = 0
        shape.friction = 5   # for the box not to slide away if the player stops on a platform

        self.space.add(body, shape)
        return shape

    def add_box(self, topleft: Tuple[int, int]):
        w, h = 4, 2
        body = pymunk.Body(1, 10, body_type=pymunk.Body.DYNAMIC)
        body.position = topleft[0] + w/2, topleft[1] + h/2

        shape = pymunk.Poly.create_box(body, (w, h), radius=0)
        shape.elasticity = 0
        shape.friction = 5

        self.space.add(body, shape)
        return shape

    def get_position(self, item: pymunk.Poly):
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
    space.add_platform((5, 20), 20, 3)
    box = space.add_box((10, 10))
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
