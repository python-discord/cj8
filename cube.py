#!/usr/bin/env python
# coding: utf-8

import time
from typing import Dict, List

import numpy as np
from asciimatics.event import KeyboardEvent, MouseEvent
from asciimatics.screen import ManagedScreen, Screen


# define rotation matrices
def Rx(theta: np.float32) -> np.matrix:
    """Rotation by theta around x axis."""
    return np.matrix(
        [
            [1, 0, 0],
            [0, np.cos(theta), np.sin(theta)],
            [0, -np.sin(theta), np.cos(theta)],
        ]
    )


def Ry(theta: np.float32) -> np.matrix:
    """Rotation by theta around y axis."""
    return np.matrix(
        [
            [np.cos(theta), 0, -np.sin(theta)],
            [0, 1, 0],
            [np.sin(theta), 0, np.cos(theta)],
        ]
    )


def Rz(theta: np.float32) -> np.matrix:
    """Rotation by theta around z axis."""
    return np.matrix(
        [
            [np.cos(theta), np.sin(theta), 0],
            [-np.sin(theta), np.cos(theta), 0],
            [0, 0, 1],
        ]
    )


# 3d to 2d projection
def project3d(
    point: np.array,  # the 3D point to turn into a 2D point
    camera_position: np.array = np.array([0, 0, 5]),
    camera_x: np.array = np.array([1, 0, 0]),  # "what is right"
    camera_y: np.array = np.array([0, 1, 0]),  # "what is up"
    camera_z: np.array = np.array(
        [0, 0, -1]
    ),  # must be negative cross product of camera_x and camera_y,
    # "what is forward"
) -> np.array:
    """Project a point in 3 space onto 2D coordinates for screen.

    Take a 3D point and project it into 2D to draw it, by using a
    camera given via its position vector and a "camera coordinate
    system": The vector camera_z is (the unit vector) where the camera
    is pointed (say toward the scene, which may be centered about the
    origin), and camera_x and camera_y are unit vectors to define what
    is "to the right" and "up". They should be orthogonal, and
    camera_z their (negative) cross-product.
    """
    # compute point P on perspective plane:
    if np.abs(camera_z.dot(point - camera_position)) < 1e-6:
        # camera to point directon is orthogonal to camera view direction, so no point of intersection
        return None
    P = (
        1 / camera_z.dot(point - camera_position) * (point - camera_position)
        + camera_position
    )
    x, y = P.dot(camera_x), P.dot(camera_y)
    return np.array([x, y])


class Artist:
    """A dummy class providing a 3D drawing interface."""

    def __init__(
        self,
        screen: Screen,
        camera_position: np.array = np.array([0, 0, 5]),
        camera_x: np.array = np.array([1, 0, 0]),  # "what is right"
        camera_y: np.array = np.array([0, 1, 0]),  # "what is up"
        camera_z: np.array = np.array(
            [0, 0, -1]
        ),  # must be negative cross product of camera_x and camera_
    ):
        """Initialise the screen drawing artist."""
        self.screen = screen
        self.h = screen.height
        self.w = screen.width
        self.cx = self.w / 2
        self.cy = self.h / 2

        self.camera_position = camera_position
        self.camera_x = camera_x
        self.camera_y = camera_y
        self.camera_z = camera_z

    def line(self, pt1: np.array, pt2: np.array) -> None:
        """Draw a line from pt1 to pt2."""
        x, y = project3d(
            pt1,
            camera_position=self.camera_position,
            camera_x=self.camera_x,
            camera_y=self.camera_y,
            camera_z=self.camera_z,
        )
        x = self.cx * (1 + x)
        y = self.cy * (1 + y)
        self.screen.move(x, y)
        x, y = project3d(
            pt2,
            camera_position=self.camera_position,
            camera_x=self.camera_x,
            camera_y=self.camera_y,
            camera_z=self.camera_z,
        )
        x = self.cx * (1 + x)
        y = self.cy * (1 + y)
        self.screen.draw(x, y)

    def fill_polygon(self, polygons: List[List[np.array]], colour: int) -> None:
        """Draw a filled polygon of the given colour. Coordinates are 3D."""

        def proj(pt: np.array) -> np.array:
            """Convert 3D coordinates to 2D screen coordinates."""
            x, y = project3d(
                pt,
                camera_position=self.camera_position,
                camera_x=self.camera_x,
                camera_y=self.camera_y,
                camera_z=self.camera_z,
            )
            return np.array([self.cx * (1 + x), self.cy * (1 + y)])

        self.screen.fill_polygon(
            [[proj(pt) for pt in poly] for poly in polygons], colour
        )


