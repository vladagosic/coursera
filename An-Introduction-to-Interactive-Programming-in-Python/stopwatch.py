# "Stopwatch: The Game" by Vladimir Gosic

import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

# global variables

interval = 100			# interval for timer in miliseconds
win_condition = 10		# win if the time is divisible by it
time = 0				# time passed since last reset
score = [0, 0]			# holds nr. of tries and wins


# helper functions for formatting strings

def format_time(t):
    """ formats the integer in time format 'm:ss.mm' """
    tenth_sec_str = str(time % 10)
    seconds = (time % 600) / 10
    seconds_str = "0" + str(seconds) if seconds < 10 else str(seconds)
    min_str = str(time / 600)
    return min_str + ":" + seconds_str + "." + tenth_sec_str
    
def format_score(s):
    """ formats the score array in format 'T / W' """
    return str(s[0]) + " / " + str(s[1])    
 
    
# event handlers for buttons; "start", "stop", "reset"

def start():
    """ starts the timer """
    timer.start()

def stop():
    """ stops the timer and evaluates time. updates the score """
    if timer.is_running():
        timer.stop()
        if time % win_condition == 0:
            score[0] += 1
        score[1] += 1

def reset():
    """ stops the timer and resets the time and score """
    global time, score
    timer.stop()
    time = 0
    score = [0, 0]

    
# event handler for timer

def tick():
    """ increments the time """
    global time
    time += 1

    
# draw event handler

def draw(canvas):
    canvas.draw_text(format_time(time), [90, 120], 50, "White",  "sans-serif")
    canvas.draw_text(format_score(score), [220, 40], 24, "Green",  "sans-serif")
    canvas.draw_text("by VG", [270, 190], 8, "Gray",  "monospace")
    
# create frame

frame = simplegui.create_frame("Stopwatch Game", 300, 200)


# create buttons with event handlers

frame.add_button("Start", start, 100)
frame.add_button("Stop", stop, 100)
frame.add_button("Reset", reset, 100)


# create timer

timer = simplegui.create_timer(interval, tick)


# set the draw handler for canvas

frame.set_draw_handler(draw)


# start frame and the game. HAVE FUN! :)

frame.start()

