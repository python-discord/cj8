#!/usr/bin/env python
# coding: utf-8

from time import sleep

import numpy as np
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

    The angles alpha and beta are supposed to define the field of view
    in radians. Not happy with that yet.

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


class BaseCube:
    """A 1x1 cube centred at the origin."""

    def __init__(self):
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

    def draw_cage(self, artist: Artist) -> None:
        """Draw self using artist."""
        for pt1, pt2 in zip(self.front, [*self.front[1:], self.front[0]]):
            artist.line(pt1, pt2)
        for pt1, pt2 in zip(self.back, [*self.back[1:], self.back[0]]):
            artist.line(pt1, pt2)
        for pt1, pt2 in zip(self.front, self.back):
            artist.line(pt1, pt2)


class TranslatedCube(BaseCube):
    """A base cube that is shifted into a new location."""

    def __init__(self, position: np.array):
        """Initialise translated cube."""
        super().__init__()
        # self.position = position
        self.front = [pt + position for pt in self.front]
        self.back = [pt + position for pt in self.back]


class GenericCube(TranslatedCube):
    """A translated cube that can subsequently be rotated around the x, y, or z axis."""

    # def __init__(self, position; np.array):
    #     super().__init__(position)
    #     # this is an alternative: keep record of the orientation of
    #     # the entire cube and change that rather than updating each
    #     # individual corner point:
    #     self.orientation_x = np.array([1,0,0])
    #     self.orientation_y = np.array([0,1,0])
    #     self.orientation_z = self.orientation_x.cross(self.orientation_y)
    def __rotation_update__(self, R: np.matrix) -> None:
        """Multiply each point in this object by rotation matrix R."""
        self.front = [R.dot(pt).getA1() for pt in self.front]
        self.back = [R.dot(pt).getA1() for pt in self.back]

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

    @ManagedScreen
    def demo(screen: Screen = None) -> None:
        """Maybe this one doesn't need a description."""
        # create an artist to draw the individual cubes
        artist = Artist(
            screen,
            camera_position=np.array([0.2, 0.4, 7]),
        )

        # the Rubik cube is made up of 26 individual cubes
        rubik_cube = [
            GenericCube(np.array([x, y, z]))
            for x in [-1, 0, 1]
            for y in [-1, 0, 1]
            for z in [-1, 0, 1]
            if np.linalg.norm([x, y, z]) > 1e-5  # exclude the center cube
        ]
        screen.print_at(
            f"Resolution: {screen.width=} x {screen.height=}, {len(rubik_cube)=}", 0, 0
        )

        # draw each individual cube:
        for cube in rubik_cube:
            cube.draw_cage(artist)

        screen.refresh()
        sleep(1/2)

        for steps in range(90):  # 90 steps of 1 degree rotations

            # rotate left most disc
            for cube in rubik_cube[:9]:
                cube.rotate_x(np.pi/180 * 1)  # 1 degree

            screen.clear_buffer(0, 0, 0)
            for cube in rubik_cube:
                cube.draw_cage(artist)

            screen.refresh()
            sleep(1/30)

    demo()
