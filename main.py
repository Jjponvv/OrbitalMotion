import pygame as pg
import math

pg.init()

WIDTH, HEIGHT = RES = (800, 600)

sc = pg.display.set_mode(RES)

##CONSTANTS##

G = 0.000000000066743
SCALE = 1000000000
TIMESTEP = 3600 * 24

class Object_:
    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass
        self.vx = 0
        self.vy = 0
        self.fx = 0
        self.fy = 0

    def draw(self, sc):
        pg.draw.circle(sc, self.color, (int(self.x/SCALE+WIDTH/2), int(self.y/SCALE+HEIGHT/2)), self.radius)

    def attraction(self, other):
        dx = other.x - self.x
        dy = other.y - self.y

        distance = math.sqrt(dx**2+dy**2)

        if distance == 0:
            return 0, 0
        
        force = G * self.mass * other.mass / distance**2
        angle = math.atan2(dy, dx)
        force_x = math.cos(angle) * force
        force_y = math.sin(angle) * force

        return force_x, force_y
    
    def update_position(self):

        self.vx += self.fx / self.mass * TIMESTEP
        self.vy += self.fy / self.mass * TIMESTEP

        self.x += self.vx * TIMESTEP
        self.y += self.vy * TIMESTEP

sun = Object_(WIDTH / 2, HEIGHT / 2, 30, pg.Color('Yellow'), 1.989e30)
earth = Object_(WIDTH / 2 + 150 * SCALE, HEIGHT / 2 + 50 * SCALE, 20, (0, 255, 0), 5.972e24)
earth.vy = 29_783

objects = [sun, earth]

run = True
while run:
    for e in pg.event.get():
        if e.type == pg.QUIT:
            run = False

    sc.fill((255, 255, 255))

    for obj in objects:
        obj.fx = obj.fy = 0

        for other in objects:
            if obj != other:
                fx, fy = obj.attraction(other)
                obj.fx += fx
                obj.fy += fy

    for obj in objects:
        obj.update_position()
        obj.draw(sc)

    pg.display.flip()
