# the slot simulator
__author__ = 'Vlada'

import random

# uses random.randrange to simulate the wheel turning
#
# 0 - empty
# 1 - one bar
# 2 - two bars
# 3 - three bars
# 4 - cherry
# 5 - seven
#
#
# WINNINGS
# 1 cherry      - 2x
# 2 cherries    - 5x
# any bar       - 10x
# 3 one bars    - 15x
# 3 two bars    - 20x
# 3 three bars  - 25x
# 3 cherries    - 30x
# 3 sevens      - 50x


values = ["empty", "one bar", "two bars", "three bars", "cherry", "seven"]
balance = 100
bet = 50
win = ""

def number_to_name(number):
    """ converts the known number to the name based of defined scheme """
    return values[number]


def name_to_number(name):
    """ converts the known name to the number based of defined scheme """
    return values.index(name)


def spin_one():
    return random.randrange(0, 6)


def spin_three():
    return [spin_one(), spin_one(), spin_one()]


def spin(b):
    global balance, bet, win
    win = ""
    print "Player balance:", b
    print "Player bets: ", bet
    print "...spinning..."
    roll = spin_three()
    b = b - bet + bet * evaluate_win_multiplier(roll)
    print "Roll:", get_roll_text(roll)
    print "WIN:", win
    print "Balance: ", b
    balance = b
    print ""
    print ""


def get_roll_text(roll):
    text = ""
    for x in range(0, 3):
        text += number_to_name(roll[x])
        if x != 2:
            text += ", "
    return text


def evaluate_win_multiplier(roll):
    global win
    if roll[0] == 0:
        return evaluate_cherries_multiplier(roll)
    elif roll[0] > 0 and roll[0] < 4:
        return evaluate_bars_multiplier(roll)
    elif roll[0] == 4:
        return evaluate_cherries_multiplier(roll)
    elif roll[0] == 5:
        if same_values(roll):
            win = "JACKPOT"
            return 50
        else:
            return evaluate_cherries_multiplier(roll)
    else:
        print "ERROR: Roll is not valid"
        return 0


def evaluate_cherries_multiplier(roll):
    global win
    nr = 0
    for x in range(0, 3):
        if roll[x] == 4:
            nr += 1
    if nr == 1:
        win = "one cherry"
        return 2
    elif nr == 2:
        win = "two cherries"
        return 5
    elif nr == 3:
        win = "three cherries"
        return 30
    else:
        return 0


def evaluate_bars_multiplier(roll):
    global win
    bar = roll[0]
    if same_values(roll):
        if bar == 1:
            win = "three one bars"
            return 15
        elif bar == 2:
            win = "three two bars"
            return 20
        elif bar == 3:
            win = "three three bars"
            return 25
        else:
            return 0
    else:
        if roll[1] > 0 and roll[1] < 4 and roll[2] > 0 and  roll[2] < 4:
            win = "any bars"
            return 10
        else:
            return evaluate_cherries_multiplier(roll)


def same_values(roll):
    if roll[0] == roll[1] and roll[0] == roll[2]:
        return True
    else:
        return False


#spin(balance)

def spin_times(n):
    for x in range(0, n):
        spin(balance)


spin_times(10)