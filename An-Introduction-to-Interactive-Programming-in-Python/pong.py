
# Implementation of classic arcade game Pong

import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True

score1 = 0
score2 = 0

ball_pos = [WIDTH / 2, HEIGHT / 2]
ball_vel = [0, 0]

paddle1_pos = HEIGHT / 2
paddle2_pos = HEIGHT / 2

paddle1_vel = 0
paddle2_vel = 0

PAD_SPEED = 3
BALL_ACC = 1.1


# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel  # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT / 2]

    x = random.randrange(120, 240) / 60
    y = random.randrange(60, 180) / 60

    if direction == RIGHT:
        ball_vel = [x, -y]
    elif direction == LEFT:
        ball_vel = [-x, -y]


# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints

    paddle1_pos = HEIGHT / 2
    paddle2_pos = HEIGHT / 2

    paddle1_vel = 0
    paddle2_vel = 0

    score1 = 0
    score2 = 0

    if random.randrange(1, 11) % 2 == 0:
        dct = RIGHT
    else:
        dct = LEFT

    spawn_ball(dct)

def draw(c):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel

    # draw mid line and gutters
    c.draw_line([WIDTH / 2, 0], [WIDTH / 2, HEIGHT], 1, "White")
    c.draw_line([PAD_WIDTH, 0], [PAD_WIDTH, HEIGHT], 1, "White")
    c.draw_line([WIDTH - PAD_WIDTH, 0], [WIDTH - PAD_WIDTH, HEIGHT], 1, "White")

    # update ball
    if ball_pos[1] <= BALL_RADIUS or ball_pos[1] >= HEIGHT - 1 - BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]

    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]

    # check if the ball touched the gutter or the paddle
    if ball_pos[0] - BALL_RADIUS <= PAD_WIDTH:
        if paddle1_pos - HALF_PAD_HEIGHT <= ball_pos[1] <= paddle1_pos + HALF_PAD_HEIGHT:
            ball_vel[0] = -ball_vel[0] * BALL_ACC
            ball_vel[1] *= BALL_ACC
        else:
            score2 += 1
            spawn_ball(RIGHT)
    elif ball_pos[0] + BALL_RADIUS >= WIDTH - 1:
        if paddle2_pos - HALF_PAD_HEIGHT <= ball_pos[1] <= paddle2_pos + HALF_PAD_HEIGHT:
            ball_vel[0] = -ball_vel[0] * BALL_ACC
            ball_vel[1] *= BALL_ACC
        else:
            score1 += 1
            spawn_ball(LEFT)

    # draw ball
    c.draw_circle(ball_pos, BALL_RADIUS, 5, 'White', 'White')

    # update paddle's vertical position, keep paddle on the screen
    if paddle1_pos + paddle1_vel - HALF_PAD_HEIGHT >= 0 and paddle1_pos + paddle1_vel + HALF_PAD_HEIGHT <= HEIGHT:
        paddle1_pos += paddle1_vel

    if paddle2_pos + paddle2_vel - HALF_PAD_HEIGHT > 0 and paddle2_pos + paddle2_vel + HALF_PAD_HEIGHT < HEIGHT:
        paddle2_pos += paddle2_vel

    # draw paddles
    c.draw_polygon([[0, paddle1_pos - HALF_PAD_HEIGHT], [PAD_WIDTH, paddle1_pos - HALF_PAD_HEIGHT], [PAD_WIDTH, paddle1_pos + HALF_PAD_HEIGHT], [0, paddle1_pos + HALF_PAD_HEIGHT]], 2, 'White', 'White')
    c.draw_polygon([[WIDTH - PAD_WIDTH, paddle2_pos - HALF_PAD_HEIGHT], [WIDTH, paddle2_pos - HALF_PAD_HEIGHT], [WIDTH, paddle2_pos + HALF_PAD_HEIGHT], [WIDTH - PAD_WIDTH, paddle2_pos + HALF_PAD_HEIGHT]], 2, 'White', 'White')

    # draw scores
    c.draw_text(str(score1), [WIDTH / 4 - 20, 50], 40, "White",  "monospace")
    c.draw_text(str(score2), [3 * WIDTH / 4 - 20, 50], 40, "White",  "monospace")


def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel = -PAD_SPEED
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel = PAD_SPEED
    elif key == simplegui.KEY_MAP["up"]:
        paddle2_vel = -PAD_SPEED
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel = PAD_SPEED


def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP["up"]:
        paddle2_vel = 0
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 0

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Reset", new_game, 100)

# start frame
new_game()
frame.start()
