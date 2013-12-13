__author__ = 'Vladimir Gosic'

#SpaceShip
import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import math
import random


# globals for user interface
WIDTH = 800
HEIGHT = 600
PLAYER_SCORE = [20, 30, 100, 20]
time = 0.5

# game globals
SHIP_TURN_SPEED = 0.1
SHIP_SPEED = 0.25
SHIP_LIVES = 3
FRICTION = 0.01
MISSILE_SPEED = 3
MISSILE_LIFE = 60
ROCK_COUNT = 12
started = False


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
missile_info = ImageInfo([5, 5], [10, 10], 3, MISSILE_LIFE)
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
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)


# Sprite class
class Sprite():
    def __init__(self, pos, vel, angle, angle_vel, image, info, parent=None, sound=None):
        self.pos = [pos[0], pos[1]]
        self.vel = [vel[0], vel[1]]
        self.angle = angle
        self.angle_vel = angle_vel
        self.image = image
        self.image_center = list(info.get_center())
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        self.parent = parent
        self.sound = sound
        if self.sound:
            self.sound.rewind()
            self.sound.play()

    def get_position(self):
        return self.pos

    def get_radius(self):
        return self.radius

    def collide(self, other_object):
        return dist(self.get_position(), other_object.get_position()) < self.get_radius() + other_object.get_radius()

    def draw(self, canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)

    def update(self, friction=0.0):
        # update orientation
        self.age += 1
        self.angle += self.angle_vel
        for i in range(2):
            self.vel[i] *= 1 - friction
        # update position
        limits = (WIDTH, HEIGHT)
        for i in range(2):
            self.pos[i] += self.vel[i]
            self.pos[i] = self.pos[i] % limits[i]
        #print self.lifespan and self.age < self.lifespan, self.lifespan, self.age
        return self.lifespan < self.age


# Ship class, it inherits from Sprite class
class Ship(Sprite):
    def __init__(self, controls, player, *args, **kwds):
        Sprite.__init__(self, *args, **kwds)  # inherit from sprite
        self.thrust = False
        self.score = 0
        self.lives = SHIP_LIVES
        self.controls = {"left": controls[0], "up": controls[1], "right": controls[2], "fire": controls[4]}
        self.player = player
        self.missiles = set()
        if self.sound:
            self.sound.pause()
            self.sound.rewind()

    def set_thrust(self, value):
        self.thrust = value
        # shift image center and play/pause sound
        if value:
            self.image_center[0] *= 3
            if self.sound:
                self.sound.play()
        else:
            self.image_center[0] /= 3
            if self.sound:
                self.sound.pause()
                self.sound.rewind()

    def shoot(self):
        # shoot and return a missile (Sprite object)
        point_at = angle_to_vector(self.angle)
        pos = list(self.pos)
        vel = list(self.vel)
        for i in range(2):
            pos[i] += point_at[i] * self.image_center[0]
            vel[i] += point_at[i] * 5
        return Sprite(pos, vel, self.angle, 0, missile_image, missile_info, self, missile_sound)

    def update(self):
        # move forward
        if self.thrust:
            vel = angle_to_vector(self.angle)
            for i in range(2):
                self.vel[i] += vel[i] * SHIP_SPEED
        # sprite behaviour
        Sprite.update(self, FRICTION)

    def draw_score(self, index, canvas):
        pos = PLAYER_SCORE[0] if (len(ships) == 1 or index == 0) else ((WIDTH - PLAYER_SCORE[0] - PLAYER_SCORE[2]) / (len(ships) - 1)) * index
        canvas.draw_text(self.player, [pos, PLAYER_SCORE[1]], PLAYER_SCORE[3], "White", "monospace")
        canvas.draw_text("LIVES: " + str(self.lives), [pos, PLAYER_SCORE[1] * 2], PLAYER_SCORE[3], "White", "monospace")
        canvas.draw_text("SCORE: " + str(self.score), [pos, PLAYER_SCORE[1] * 3], PLAYER_SCORE[3], "White", "monospace")

    def is_alive(self):
        return self.lives > 0


# draw handler
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

    #draw game start screen


    # update and draw sprites and ship
    process_sprite_group(rocks, canvas)
    idx = alive = 0
    for ship in set(ships):
        ship.draw_score(idx, canvas)
        if ship.is_alive():
            alive += 1
            ship.update()
            ship.draw(canvas)
            ship.score += group_group_collide(ship.missiles, rocks)
            process_sprite_group(ship.missiles, canvas)
            if group_collide(rocks, ship):
                ship.lives -= 1
        idx += 1
    if alive == 0:
        initialize()


def key_down(key):
    for ship in ships:
        if ship.controls["up"] == key:
            ship.set_thrust(True)
        elif ship.controls["left"] == key:
            ship.angle_vel = -SHIP_TURN_SPEED
        elif ship.controls["right"] == key:
            ship.angle_vel = SHIP_TURN_SPEED
        elif ship.controls["fire"] == key:
            ship.missiles.add(ship.shoot())


def key_up(key):
    for ship in ships:
        if ship.controls["up"] == key:
            ship.set_thrust(False)
        elif ship.controls["left"] == key:
            ship.angle_vel = 0.0
        elif ship.controls["right"] == key:
            ship.angle_vel = 0.0


def mouse_handler(position):
    global started
    if started == False:
        started = True


def group_group_collide(group, other_group):
    cnt = 0
    for item in set(group):
        if group_collide(other_group, item):
            group.discard(item)
            cnt += 1
    return cnt


def group_collide(group, other_object):
    for item in set(group):
        if item.collide(other_object):
            group.remove(item)
            return True
    return False


def process_sprite_group(sprites, canvas):
    for sprite in list(sprites):
        if sprite.update():
            sprites.remove(sprite)
        sprite.draw(canvas)


# timer handler that spawns a rock
def rock_spawner():
    if started and len(rocks) <= ROCK_COUNT:
        pos = [random.random() * WIDTH, random.random() * HEIGHT]
        vel = angle_to_vector(random.random() * 2 * math.pi)  # random vel
        a_vel = (random.random() - 0.5) * 0.05  # random spin vel
        rock = Sprite(pos, vel, 0, a_vel, asteroid_image, asteroid_info)
        valid = True
        for ship in set(ships):
            if ship.is_alive():
                valid = valid and not ship.collide(rock)
        if valid:
            rocks.add(rock)


def initialize():
    global ships, rocks, started
    # initialize ships and rocks sets
    ships = set()
    rocks = set()
    started = False

    if soundtrack:
        soundtrack.rewind()
        soundtrack.play()

    ship_settings = [["left", "up", "right", "down", "space", "player 1"]]
                     # ["A", "W", "D", "S", "R", "player 2"],
                     # ["H", "U", "K", "J", "O", "player 3"]]
    for ship in ship_settings:
        controls = []
        for i in range(len(ship) - 1):
            controls.append(simplegui.KEY_MAP[ship[i]])
        pos = [WIDTH / (len(ship_settings) + 1) * (ship_settings.index(ship) + 1), HEIGHT / 2]
        ships.add(Ship(controls, ship[-1], pos, [0, 0], 0, 0, ship_image, ship_info, None, ship_thrust_sound))

    rock_spawner()  # force a initial spawn

# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
initialize()    # initialize game objects

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(key_down)
frame.set_keyup_handler(key_up)
frame.set_mouseclick_handler(mouse_handler)
timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
