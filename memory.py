# implementation of card game - Memory by Vladimir Gosic

import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import random


def new_game():
    """ initializes the global variables for the memory game (0: not flipped, 1: flipped unpaired, 2: flipped paired) """
    global cards_list, turns, last_guess
    turns = 0
    last_guess = -1
    # two dimensional array holds the card values and their states
    cards_list = [[0, 0], [0, 0], [1, 0], [1, 0], [2, 0], [2, 0], [3, 0], [3, 0], [4, 0], [4, 0], [5, 0], [5, 0], [6, 0], [6, 0], [7, 0], [7, 0]]
    random.shuffle(cards_list)
    label.set_text("Turns = " + str(turns))


def mouse_click(pos):
    """ gets the index based on position and checks if it is paired with previous guess """
    global last_guess, turns
    # get the index based on position clicked
    index = pos[0] // 50 + pos[1] // 100 * 8
    # execute logic only if the card is not already flipped
    if cards_list[index][1] == 0:
        if last_guess == -1:
            # reset the previously flipped cards
            for card in [card for card in cards_list if card[1] == 1]:
                card[1] = 0
            # save current guess and set card flipped
            last_guess = index
            cards_list[index][1] = 1
        elif cards_list[last_guess][0] == cards_list[index][0]:
            # set state of the cards to guessed, increment the number of turns and reset last guess
            cards_list[last_guess][1] = 2
            cards_list[index][1] = 2
            last_guess = -1
            turns += 1
        else:
            # increment number of turns and reset last guess since the cards are different
            cards_list[index][1] = 1
            last_guess = -1
            turns += 1
    # write the number of turns played in the label
    label.set_text("Turns = " + str(turns))


def draw(canvas):
    """ draws the cards in 2 rows; not flipped if their state is 0, else flipped; if all cards are flipped game over """
    game_over = True
    for card in list(enumerate(cards_list)):
        if card[1][1] == 0:
            canvas.draw_polygon([[card[0] % 8 * 50, card[0] // 8 * 100], [(card[0] % 8 + 1) * 50, card[0] // 8 * 100], [(card[0] % 8 + 1) * 50, 100 + card[0] // 8 * 100], [card[0] % 8 * 50, 100 + card[0] // 8 * 100]], 5, "Black", "Orange")
            game_over = False
        else:
            canvas.draw_text(str(card[1][0]), [5 + card[0] % 8 * 50, 75 + card[0] // 8 * 100], 70, "White", "monospace")
    if game_over:
        canvas.draw_polygon([[0, 0], [400, 0], [400, 200], [0, 200]], 5, "Black", "Black")
        canvas.draw_text("GAME", [55, 90], 100, "Red", "sans-serif")
        canvas.draw_text("OVER", [55, 180], 100, "Red", "sans-serif")


# create frame and add a button and labels
frame = simplegui.create_frame("Memory Game", 400, 200)
frame.add_button("Restart", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouse_click)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric