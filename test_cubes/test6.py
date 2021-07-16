import time
import numpy as np
import math
from asciimatics.screen import ManagedScreen
import traceback

def leng(v):
    return (v**2).sum()**.5

def limit(bot,top,val):
    return min(max(val,bot),top)
    
def z_depth(source):
    def wrap(face : Face):
        return max([leng(p-source) for p in face.vertices])
    return wrap

def Rx(theta: np.float32) -> np.matrix:
    "rotation by theta around x axis"
    return np.matrix(
        [
            [1, 0, 0],
            [0, np.cos(theta), np.sin(theta)],
            [0, -np.sin(theta), np.cos(theta)],
        ]
    )


def Ry(theta: np.float32) -> np.matrix:
    "rotation by theta around y axis"
    return np.matrix(
        [
            [np.cos(theta), 0, -np.sin(theta)],
            [0, 1, 0],
            [np.sin(theta), 0, np.cos(theta)],
        ]
    )


def Rz(theta: np.float32) -> np.matrix:
    "rotation by theta around z axis"
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
    """
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
        screen,
        camera_position: np.array = np.array([0, 0, 5],dtype=float),
        camera_x: np.array = np.array([1, 0, 0]),  # "what is right"
        camera_y: np.array = np.array([0, 1, 0]),  # "what is up"
        camera_z: np.array = np.array(
            [0, 0, -1]
        ),  # must be negative cross product of camera_x and camera_
        scale = 50,
        yscale = .5
    ):
        self.screen = screen
        self.h = screen.height
        self.w = screen.width
        self.cx = self.w / 2
        self.cy = self.h / 2

        self.camera_position = camera_position
        self.camera_x = camera_x
        self.camera_y = camera_y
        self.camera_z = camera_z
        self.scale = scale
        self.yscale = yscale

    def line(self, pt1: np.array, pt2: np.array):
        "draw a line from pt1 to pt2"
        x, y = project3d(
            pt1,
            camera_position=self.camera_position,
            camera_x=self.camera_x,
            camera_y=self.camera_y,
            camera_z=self.camera_z,
        )
        x,y = self.resize(x,y)
        self.screen.move(x, y)
        x, y = project3d(
            pt2,
            camera_position=self.camera_position,
            camera_x=self.camera_x,
            camera_y=self.camera_y,
            camera_z=self.camera_z,
        )
        x,y = self.resize(x,y)
        self.screen.draw(x, y)
    
    def polygon(self,pts,color = 0):
        self.screen.fill_polygon([[
            self.resize(*project3d(
                p,
                camera_position=self.camera_position,
                camera_x=self.camera_x,
                camera_y=self.camera_y,
                camera_z=self.camera_z,
            )) for p in pts
        ],[
            [(0, 0)]*4
        ]], color)
        
    def resize(self,x,y):
        x = x*self.scale + self.cx
        y = y*self.yscale*self.scale + self.cy
        return x,y

faces = [[0,1,2,3],[4,5,6,7],[0,1,4,5],[2,3,6,7],[0,2,4,6],[1,3,5,7]]
face_draw_indices = [0,1,3,2]
edges = [
    [0,1],[0,2],[0,4],
    [1,3],[1,5],
    [2,3],[2,6],
    [3,7],
    [4,5],[4,6],
    [5,7],
    [6,7]
]

directions = [np.array([x,y,z],dtype=float) for x in (-1,0,1) for y in(-1,0,1) for z in (-1,0,1) if bool(x) ^ bool(y) ^ bool(z) and not(x and y and z)]

whole_rotate = {'-203':(-1,0),'-204':(0,1),'-205':(1,0),'-206':(0,-1)}
rotate_side = {'r':0,'d':1,'f':2,'b':3,'u':4,'l':5}

data = {'time':0,'to_print':'running...','last_update':time.time()}
PI2 = math.pi * 2

class RubikCube:
    def __init__(self,artist : Artist):
        self.cubices = [Cube(np.array([x,y,z]),1) for x in range(-1,2) for y in range(-1,2) for z in range(-1,2)]
        self.artist = artist
        self.rotation = np.zeros(2)
        data['to_print'] = []
    
    
    def draw(self):
        faces = []
        for cube in self.cubices:
            faces.extend(cube.get_faces())
        
        for face in faces:
            for i in range(4):
                vertex = face.vertices[i]
                vertex = Ry(self.rotation[0]).dot(vertex).getA1()
                vertex = Rx(self.rotation[1]).dot(vertex).getA1()
                face.vertices[i] = vertex

        sorted_faces = sorted(faces,key=z_depth(self.artist.camera_position),reverse=True)
        for face in sorted_faces:
            self.artist.polygon(face.vertices,face.color)
            for i in range(4):
                j = (i+1)%4
                self.artist.line(face.vertices[i],face.vertices[j])

    def update(self):
        self.poll_events()
        self.draw()

    def poll_events(self):
        event = self.artist.screen.get_event()
        while event:
            event = str(event)
            event_sep = event.split()
            if event_sep[0] == 'KeyboardEvent:':
                #data['to_print'] = event_sep
                if event_sep[1] in whole_rotate:
                    self.rotate_whole(*whole_rotate[event_sep[1]])
                else:
                    c = chr(int(event_sep[1]))
                    data['to_print'] = 'input: ' + c
                    if c.lower() in rotate_side:
                        self.rotate(rotate_side[c.lower()],c == c.lower())
                
            event = self.artist.screen.get_event()

    def rotate_whole(self,x,y):
        self.rotation -= np.array([x,y],dtype=float) * (time.time()-data['last_update']) * 3

    def rotate(self,side=0,clockwise = True):
        cube = self.cubices[13]
        faces = cube.get_faces()
        d = directions[side]
        min_angle = 180
        for i,face in enumerate(faces):
            for j in range(4):
                vertex = face.vertices[j]
                vertex = Ry(self.rotation[0]).dot(vertex).getA1()
                vertex = Rx(self.rotation[1]).dot(vertex).getA1()
                face.vertices[j] = vertex
            angle = face.angle(-d)
            if angle < min_angle:
                min_face = i
                min_angle = angle
        vec = cube.get_faces()[min_face].vector()

        mul = 90 * [1,-1][clockwise]
        for cube in self.cubices:
            if abs(cube.pos.dot(vec).sum() - 1) < .1:
                cube.rotate(*vec*mul)

class Face:
    def __init__(self,vertices,color,parent):
        self.vertices = [vertices[face_draw_indices[i]] for i in range(4)]
        self.color = color
        self.parent = parent
    
    def vector(self):
        vec = np.zeros(3)
        for vertex in self.vertices:
            vec += vertex
        return vec/2
    
    def angle(self,vec2):
        vec = self.vector()
        return math.acos(limit(-1,1,vec.dot(vec2)/(leng(vec)*leng(vec2))))

class Cube:
    def __init__(self, pos : np.ndarray, size : float, colors = list(range(1,7))):
        self.pos = pos
        self.fixed_pos = pos.copy()
        self.size = size
        self.rotation = np.array([0,0,0],dtype=float)
        self.colors = colors
        self.update(0,0,0)
    
    def rotate(self,x,y,z):
        self.rotation += np.array([x,y,z])
        self.update(x,y,z)
        self.rotation[self.rotation>=360] -= 360

    def update(self,rx,ry,rz):
        self.pos = Rx(math.radians(rx)).dot(self.pos).getA1()
        self.pos = Ry(math.radians(ry)).dot(self.pos).getA1()
        self.pos = Rz(math.radians(rz)).dot(self.pos).getA1()

        vertices = [np.array([x-.5,y-.5,z-.5])*self.size for x in range(2) for y in range(2) for z in range(2)]
        
        for i in range(len(vertices)):
            vertex = vertices[i]
            vertex = Rx(math.radians(self.rotation[0])).dot(vertex).getA1()
            vertex = Ry(math.radians(self.rotation[1])).dot(vertex).getA1()
            vertex = Rz(math.radians(self.rotation[2])).dot(vertex).getA1()
            vertices[i] = vertex+self.pos
        
        self.vertices = vertices
    
    def get_faces(self):
        vertices = self.vertices
        return [Face([vertices[j] for j in face],self.colors[i],self) for i,face in enumerate(faces)]
    
    def set_color(self,color,index):
        self.colors[index] = color
                
        


def main():
    @ManagedScreen
    def demo(screen=None):
        # create an artist to draw the individual cubes
        artist = Artist(
            screen,
            camera_position=np.array([0, 0, 50],dtype=float),
            scale=550
        )

        cube = RubikCube(artist)

        while True:
            data['time'] = time.time()
            screen.clear_buffer(0, 0, 0)
            screen.print_at(data['to_print'], 0, 0)
            cube.update()
            data['last_update'] = time.time()
            screen.refresh()
            time.sleep(limit(.02,.2,.2-time.time()-data['time']))
            
            
    demo()
    
try:
    print('program start')
    main()
except:
    print(traceback.format_exc())
    input()
print('program end')