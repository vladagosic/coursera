# program template for Spaceship

# GOOD MOVEMENT!        http://www.codeskulptor.org/#user26_7cfmV7nH5N_0.py
# explosion image:      http://commondatastorage.googleapis.com/codeskulptor-assets/explosion.hasgraphics.png


import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import math
import random

class ImageInfo:
    def __init__(self, center, size, radius=0, lifespan=None, animated=False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2013.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5, 5], [10, 10], 3, -1)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p, q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info, controls, thrust_sound=None):
        self.pos = [pos[0], pos[1]]
        self.vel = [vel[0], vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.controls = controls
        self.sound = thrust_sound
        self.missile_away = False
        self.score = 0
        self.lives = SHIP_LIVES
        
    def draw(self, canvas):
        if self.thrust:
            self.image_center[0] = 1.5 * self.image_size[0]
        else:
            self.image_center[0] = 0.5 * self.image_size[0]
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)

    def update(self, keys_pressed):
        if keys_pressed[self.controls[4]] and not self.missile_away:
            self.fire_misile()
        elif not keys_pressed[self.controls[4]] and self.missile_away:
            self.missile_away = False

        if keys_pressed[self.controls[0]]:
            self.angle_vel -= SHIP_TURN_SPEED

        if keys_pressed[self.controls[2]]:
            self.angle_vel += SHIP_TURN_SPEED

        self.angle_vel *= DEBRIS_FRICTION
        self.angle += self.angle_vel

        forward = angle_to_vector(self.angle)

        if self.sound:
            if keys_pressed[self.controls[1]] and not self.thrust:
                self.sound.play()
            elif not keys_pressed[self.controls[1]] and self.thrust:
                self.sound.pause()
                #self.sound.rewind()

        self.thrust = keys_pressed[self.controls[1]]

        if self.thrust:
            self.vel[0] += forward[0] * SHIP_SPEED
            self.vel[1] += forward[1] * SHIP_SPEED

        self.vel[0] *= DEBRIS_FRICTION
        self.vel[1] *= DEBRIS_FRICTION

        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT

    def fire_misile(self):
        forward = angle_to_vector(self.angle)

        if len(missiles) == MISSILE_COUNT:
            missiles.remove(missiles[0])
        missiles.append(Sprite([self.pos[0] + forward[0] * self.image_size[0] / 2, self.pos[1] + forward[1] * self.image_size[1] / 2], [self.vel[0] + forward[0] * MISSILE_SPEED, self.vel[1] + forward[1] * MISSILE_SPEED], self.angle, 0, missile_image, missile_info, missile_sound))
        self.missile_away = True
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound=None):
        self.pos = [pos[0], pos[1]]
        self.vel = [vel[0], vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        #canvas.draw_circle(self.pos, self.radius, 1, "Red", "Red")
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
    
    def update(self):
        if self.lifespan > 0:
            self.lifespan -= 1
        self.angle += self.angle_vel

        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT



def draw(canvas):
    global time
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    canvas.draw_text("Lives", LIVES_POS, 18, "White", "monospace")
    canvas.draw_text("Score", SCORE_POS, 18, "White", "monospace")

    # update and draw ships and sprites
    for ship in ships:
        canvas.draw_text(str(ship.lives), [LIVES_POS[0], LIVES_POS[1] + TEXT_SIZE * (ships.index(ship) + 1)], 18, "White")
        canvas.draw_text(str(ship.score), [SCORE_POS[0], SCORE_POS[1] + TEXT_SIZE * (ships.index(ship) + 1)], 18, "White")
        ship.update(keys)
        ship.draw(canvas)
    for rock in rocks:
        rock.update()
        rock.draw(canvas)
    #dead_missiles = []
    for missile in list(missiles):
        missile.update()
        missile.draw(canvas)
        if missile.lifespan == 0:
            missiles.remove(missile)
    #for dead in dead_missiles:
    #    missiles.remove(dead)


def key_down(key):
    #print(chr(key))
    if chr(key) in keys.keys():
        keys[chr(key)] = True


def key_up(key):
    if chr(key) in keys.keys():
        keys[chr(key)] = False
            
# timer handler that spawns a rock    
def rock_spawner():
    if len(rocks) == ROCK_COUNT:
        rocks.remove(rocks[0])
    rocks.append(Sprite([random.randrange(100, WIDTH - 100), random.randrange(100, HEIGHT - 100)], [random.randrange(-100, 100) / 30, random.randrange(-100, 100) / 30], 0, random.randrange(-10, 10) * 0.03, asteroid_image, asteroid_info))
    
def initialize():
    global ships, rocks, missiles, keys
    # initialize ships, rocks and missiles collection
    ships = []
    rocks = []
    missiles = []
    keys = {}

    ship_controls = [["%", "&", "'", "down", " "],
                     ["A", "W", "D", "S", "R"]]
    for ship in ship_controls:
        ships.append(Ship([WIDTH / (len(ship_controls) + 1) * (ship_controls.index(ship) + 1), HEIGHT / 2], [0, 0], 0, ship_image, ship_info, ship, ship_thrust_sound))
        for control in ship:
            keys[control] = False

# globals for user interface
WIDTH = 800
HEIGHT = 600
LIVES_POS = [20, 30]
SCORE_POS = [700, 30]
TEXT_SIZE = 20
time = 0.5

# game globals
SHIP_TURN_SPEED = 0.009
SHIP_SPEED = 0.75
SHIP_LIVES = 3
DEBRIS_FRICTION = 0.95
MISSILE_SPEED = 3
MISSILE_COUNT = 4
ROCK_COUNT = 5

# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(key_down)
frame.set_keyup_handler(key_up)

timer = simplegui.create_timer(1000.0, rock_spawner)

initialize()
# get things rolling
timer.start()
frame.start()