class BaseCube:
    """A 1x1 cube centred at the origin. It has coloured faces but doesn't do much otherwise."""

    def __init__(
        self,
        colours: Dict[str, int] = {
            "front": Screen.COLOUR_MAGENTA,
            "back": Screen.COLOUR_RED,
            "left": Screen.COLOUR_BLUE,
            "right": Screen.COLOUR_GREEN,
            "top": Screen.COLOUR_CYAN,
            "bottom": Screen.COLOUR_YELLOW,
        },
    ):
        # define corner points of front face and back face, starting in top left, going clockwise
        front = [
            np.array(
                [-1, 1, 1]
            ),  # (x,y,z) coordinates of each point, z is 1 for all front points
            np.array([1, 1, 1]),
            np.array([1, -1, 1]),
            np.array([-1, -1, 1]),
        ]
        back = [
            np.array([-1, 1, -1]),
            np.array([1, 1, -1]),
            np.array([1, -1, -1]),
            np.array([-1, -1, -1]),
        ]
        front = [pt / 2 for pt in front]  # make the cubes side lengths equal to one
        back = [pt / 2 for pt in back]
        self.front = front
        self.back = back
        self.normal_vectors = {
            "front": [0, 0, 1],
            "back": [0, 0, -1],
            "left": [-1, 0, 0],
            "right": [1, 0, 0],
            "top": [0, 1, 0],
            "bottom": [0, -1, 0],
        }
        self.colours = colours

    def draw_cage(self, artist: Artist) -> None:
        """Draw self as wireframe using artist."""
        for pt1, pt2 in zip(self.front, [*self.front[1:], self.front[0]]):
            artist.line(pt1, pt2)
        for pt1, pt2 in zip(self.back, [*self.back[1:], self.back[0]]):
            artist.line(pt1, pt2)
        for pt1, pt2 in zip(self.front, self.back):
            artist.line(pt1, pt2)

    def draw_block_faces(self, artist: Artist) -> None:
        """Draw self with solid colored faces using artist."""
        camera_direction = artist.camera_position

        # front
        if np.inner(camera_direction, self.normal_vectors["front"]) > 0:
            artist.fill_polygon(
                [
                    self.front,
                ],
                self.colours["front"],
            )
        # back
        if np.inner(camera_direction, self.normal_vectors["back"]) > 0:
            artist.fill_polygon(
                [
                    self.back[::-1],
                ],
                self.colours["back"],
            )
        # left
        if np.inner(camera_direction, self.normal_vectors["left"]) > 0:
            artist.fill_polygon(
                [
                    [
                        self.front[0],
                        self.back[0],
                        self.back[2],
                        self.front[2],
                    ]
                ],
                self.colours["left"],
            )
        # right
        if np.inner(camera_direction, self.normal_vectors["right"]) > 0:
            artist.fill_polygon(
                [
                    [
                        self.front[1],
                        self.front[3],
                        self.back[3],
                        self.back[1],
                    ]
                ],
                self.colours["right"],
            )
        # top
        if np.inner(camera_direction, self.normal_vectors["top"]) > 0:
            artist.fill_polygon(
                [
                    [
                        self.front[0],
                        self.front[1],
                        self.back[1],
                        self.back[0],
                    ]
                ],
                self.colours["top"],
            )
        # bottom
        if np.inner(camera_direction, self.normal_vectors["bottom"]) > 0:
            artist.fill_polygon(
                [
                    [
                        self.front[2],
                        self.front[3],
                        self.back[3],
                        self.back[2],
                    ]
                ],
                self.colours["bottom"],
            )


class TranslatedCube(BaseCube):
    """A base cube that is shifted into a new location."""

    def __init__(self, position: np.array = np.array([0, 0, 0])):
        """Initialise translated cube."""
        super().__init__()
        self.position = position
        self.front = [pt + position for pt in self.front]
        self.back = [pt + position for pt in self.back]


class GenericCube(TranslatedCube):
    """A translated cube that can subsequently be rotated around the x, y, or z axis."""

    def __rotation_update__(self, R: np.matrix) -> None:
        """Multiply each point in this object by rotation matrix R."""
        self.front = [R.dot(pt).getA1() for pt in self.front]
        self.back = [R.dot(pt).getA1() for pt in self.back]
        self.position = R.dot(self.position).getA1()
        self.normal_vectors = {
            face: R.dot(normal).getA1() for face, normal in self.normal_vectors.items()
        }

    def rotate_x(self, theta: np.float32) -> None:
        """Rotate entire object around x axis by angle theta [radians]."""
        R = Rx(theta)
        self.__rotation_update__(R)

    def rotate_y(self, theta: np.float32) -> None:
        """Rotate entire object around z axis by angle theta [radians]."""
        R = Ry(theta)
        self.__rotation_update__(R)

    def rotate_z(self, theta: np.float32) -> None:
        """Rotate entire object around z axis by angle theta [radians]."""
        R = Rz(theta)
        self.__rotation_update__(R)


