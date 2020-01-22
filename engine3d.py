import pygame
from pygame import gfxdraw
import numpy as np
import sys
import time
import math
import copy

screen_size = 1200, 1200
fov = 450
bgc = (0,0,0)
cv = int(screen_size[0]/2), int(screen_size[1]/2)


class Vec3d(object):

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z

    def __repr__(self):
        return f"Vec3d({self.x}, {self.y}, {self.z})"

class Object3d(object):

    def __init__(self, pos: Vec3d=Vec3d(0,0,0), color=(255,0,255), size: Vec3d=Vec3d(0.5,0.5,0.5)):
        self.pos = copy.copy(pos)
        self.color =  copy.copy(color)

        self.verts, self.edges, self.faces = self.setup_shape()
        self.set_size(size)
    
    def join(self, o):
        """
        o must be this class instance
        """
        l = len(self.verts)
        
        for v in o.verts:
            self.verts.append(Vec3d(v.x+o.pos.x, v.y+io))   
        for e in o.edges:
            self.edges.append((e[0]+l, e[1]+l))
        return self

        
    def setup_shape(self):
        verts = [Vec3d(x, y , z) for x in (-1, 1) for y in (-1, 1) for z in (-1, 1)]
        edges = [
            (0, 4), (0, 1), (0, 2),
            (6, 4), (6, 2), (6, 7),
            (7, 5), (7, 3), (3, 2),
            (1, 3), (1, 5), (5, 4)
        ]

        faces = None #todo

        return verts, edges, faces

    def set_size(self, size: Vec3d):
        for idx, (x,y,z) in enumerate(self.verts):
            self.verts[idx] = Vec3d(x*size.x, y*size.y, z*size.z)

    
    def rotate(self, angle):
        # as the challange is not to check internet at all
        # i needed to reinvent this, good i still remember much stuff from
        # math classes
        ax,ay,az = angle        
        axs,axc = math.sin(ax), math.cos(ax)
        ays,ayc = math.sin(-ay), math.cos(-ay)
        azs,azc = math.sin(az), math.cos(az)
        #TODO matrixes + numpy/numba
        for idx, (x,y,z) in enumerate(self.verts):
            if ax != 0:                
                z, y = z * axc - y * axs, z * axs + y * axc                 
            if ay != 0:
                z, x = z * ayc - x * ays, z * ays + x * ayc                      
            if az != 0:
                x, y = x * azc - y * azs, x * azs + y * azc
            self.verts[idx] = Vec3d(x,y,z)
        return self
        


class Camera3d(object):
    

    def __init__(self, pos :Vec3d=Vec3d(0,0,-5), angle=(0, math.pi/2), fov=1200):
        
        self.pos = copy.copy(pos)
        self.fov = fov
        self.show_verts = True
        self.show_edges = True
        self.show_faces = False #TBD
        self.angle = angle # to be implemented ;)

    def project(self, o: Object3d, vert: Vec3d):
        """
        verts just a triple i coultn't find more elegant way atm :(
        """                 
        _x, _y, _z = o.pos        
        x,y,z = -_x+vert.x-self.pos.x, -_y+vert.y-self.pos.y, -_z+vert.z+self.pos.z
        x = x*self.fov/z+cv[0]
        y = y*self.fov/z+cv[1]
        return Vec3d(x,y,z)

    def draw(self, o: Object3d):   
        if self.show_verts:            
            for v in o.verts:                               
                x,y,z = self.project(o, v)                
                pygame.gfxdraw.filled_circle(screen, int(x), int(y), 3, (255,255,255))

        if self.show_edges:
            for a,b in o.edges:
                v, V = o.verts[a], o.verts[b]                
                x,y,z = self.project(o, v)
                X,Y,Z = self.project(o, V)
                pygame.gfxdraw.line(screen, int(x), int(y), int(X), int(Y), o.color)
        
        if self.show_faces: #waiting for implementation ^^
            pass


## INIT PYGAME
pygame.init()
screen = pygame.display.set_mode(screen_size)
screen.fill(bgc)
#TODO class

player_movement = 0.7


world = list() 
# ^ let's say it's our world if not the challange and limited time 
# it could be nicely 'classified'
world += [
    Object3d(Vec3d(-1,-1, 0),color=(0,0,255)),
    Object3d(Vec3d(1,1,1)),
    Object3d(Vec3d(3,3,2), color=(255,255,0)),
    Object3d(Vec3d(5,5,3), color=(0,255,255)),
    Object3d(Vec3d(9,8,4), color=(255,255,255)),
    Object3d(Vec3d(3,3,5), color=(255,0,0)),
    
    
    Object3d(Vec3d(5,5,3.5), color=(0,255,255)),
    Object3d(Vec3d(9.5,8,4.5), color=(255,255,255)),
    Object3d(Vec3d(3,3.5,5.5), color=(255,0,0))   
]

_map = [
    "011111111110",
    "100100010001",
    "100100100001",
    "100101000001",
    "100110000001",
    "100110000001",
    "100101000001",
    "100100100001",
    "100100010001",
    "011111111110",
]
world2 = list()
created = False
labirynth = None
depth = 3
for idx_z, row in enumerate(_map):
    
    for idx_x, cell in enumerate(list(row)):
        for z in range(depth):
        
            if cell == '1':
                world2.append(Object3d(Vec3d(idx_x,idx_z,z), color=(255,0, int(z*255/depth))))
            
cam2 = Camera3d(Vec3d(-5,-5,-20))
# print(world2)



# box2 = Object3d(Vec3d(-1,3,2), size=Vec3d(0.1,0.2,0.1), color=(0,255,0))
# cam_user = Camera3d() #user can move it around
# cam_retarded = Camera3d() 


dt = 0
while(True):
    dt += 1
    # print(cam_user.pos.z, cam_retarded.pos.z)

    # cam_user.pos.z -= dt*0.003
    time.sleep(0.02)
    screen.fill(bgc)

    #steady cam
    # box2.rotate((0.05,0,0))
    # cam_user.draw(box2)

    #dungeon
    x = 0
    for o in world2:
        x += 1
        o.rotate(Vec3d(math.sin(dt/20+x/5)*0.05,0.01,0))        
        cam2.draw(o)
        if x == 10: x = 0

    ###retarded one
    #playing directly with objects
    # x ,y = math.sin(dt/7)*2, math.cos(dt/7)*2
    # world[3].pos=(x,y,3)
    # world[5].rotate((0,0,0.2))
    #playing with camera
    # cam_retarded.pos = Vec3d(math.sin(dt/25)*2, math.cos(dt/25)*2,(math.cos(dt/21)-3)*2)
    # world[0].rotate(Vec3d(0, 0, 0.09*math.sin(dt*0.1)))
    # for o in world:
    #     o.rotate((0, 0.03, 0))
    #     cam_retarded.draw(o)

    pygame.display.flip()
        
    
    #check if we should quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit(0)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                cam2.pos.x -= player_movement
            if event.key == pygame.K_RIGHT:
                cam2.pos.x += player_movement 
            if event.key == pygame.K_UP:
                cam2.pos.y -= player_movement
            if event.key == pygame.K_DOWN:
                cam2.pos.y += player_movement 
            if event.key == pygame.K_SPACE:
                cam2.pos.z = -5
    
#DO TO put all in __main__