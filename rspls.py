# Rock-paper-scissors-lizard-Spock template
import random

# The key idea of this program is to equate the strings
# "rock", "paper", "scissors", "lizard", "Spock" to numbers
# as follows:
#
# 0 - rock
# 1 - Spock
# 2 - paper
# 3 - lizard
# 4 - scissors

# helper functions

def number_to_name(number):
    """ converts the known number to the name based of defined scheme """
    # fill in your code below
    if number == 0:
        return "rock"
    elif number == 1:
        return "Spock"
    elif number == 2:
        return "paper"
    elif number == 3:
        return "lizard"
    elif number == 4:
        return "scissors"
    else:
        print("number out of range, ", number)
    # convert number to a name using if/elif/else
    # don't forget to return the result!

    
def name_to_number(name):
    """ converts the known name to the number based of defined scheme """
    # fill in your code below
    if name == "rock":
        return 0
    elif name == "Spock":
        return 1
    elif name == "paper":
        return 2
    elif name == "lizard":
        return 3
    elif name == "scissors":
        return 4
    else:
        print("name unknown, ", name)
    # convert name to number using if/elif/else
    # don't forget to return the result!


def rpsls(name):
    """ takes a passed name, transforms it into number, generates a random number and determines the winner """
    # fill in your code below
    # convert name to player_number using name_to_number
    player_number = name_to_number(name)
    # compute random guess for comp_number using random.randrange()
    comp_number = random.randrange(0, 5)
    # compute difference of player_number and comp_number modulo five
    diff = (player_number - comp_number) % 5
    outcome = ""
	# use if/elif/else to determine winner
    if (diff == 0):
        outcome = "Player and computer tie!"
    elif (diff < 3):
        outcome = "Player wins!"
    else:
        outcome = "Computer wins!"
    # convert comp_number to name using number_to_name
    comp_name = number_to_name(comp_number)
    # print results
    print "Player chooses", name
    print "Computer chooses", comp_name
    print outcome
    print ""
    
# test your code
rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")

# always remember to check your completed program against the grading rubric


