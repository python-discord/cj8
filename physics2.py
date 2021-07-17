import math
from typing import Any, List, Tuple
import logging
import pygame

logging.basicConfig(filename="logging.txt", filemode="w", level=logging.INFO)
debug = True

COLLISION_TYPES = {"box_to_target": 0,
                   "object_to_platform": 1,
                   "player_to_box": 2,
                   "box_to_box": 3,
                   "player_to_player": 4,
                   "object_to_border": 5}


class Object(pygame.Rect):
    speed: List[float] = [0, 0]

    def __init__(self, x, y, w, h, upscale: int = 1):
        super().__init__(x, y, w, h)
        self.upscale = upscale

    def get_position(self):
        x, y = self.topleft
        x /= self.upscale
        y /= self.upscale
        return round(x), round(y)


class Space:
    targets: List[Object] = []
    targets_engaged: int = 0
    players: List[Object] = []
    boxes: List[Object] = []
    platforms: List[Object] = []
    thinkingbox: Object = None
    player_on_ground = False
    player_in_thinkingbox = False

    def __init__(self, w: int, h: int, gravity: int, upscale: int = 100):
        self.w = w * upscale
        self.h = h * upscale
        self.gravity = gravity * upscale
        self.upscale = upscale

    def add_object(self, x: int, y: int, w: int, h: int, type: str):
        item = Object(x*self.upscale, y*self.upscale, w*self.upscale, h*self.upscale, upscale=self.upscale)

        if type == "target":
            self.targets.append(item)
        if type == "player":
            self.players.append(item)
        if type == "box":
            self.boxes.append(item)
        if type == "platform":
            self.platforms.append(item)
        if type == "thinkingbox":
            self.thinkingbox = item

        return item

    def check_collisions(self) -> List[Tuple[Object, Any, int]]:
        collisions = []

        def check_list(item1: Object, rect_list: List[Object], collision_type: str):
            item1toitem2_list = item1.collidelistall(rect_list)
            if item1toitem2_list:
                for i in item1toitem2_list:
                    item2 = rect_list[i]
                    collisions.append((item1, item2, COLLISION_TYPES[collision_type]))

                    logging.info(f"{item1} collides with {item2} ({collision_type})")

        def check_borders(item: Object):
            if item.left < 0 or item.right > self.w or item.top < 0 or item.bottom > self.h:
                collisions.append((item, "wall", COLLISION_TYPES["object_to_border"]))

                logging.info(f"{item} collides with a border")

        def check_sametype(itemlist: List[Object], collision_type: str):
            for item1_i, item1 in enumerate(itemlist):
                for item2_i in range(len(itemlist) - (item1_i + 1)):
                    item2_i += (item1_i + 1)
                    item2 = itemlist[item2_i]
                    if item1.colliderect(item2):
                        collisions.append((item1, item2, COLLISION_TYPES[collision_type]))

                        logging.info(f"{item1}, array index: {item1_i},\
                                      collides with a similar object ({collision_type})")

        def check_playerinthinking(p: Object):
            if (player.left > self.thinkingbox.left and player.right < self.thinkingbox.right and
                player.bottom >= self.thinkingbox.bottom and player.top <= self.thinkingbox.top):
                self.player_in_thinkingbox = True

        for box in self.boxes:
            if debug:
                index = 0
                logging.info(f"checking box{index}'s collisions")
                index += 1

            check_list(box, self.targets, "box_to_target")
            check_list(box, self.platforms, "object_to_platform")
            check_borders(box)
        check_sametype(self.boxes, "box_to_box")

        for player in self.players:
            logging.info("checking player collisions")

            check_list(player, self.platforms, "object_to_platform")
            check_list(player, self.boxes, "player_to_box")
            check_borders(player)
            if self.thinkingbox:
                check_playerinthinking(player)
        check_sametype(self.players, "player_to_player")

        return collisions

    def resolve_collisions(self, collisions: List[Tuple[Object, Any, int]]):
        def whatside(collision: Tuple[Object, Object, int], tolerance: int = 31):
            if abs(collision[0].top - collision[1].bottom) < tolerance:
                return "top"
            if abs(collision[0].bottom - collision[1].top) < tolerance:
                return "bottom"
            if abs(collision[0].right - collision[1].left) < tolerance:
                return "right"
            if abs(collision[0].left - collision[1].right) < tolerance:
                return "left"

        for collision in collisions:
            item1 = collision[0]
            item2 = collision[1]
            collision_type = collision[2]

            if debug:
                index = 0
                if item2 != "wall":
                    logging.info(f"resolving collision{index}, {collision}: \n"
                                 f"\t item1 stats: topleft: {item1.topleft}, speed: {item1.speed} \n"
                                 f"\t item2 stats: topleft: {item2.topleft}, speed: {item2.speed}")
                else:
                    logging.info(f"resolving collision{index}, {collision}: \n"
                                 f"\t item1 stats: topleft: {item1.topleft}, speed: {item1.speed}")

            if collision_type == COLLISION_TYPES["box_to_target"]:
                self.targets_engaged += 1

            if collision_type == COLLISION_TYPES["object_to_platform"]:
                side = whatside(collision)
                logging.info(f"collision happened at item1's {side} side")
                if side == "left":
                    item1.speed[0] = 0
                    item1.left = item2.right
                if side == "right":
                    item1.speed[0] = 0
                    item1.right = item2.left
                if side == "top":
                    item1.speed = [item1.speed[0], item1.speed[1]*-1]
                    item1.top = item2.bottom
                if side == "bottom":
                    item1.speed = [0, 0]
                    item1.bottom = item2.top
                    if item1 in self.players:
                        self.player_on_ground = True

            if collision_type == COLLISION_TYPES["player_to_box"]:
                item2.speed = [0, 0]
                side = whatside(collision)
                logging.info(f"collision happened at item1's {side} side")
                if side == "top":
                    item2.bottom = item1.top
                if side == "bottom":
                    item1.speed = [0, 0]
                    item1.bottom = item2.top
                    self.player_on_ground = True
                if side == "left":
                    item2.right = item1.left
                if side == "right":
                    item2.left = item1.right

            if collision_type == COLLISION_TYPES["box_to_box"]:
                alpha_box = item1
                if item2.collidelistall(self.players):
                    alpha_box = item2

                side = whatside(collision)
                logging.info(f"collision happened at item1's {side} side")
                if side == "top":
                    item2.speed = [0, 0]
                    item2.bottom = item1.top
                if side == "bottom":
                    item1.speed = [0, 0]
                    item1.bottom = item2.top
                if side == "left":
                    item1.speed[0] = 0
                    item2.speed[0] = 0
                    if alpha_box is item1:
                        item2.right = item1.left
                    else:
                        item1.left = item2.right
                if side == "right":
                    item1.speed[0] = 0
                    item2.speed[0] = 0
                    if alpha_box is item1:
                        item2.left = item1.right
                    else:
                        item1.right = item2.left

            if collision_type == COLLISION_TYPES["player_to_player"]:
                pass

            if collision_type == COLLISION_TYPES["object_to_border"]:
                if item1.left < 0:
                    item1.speed[0] = 0
                    item1.left = 0
                if item1.right > self.w:
                    item1.speed[0] = 0
                    item1.right = self.w
                if item1.top < 0:
                    item1.speed[1] *= -1
                    item1.top = 0
                if item1.bottom > self.h:
                    item1.speed[1] *= 0
                    item1.bottom = self.h

            if debug:
                if item2 != "wall":
                    logging.info(f"resolved collision{index}, {collision}: \n"
                                 f"\t item1 stats: topleft: {item1.topleft}, speed: {item1.speed} \n"
                                 f"\t item2 stats: topleft: {item2.topleft}, speed: {item2.speed}")
                else:
                    logging.info(f"resolved collision{index}, {collision}: \n"
                                 f"\t item1 stats: topleft: {item1.topleft}, speed: {item1.speed} \n")
                index += 1

    def move_player(self, player: Object, key: str):
        jump_height = 7 * self.upscale
        jump_speed = self.gravity * math.sqrt((jump_height / self.gravity) * 2)
        if key == "up" and self.player_on_ground:
            logging.info(f"moving player up: speed: {player.speed}")
            player.speed[1] = jump_speed * -1
            self.player_on_ground = False
            logging.info(f"moved player up: speed: {player.speed}")
        if key == "down":
            logging.info(f"moving player down: speed: {player.speed}")
            player.speed[1] += jump_speed
            logging.info(f"moving player down: speed: {player.speed}")
        if key == "right":
            player.right += 30
            logging.info(f"moved player right: topleft: {player.topleft}")
        if key == "left":
            player.left -= 30
            logging.info(f"moved player left: topleft: {player.topleft}")

    def step(self, fps: int):
        self.player_in_thinkingbox = False
        self.targets_engaged = 0

        for i in range(len(self.boxes)):
            collisions = self.check_collisions()
            self.resolve_collisions(collisions)

        dynamic_objects = self.players + self.boxes
        # applying gravity to dynamic objects
        for object in dynamic_objects:
            if debug:
                index = 0
                logging.info(f"applying gravity on object{index}: speed: {object.speed}")
            object.speed[1] += (self.gravity / fps)
            if debug:
                logging.info(f"applied gravity on object{index}: speed: {object.speed}")
                index += 1

        # moving objects
        for object in dynamic_objects:
            if debug:
                index = 0
                logging.info(f"moving dynamic_object{index}: topleft: {object.topleft}")

            new_x = round(object.topleft[0] + object.speed[0] * (1 / fps))
            new_y = round(object.topleft[1] + object.speed[1] * (1 / fps))
            object.topleft = new_x, new_y

            if debug:
                logging.info(f"moved dynamic_object{index}: topleft: {object.topleft}")
                index += 1

    def reset(self):
        self.targets = []
        self.targets_engaged = 0
        self.players = []
        self.boxes = []
        self.platforms = []
        self.thinkingbox = None
        self.player_on_ground = False
        self.player_in_thinkingbox = False
