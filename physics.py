import logging
from typing import Tuple

import pygame
import pymunk
import pymunk.pygame_util
from blessed.keyboard import Keystroke

logging.basicConfig(filename="logging.txt", filemode='w', level=logging.INFO)

WINDOW = {'w': 100,
          'h': 30}

COLLISION = {'platform': 0,
             'box': 1,
             'target': 2,
             'player': 3}


def center(topleft: Tuple[float, float], width: int, height: int) -> Tuple[float, float]:
    return topleft[0] + width/2, topleft[1] + height/2


def player_and_box_coll(arbiter: pymunk.Arbiter, space, data):
    logging.info("player and box collided")
    player = arbiter.shapes[0].body
    box = arbiter.shapes[1].body

    pos_diff = player.position - box.position
    if pos_diff[0] < 0:  # this will return True when the player is left to the box
        box.position += pymunk.Vec2d(1, 0)
    elif pos_diff[0] > 0:
        box.position += pymunk.Vec2d(-1, 0)

    return False


def get_position(item: pymunk.Poly) -> Tuple[int, int]:
    vertices = item.get_vertices()
    topleft = vertices.pop(len(vertices) - 1)
    x, y = topleft + item.body.position

    return round(x), round(y)


class MySpace:
    def __init__(self):
        self.space = pymunk.Space()
        self.space.gravity = 0, 30
        self.create_borders(self.space.static_body)
        self.add_collision_handlers()
        self.targets_to_engage = 0
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

    def add_collision_handlers(self):
        player_and_box = self.space.add_collision_handler(COLLISION["player"], COLLISION["box"])
        player_and_box.begin = player_and_box_coll
        box_and_target = self.space.add_collision_handler(COLLISION["box"], COLLISION["target"])
        box_and_target.begin = self.box_and_target_coll

    def add_object(self, topleft: Tuple[float, float], type: str = 'platform', w: int = 1, h: int = 1) -> pymunk.Poly:
        types = {"platform": {"body_type": pymunk.Body.STATIC, 'w': w, 'h': h, "mass": 0, "mom": 0},
                 "box": {"body_type": pymunk.Body.DYNAMIC, 'w': 4, 'h': 2, "mass": 1, "mom": 10},
                 "target": {"body_type": pymunk.Body.STATIC, 'w': 2, 'h': 0.01, "mass": 0, "mom": 0},
                 "player": {"body_type": pymunk.Body.DYNAMIC, 'w': 4, 'h': 3, "mass": 1, "mom": 10}}

        if type in types.keys():
            body = pymunk.Body(types[type]["mass"], types[type]["mom"], types[type]["body_type"])
            # pymunk works with center-position and we work with topleft
            body.position = center(topleft, types[type]['w'], types[type]['h'])

            shape = pymunk.Poly.create_box(body, (types[type]['w'], types[type]['h']), radius=0.2)
            shape.collision_type = COLLISION[type]
            shape.elasticity = 0
            shape.friction = 1
            if type == "target":
                shape.sensor = True
                self.targets_to_engage += 1

            self.space.add(body, shape)
            if type == "player":
                self.player = shape
            return shape

    def move_player(self, key: Keystroke) -> None:
        # TODO: block doublejump and double pull-down
        if key.name == "KEY_UP":
            impulse = 0, -20.494   # based on my calculations this should send the jellyfish around 7 pixels high
            self.player.body.apply_impulse_at_local_point(impulse)
        if key.name == "KEY_DOWN":
            impulse = 0, 20.494
            self.player.body.apply_impulse_at_local_point(impulse)
        if key.name == "KEY_LEFT":
            self.player.body.position += pymunk.Vec2d(-1, 0)
        if key.name == "KEY_RIGHT":
            self.player.body.position += pymunk.Vec2d(1, 0)

    def step(self, fps: int) -> None:
        self.space.step(1/fps)

    def box_and_target_coll(self, arbiter: pymunk.Arbiter, space, data):
        self.targets_to_engage -= 1


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
        print(get_position(box))
        # here too

        pygame.display.flip()
        space.space.step(1/60)
        clock.tick(60)

    pygame.quit()