if __name__ == "__main__":

    distance_to_camera = 6

    @ManagedScreen
    def main_event_loop(screen: Screen = None) -> None:
        """The main event loop that redraws the screen and takes user input."""
        # create an artist to draw the individual cubes
        artist = Artist(
            screen,
            camera_position=np.array([0, 0, distance_to_camera]),
        )

        # the Rubik cube is made up of 26 individual cubes
        rubik_cube = [
            GenericCube(np.array([x, y, z]))
            # Generate cubes from fron to back, top to bottom, left to
            # right. The first one is front top left corner.
            for z in [1, 0, -1]
            for y in [1, 0, -1]
            for x in [-1, 0, 1]
            if x or y or z
        ]

        ### DEBUG: restrict to 2 cubes for easier troubleshooting:
        # rubik_cube = [rubik_cube[0], rubik_cube[-1]]

        last_time = time.time_ns()
        key, mouse_x, mouse_y, mouse_buttons = 0, 0, 0, 0
        distance = 0
        camera_2d = np.array([0, 0])
        start_pos = np.array([0, 0])
        while True:
            ev = screen.get_event()
            if isinstance(ev, KeyboardEvent):
                key = ev.key_code
                # Stop on ctrl+q or ctrl+x, or simply on q/Q
                if key in (17, 24, ord("Q"), ord("q")):
                    # raise StopApplication("User terminated app")
                    return
                elif key == ord("f"):  # rotate front disc counter-clockwise
                    # the "front" are the first 9 cubes in the list
                    for cube in rubik_cube[:9]:
                        cube.rotate_z(
                            np.pi / 2
                        )  # rotate the cube by 90 degrees to the left
                        # (counter-clockwise), this should be animated and the
                        # animation non-interruptable; omit animation for now
                    # re-arrange the cubes, so that the meaning of the interval positions remains the same
                    rubik_cube = [
                        rubik_cube[2],
                        rubik_cube[5],
                        rubik_cube[8],
                        rubik_cube[1],
                        rubik_cube[4],
                        rubik_cube[7],
                        rubik_cube[0],
                        rubik_cube[3],
                        rubik_cube[6],
                        *rubik_cube[9:],
                    ]
                elif key == ord("F"):  # rotate front disc clockwise
                    # the "front" are the first 9 cubes in the list
                    for cube in rubik_cube[:9]:
                        cube.rotate_z(
                            -np.pi / 2
                        )  # rotate the cube by -90 degrees to the left (=90 to the right)
                        # (clockwise), this should be animated and the
                        # animation non-interruptable; omit animation for now
                    # re-arrange the cubes, so that the meaning of the interval positions remains the same
                    rubik_cube = [
                        rubik_cube[6],
                        rubik_cube[3],
                        rubik_cube[0],
                        rubik_cube[7],
                        rubik_cube[4],
                        rubik_cube[1],
                        rubik_cube[8],
                        rubik_cube[5],
                        rubik_cube[2],
                        *rubik_cube[9:],
                    ]

            elif isinstance(ev, MouseEvent):
                mouse_x, mouse_y, mouse_buttons = ev.x, ev.y, ev.buttons
                if mouse_buttons:
                    start_pos = np.array([mouse_x, mouse_y])
                else:
                    end_pos = np.array([mouse_x, mouse_y])

                    camera_2d += end_pos - start_pos
                    camera_2d_normalised = (
                        camera_2d / max(screen.width, screen.height) * np.pi
                    )
                    alpha, beta = camera_2d_normalised

                    R = Ry(alpha) @ Rx(beta)
                    camera_x = (R @ np.array([1, 0, 0])).getA1()
                    camera_y = (R @ np.array([0, 1, 0])).getA1()
                    camera_z = -(R @ np.array([0, 0, 1])).getA1()

                    artist.camera_position = -camera_z * distance_to_camera
                    artist.camera_x = camera_x
                    artist.camera_y = camera_y
                    artist.camera_z = camera_z

            current_time = time.time_ns()
            frames_per_second = 1e9 / (current_time - last_time)
            last_time = current_time

            screen.clear_buffer(0, 0, 0)
            screen.print_at(
                f"""{screen.width=}, {screen.height=}, {len(rubik_cube)=}
{frames_per_second=:5.1f} {key=:4d} {mouse_x=:4d}, {mouse_y=:4d} {mouse_buttons=} {distance=:5.1f}""",
                0,
                0,
            )
            screen.print_at(
                "Press q/Q to quit, f/F to rotate front disc, drag the mouse for rotation of the cube.",
                0,
                3,
            )

            def cube_camera_distance(cube: TranslatedCube) -> np.float32:
                """Return distance of cube centre point to the camera."""
                return np.linalg.norm(artist.camera_position - cube.position)

            # draw each individual cube, start with those furthest away from the camera:
            for cube in sorted(rubik_cube, key=cube_camera_distance, reverse=True):
                cube.draw_block_faces(artist)
                # cube.draw_cage(artist)

            screen.refresh()

    main_event_loop()
