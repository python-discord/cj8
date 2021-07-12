#!/usr/bin/env python
# coding: utf-8

import copy
import math
# import numpy as np
from asciimatics.screen import ManagedScreen
from time import sleep

COLOUR_BLACK = 0
COLOUR_RED = 1
COLOUR_GREEN = 2
COLOUR_YELLOW = 3
COLOUR_BLUE = 4
COLOUR_MAGENTA = 5
COLOUR_CYAN = 6
COLOUR_WHITE = 7
CUBE_SIZE = 3


# define point class
class Point:
    """A class to hold the points"""
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    def __repr__(self) -> tuple:
        """A useless thing that exists"""
        return self.x, self.y, self.z
    
    def position(self, x_mul, y_mul) -> tuple:
        """Return the position multiplied by the position multiplier"""
        return self.x * x_mul, self.y * y_mul
    
    def __str__(self) -> str:
        """Return the X Y Z coords as a string"""
        return f"X:{self.x}, Y:{self.y}, Z:{self.z}"


class Cube:
    """A class to create the cube"""
    def __init__(self, screen):
        """Define all the variables for the cube"""
        
        self.screen = screen
        self.h = screen.height
        self.w = screen.width
        
        self.cx = self.w / 3
        self.cy = self.h / 1.5
        self.cz = 0
        self.size = self.h / 3

        self.time_delta = 0
        self.time_last = 0

        self.rotate_mode = False
        self.rotate_start_x = None
        self.rotate_start_y = None

        self.size_list_x = [
            self.cx - self.size,
            self.cx - self.size + self.size/1.5,
            self.cx + self.size - self.size/1.5,
            self.cx + self.size
        ]
        self.size_list_y = [
            self.cy - self.size,
            self.cy - self.size + self.size/1.5,
            self.cy + self.size - self.size/1.5,
            self.cy + self.size
        ]
        self.size_list_z = [
            self.cz - self.size,
            self.cz - self.size + self.size/1.5,
            self.cz + self.size - self.size/1.5,
            self.cz + self.size
        ]

        self.block_faces = [
            self.create_face(3, self.size_list_y, self.size_list_z, 'x', self.cx+self.size, 1),
            self.create_face(3, self.size_list_y, self.size_list_z, 'x', self.cx-self.size, 2),
            self.create_face(3, self.size_list_x, self.size_list_z, 'y', self.cy+self.size, 3),
            self.create_face(3, self.size_list_x, self.size_list_z, 'y', self.cy-self.size, 4),
            self.create_face(3, self.size_list_x, self.size_list_y, 'z', self.cz+self.size, 5),
            self.create_face(3, self.size_list_x, self.size_list_y, 'z', self.cz-self.size, 6),
        ]
    
    @staticmethod
    def create_face(n, size_list_1, size_list_2, stable_type, stable_value, color):

        if stable_type == 'x':
            face = []
            for i in range(n**2):
                block = [
                    Point(stable_value, size_list_1[i//n], size_list_2[i % n]),
                    Point(stable_value, size_list_1[i//n], size_list_2[i % n+1]),
                    Point(stable_value, size_list_1[i//n+1], size_list_2[i % n+1]),
                    Point(stable_value, size_list_1[i//n+1], size_list_2[i % n]),
                ]
                face.append(block)
            face.append(color)
            return face
        if stable_type == 'y':
            face = []
            for i in range(n**2):
                block = [
                    Point(size_list_1[i//n], stable_value, size_list_2[i % n]),
                    Point(size_list_1[i//n], stable_value, size_list_2[i % n+1]),
                    Point(size_list_1[i//n+1], stable_value, size_list_2[i % n+1]),
                    Point(size_list_1[i//n+1], stable_value, size_list_2[i % n]),
                ]
                face.append(block)
            face.append(color)
            return face
        if stable_type == 'z':
            face = []
            for i in range(n**2):
                block = [
                    Point(size_list_1[i//n], size_list_2[i % n], stable_value),
                    Point(size_list_1[i//n], size_list_2[i % n+1], stable_value),
                    Point(size_list_1[i//n+1], size_list_2[i % n+1], stable_value),
                    Point(size_list_1[i//n+1], size_list_2[i % n], stable_value),
                ]
                face.append(block)
            face.append(color)
            return face
    
    def draw_block_faces(self, faces):
        for face in faces:
            for block in face[:-1]:
                self.actually_draw_faces(block, face[-1])
    
    def define_rotation_parts(self, faces, n):
        print(n)
        x_rotation = []
        for block in faces[0][:-1]:
            x_rotation.extend(block)
        for face in faces[1:]:
            for block in face[:-1]:
                if self.size_list_z[1] in tuple(block):
                    x_rotation.extend(block)
        self.rotate_z(1, x_rotation)
    
    def main_loop(self):
        time_now = 0
        while True:
            self.time_delta = time_now - self.time_last
            self.time_last = time_now

            self.check_event()
            # self.draw_faces()
            # self.draw()
            self.decide_face_order()
            self.screen.refresh()
            self.screen.clear_buffer(0, 0, 0)
            sleep(0.1)
            time_now += 100

    def check_event(self):
        event = str(self.screen.get_event())
        event_sep = event.split(' ')

        if event_sep[0] == 'MouseEvent':
            pos_x = int((event_sep[1].replace('(', '')).replace(',', ''))
            pos_y = int(event_sep[2].replace(')', ''))
            button_click = int(event_sep[-1])

            if button_click == 1:
                self.rotate_mode = True
                self.rotate_start_x = pos_x
                self.rotate_start_y = pos_y
            
            if self.rotate_mode:
                # dx = self.rotate_start_x + pos_x
                # dy = self.rotate_start_y + pos_y
                pass
            if button_click == 2:
                self.rotate_mode = False

            self.screen.print_at(event_sep[-1], 0, 0)
        elif event_sep[0] == 'KeyboardEvent:':
            if event_sep[1] == "-203":
                self.rotate_whole(0, -0.2, 0, self.block_faces)
            elif event_sep[1] == "-204":
                self.rotate_whole(0.2, 0, 0, self.block_faces)
            elif event_sep[1] == "-205":
                self.rotate_whole(0, 0.2, 0, self.block_faces)
            elif event_sep[1] == "-206":
                self.rotate_whole(-0.2, 0, 0, self.block_faces)
                self.define_rotation_parts(self.block_faces, 1)
            elif event_sep[1] == "0":
                pass

    def decide_face_order(self):
        temp = copy.deepcopy(self.block_faces)
        temp.sort(key=self.find_z_value)
        self.draw_block_faces(temp)

    def actually_draw_faces(self, points, color):
        xmul = 1.5
        ymul = 0.75
        print(str(points[0]))
        self.screen.fill_polygon([[
            points[0].position(xmul, ymul), 
            points[1].position(xmul, ymul), 
            points[2].position(xmul, ymul), 
            points[3].position(xmul, ymul),  
        ], [
            (0, 0),
            (0, 0),
            (0, 0),
            (0, 0),
        ]], color)
        self.actually_draw_outline(points)

    def actually_draw_outline(self, block):
        for i in range(3):
            self.screen.move(block[i].x*1.5, block[i].y * 0.75)
            self.screen.draw(block[i+1].x*1.5, block[i+1].y * 0.75)
        self.screen.move(block[3].x*1.5, block[3].y * 0.75)
        self.screen.draw(block[0].x*1.5, block[0].y * 0.75)

    @staticmethod
    def find_z_value(face):
        maximum = -1e5
        for block in face[:-1]:
            temp = max(block[0].z, block[1].z, block[2].z, block[3].z)
            if temp > maximum:
                maximum = temp
        return maximum

    def rotate_whole(self, x, y, z, faces):
        for face in faces:
            for block in face[:-1]:
                self.rotate_x(x, block)
                self.rotate_y(y, block)
                self.rotate_y(z, block)

    def rotate_z(self, amount, vertices):
        angle = self.time_delta * 0.001 * amount * math.pi * 2
        for v in vertices:
            dx = v.x - self.cx
            dy = v.y - self.cy
            x = dx * math.cos(angle) - dy * math.sin(angle)
            y = dx * math.sin(angle) + dy * math.cos(angle)
            v.x = x + self.cx
            v.y = y + self.cy

    def rotate_x(self, amount, vertices):
        angle = self.time_delta * 0.001 * amount * math.pi * 2
        for v in vertices:
            dy = v.y - self.cy
            dz = v.z - self.cz
            y = dy * math.cos(angle) - dz * math.sin(angle)
            z = dy * math.sin(angle) + dz * math.cos(angle)
            v.y = y + self.cy
            v.z = z + self.cz

    def rotate_y(self, amount, vertices):
        angle = self.time_delta * 0.001 * amount * math.pi * 2
        for v in vertices:
            dx = v.x - self.cx
            dz = v.z - self.cz
            x = dz * math.sin(angle) + dx * math.cos(angle)
            z = dz * math.cos(angle) - dx * math.sin(angle)
            v.x = x + self.cx
            v.z = z + self.cz


@ManagedScreen
def demo(screen=None):
    cube = Cube(screen)
    cube.main_loop()


demo()
