# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console
import simplegui
import random
import math


# initialize global variables used in your code
secret = 0
range_low = 0
range_high = 100
number_of_guesses = 7


# helper function to start and restart the game
def new_game():
    """ starts a new game of Guess the number """
    global secret, number_of_guesses
    # generate a secret number and calculate available number of 
    # tries based on the formula: 2 ** n >= high - low + 1
    secret = random.randrange(range_low, range_high)
    number_of_guesses = int(math.ceil(math.log(range_high, 2)))
    # print the game setting and information
    print "New game. Range if from", range_low, "to", range_high
    print "Number of remaining guesses", number_of_guesses
    print ""


# define event handlers for control panel
def range100():
    """ sets the upper limit of the range to 100 and restarts the game """
    global range_high
    # set the upper range and restart the game
    range_high = 100
    new_game()


def range1000():
    """ sets the upper limit of the range to 1000 and restarts the game """
    # set the upper range and restart the game
    global range_high
    range_high = 1000
    new_game()

    
def input_guess(guess):
    """ converts input to number and compares it to secret. 
        lowers the number of guesses by 1, prints game outcome
        and restarts the game if correct number of guesses reached 0
    """
    global number_of_guesses
    # print the value that the player entered
    print "Guess was", guess
    # lower the number of guesses by 1 and print it
    number_of_guesses -= 1
    print "Number of remaining guesses", number_of_guesses
    # convert the player value to number and compare it to secret
    guess_nr = int(float(guess))
    if guess_nr == secret:
        # print information and restart game with last settings
        print "Correct!"
        print ""
        new_game()
    elif guess_nr > secret and guess_nr < range_high:
        print "Lower!"
    elif guess_nr < secret and guess_nr > range_low:
        print "Higher!"
    else:
        # print that player entered number out of range boundaries
        print "Guess is out of the range."
    print ""
    if number_of_guesses == 0:
        # print that player spent all tries, 
        # show the secret number and restart
        print "You loose! Requested number was", secret
        print ""
        new_game()

    
# create frame
frame = simplegui.create_frame("Guess the number", 200, 200)

# register event handlers for control elements
frame.add_button("Range is (0, 100]", range100, 200)
frame.add_button("Range is (0, 1000]", range1000, 200)
frame.add_input("Enter a guess", input_guess, 200)

# call new_game and start frame
new_game()
frame.start()

# always remember to check your completed program against the grading rubric
