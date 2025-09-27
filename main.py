#Import libraries
import pygame as pg
import math, datetime

#init pygame
pg.init()

#set WIDTH, HEIGHT of window
WIDTH, HEIGHT = RES = (800, 600)
sc = pg.display.set_mode(RES)

#set nesesery constants
G = 0.000000000066743
SCALE = 655000000
TIMESTEP = 3600*24*30/60

start_date = datetime.datetime(2025, 1, 1)
current_time_seconds = 0  

font = pg.font.SysFont("Arial", 24)

camera_x, camera_y = 0, 0

def world_to_screen(x, y):
    sx = int((x - camera_x) / SCALE + WIDTH/2)
    sy = int((y - camera_y) / SCALE + HEIGHT/2)
    return sx, sy

def screen_to_world(sx, sy):
    x = (sx - WIDTH/2) * SCALE + camera_x
    y = (sy - HEIGHT/2) * SCALE + camera_y
    return x, y

def is_mouse_over(obj, mouse_pos, scale):
    mx, my = mouse_pos
    x, y = world_to_screen(obj.x, obj.y)
    r = max(1, int(obj.radius * (5e8/scale)))
    distance = math.hypot(mx - x, my - y)
    return distance <= r

#main class
class Object_:
    def __init__(self, x, y, radius, color, mass, trail=True, name=""):
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
        self.name = name
        self.trail = trail
        self.positions = []

    def draw(self, sc, scale):
        #Drawing object
        x, y = world_to_screen(self.x, self.y)

        if self.trail and len(self.positions) > 1:
            points = [world_to_screen(px, py) for px, py in self.positions]
            pg.draw.lines(sc, (255 - self.color[0], 255 - self.color[1], 255 - self.color[2]), False, points, 2)

        pg.draw.circle(sc, self.color, (x, y), max(1, self.radius * (5e8 / scale)))

    #get attraction force
    def attraction(self, other):
        dx = other.x - self.x #delta x
        dy = other.y - self.y #delta y

        distance = math.sqrt(dx**2+dy**2) #get distance

        #check if distance!=0
        if distance == 0:
            return 0, 0
        
        force = G * self.mass * other.mass / distance**2 #force formula
        angle = math.atan2(dy, dx)
        force_x = math.cos(angle) * force #get x force
        force_y = math.sin(angle) * force #get y force

        return force_x, force_y
    #update position using Euler's method 
    def update_position(self):

        self.vx += self.fx / self.mass * TIMESTEP
        self.vy += self.fy / self.mass * TIMESTEP

        self.x += self.vx * TIMESTEP
        self.y += self.vy * TIMESTEP

        if self.trail:
            self.positions.append((self.x, self.y))

sun = Object_(0, 0, 50, pg.Color('Yellow'), 1.989e30, name="Sun")

planets = [
    Object_(57.9e9, 0, 6, (169, 169, 169), 3.301e23, trail=True, name="Mercury"),   # Mercury
    Object_(108.2e9, 0, 12, (218, 165, 32), 4.867e24, name="Venus"),  # Venus
    Object_(149.6e9, 0, 20, (0, 255, 0), 5.972e24, trail=True, name="Earth"),    # Earth
    Object_(227.9e9, 0, 10, (255, 0, 0), 0.642e24, name="Mars"),     # Mars
    Object_(778.6e9, 0, 40, (255, 165, 0), 1898e24, name="Jupiter"),   # Jupiter
    Object_(1433.5e9, 0, 34, (210, 180, 140), 568e24, name="Saturn"), # Saturn
    Object_(2872.5e9, 0, 28, (0, 255, 255), 86.8e24, name="Uranus"),  # Uranus
    Object_(4495.1e9, 0, 28, (0, 0, 255), 102e24, name="Neptune"),     # Neptune
    Object_(5906.4e9, 0, 4, (128, 128, 128), 0.0146e24, name="Pluto") # Pluto
]
for planet in planets:
    distance = planet.x
    orbital_speed = (G * sun.mass / distance) ** 0.5
    planet.vx = 0
    planet.vy = orbital_speed

objects = [sun] + planets

run = True
while run:
    for e in pg.event.get():
        if e.type == pg.QUIT:
            run = False
        elif e.type == pg.MOUSEWHEEL:
            mx, my = pg.mouse.get_pos()
            world_before = screen_to_world(mx, my)

            if e.y > 0:
                SCALE /= 1.1
            elif e.y < 0:
                SCALE *= 1.1

            world_after = screen_to_world(mx, my)
            camera_x += world_before[0] - world_after[0]
            camera_y += world_before[1] - world_after[1]

    sc.fill((255, 255, 255))

    current_time_seconds += TIMESTEP
    current_date = start_date + datetime.timedelta(seconds=current_time_seconds)


    for obj in objects:
        obj.fx = obj.fy = 0 #set to 0

        for other in objects:
            if obj != other:
                fx, fy = obj.attraction(other) #updating attraction 
#adding fx to object fx and fy to object fy
                obj.fx += fx
                obj.fy += fy

# drawing and updating position 
    for obj in objects:
        obj.update_position()
        obj.draw(sc, SCALE)

    mouse_pos = pg.mouse.get_pos()
    for obj in objects:
        if is_mouse_over(obj, mouse_pos, SCALE):
            name_surface = font.render(obj.name, True, (0,0,0))
            sc.blit(name_surface, (mouse_pos[0]+10, mouse_pos[1]+10))

    date_text = current_date.strftime("%d/%m/%Y %H:%M:%S")
    date_surface = font.render(date_text, True, (0, 0, 0))
    sc.blit(date_surface, (10, 10))
    scale_text = f"1:{int(SCALE)}"
    scale_surface = font.render(scale_text, True, (0, 0, 0))

    text_width, text_height = scale_surface.get_size()
    padding = 10
    x = WIDTH - text_width - padding
    y = HEIGHT - text_height - padding

    sc.blit(scale_surface, (x, y))


    pg.display.flip()
