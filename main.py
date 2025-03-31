#Import libraries
import pygame as pg
import math

#init pygame
pg.init()

#set WIDTH, HEIGHT of window
WIDTH, HEIGHT = RES = (800, 600)
sc = pg.display.set_mode(RES)

#set nesesery constants
G = 0.000000000066743
SCALE = 1000000000
TIMESTEP = 3600

#main class
class Object_:
    def __init__(self, x, y, radius, color, mass):
      #set variables
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
      #Drawing object
        pg.draw.circle(sc, self.color, (int(self.x/SCALE+WIDTH/2), int(self.y/SCALE+HEIGHT/2)), self.radius)

    #get attraction force
    def attraction(self, other):
        dx = other.x - self.x #delta x
        dy = other.y - self.y #delta y

        distance = math.sqrt(dx**2+dy**2)#get distance

        #check if distance!=0
        if distance == 0:
            return 0, 0
        
        force = G * self.mass * other.mass / distance**2 #force formula
        angle = math.atan2(dy, dx)
        force_x = math.cos(angle) * force #get xForce
        force_y = math.sin(angle) * force #get y force

        return force_x, force_y
    #update position using Euler's method 
    def update_position(self):

        self.vx += self.fx / self.mass * TIMESTEP
        self.vy += self.fy / self.mass * TIMESTEP

        self.x += self.vx * TIMESTEP
        self.y += self.vy * TIMESTEP

#create sun and earth
sun = Object_(WIDTH / 2, HEIGHT / 2, 60, pg.Color('Yellow'), 1.989e30)
earth = Object_(WIDTH / 2 + 128.781668823 * SCALE, HEIGHT / 2 + 82.781668823 * SCALE, 10, (0, 255, 0), 5.972e24)

#set y velocity for earth
earth.vy = 29783

objects = [sun, earth]

run = True
while run:
    for e in pg.event.get():
        if e.type == pg.QUIT:
            run = False

    sc.fill((255, 255, 255))

    for obj in objects:
        obj.fx = obj.fy = 0 #set to 0

        for other in objects:
            if obj != other:
                fx, fy = obj.attraction(other) #updating attraction 
#adding fx to object fx and ft to object fy
                obj.fx += fx
                obj.fy += fy

# drawing and updating position 
    for obj in objects:
        obj.update_position()
        obj.draw(sc)

    pg.display.flip()
