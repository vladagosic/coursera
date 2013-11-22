# Mini-project #6 - Blackjack by Vladimir Gosic

import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import random

# for printing values to the console set this to True
USE_PRINT = False

# load card images (949x460)
CARD_SIZE = (73, 115)
CARD_CENTER = (CARD_SIZE[0] / 2, CARD_SIZE[1] / 2)
CARD_SPACE = 10
card_images_standard = simplegui.load_image("http://i.imgur.com/bX4bLvm.png")
card_images_fancy = simplegui.load_image("http://i.imgur.com/D8SarJM.png")
card_images = card_images_fancy

# load card back images (73x115)
card_back_standard = simplegui.load_image("http://i.imgur.com/BDt4CCh.png")
card_back_fancy = simplegui.load_image("http://i.imgur.com/Ib5yDTJ.png")
card_back = card_back_fancy

# load background image (600x600)
BG_SIZE = (600, 600)
BG_CENTER = (BG_SIZE[0] / 2, BG_SIZE[1] / 2)
bg_image = simplegui.load_image("http://i.imgur.com/GhxDeyu.png")

# initialize the text items draw positions
SCORES_TOP = 570
LOC_DEALER = 200
LOC_PLAYER = 400
LEFT_MARGIN = 50
MID_MARGIN = 300
LOC_BET = 270
LOC_SCORE = 450
TEXT_DIST = 30

# initialize some useful global variables
startup = True
in_play = False
outcome = action = ""
bet = temp_bet = 50
balance = 1000
score = 0

# the blinking text variables
blink_colors = ["Black", "White"]
blink_interval = 60
blink_ticks = 0

# define globals for cards
SUITS = ('S', 'H', 'C', 'D')  # S - Spades, H - Hearths, C - Clubs, D - Diamonds
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 10, 'Q': 10, 'K': 10}

intro_head = "Welcome to the Blackjack table card game"
intro_rules = ["Rules:",
               "You start off with the balance $1000.",
               "You can set bet by entering desired value and hitting Enter.",
               " (note: the entered bet will be accepted next time you click deal)",
               "When you click Deal the bet amount is deduced from you balance.",
               "You and the dealer are dealt two cards each.",
               "You have options to:",
               " - Hit (get another card) ",
               " - Stand (dealer gets cards until his hand value is 17 or more)",
               "The winner is the one that has greater Hand value but not greater than 21.",
               "The one that has Hand value greater than 21 is busted and losses.",
               " (note: if the hand values are tied the dealer wins!)",
               "If you win you get double the bet amount.",
               "If you win with a Hand value of 21 you get five times the bet amount."]


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        """ Gets suit value """
        return self.suit

    def get_rank(self):
        """ Gets rank value """
        return self.rank

    def draw(self, canvas, pos):
        """  Draws the card on canvas on the requested position [top, left] """
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank),
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)

# define hand class
class Hand:
    def __init__(self):
        self.cards = []

    def __str__(self):
        result = "["
        for card in self.cards:
            result += str(card)
            if self.cards.index(card) < len(self.cards) - 1:
                result += ", "
        result += "]"
        return result

    def add_card(self, card):
        """ Adds the card object to the cards list """
        self.cards.append(card)

    def get_value(self):
        """ Gets the sum value of all the cards in the cards list """
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        value = 0
        has_aces = False
        for card in self.cards:
            value += int(VALUES[card.rank])
            if card.rank == "A":
                has_aces = True
        if has_aces and value + 10 <= 21:
            return value + 10
        else:
            return value

    def draw(self, canvas, pos):
        """ Draws the deck as horizontal list of cards on the canvas """
        i = 0
        for card in self.cards:
            card.draw(canvas, [pos[0] + i, pos[1]])
            i += CARD_SIZE[0] + CARD_SPACE


# define deck class
class Deck:
    def __init__(self):
        self.cards = []
        for suit in SUITS:
            for rank in RANKS:
                self.cards.append(Card(suit, rank))

    def shuffle(self):
        """ Shuffles the cards list """
        random.shuffle(self.cards)

    def deal_card(self):
        """ Returns the card from the last index of cards list and removes it """
        return self.cards.pop()

    def __str__(self):
        result = "["
        for card in self.cards:
            result += str(card)
            if self.cards.index(card) < len(self.cards) - 1:
                result += ", "
        result += "]"
        return result


#define event handlers for buttons
def deal():
    """ creates a deck and player and dealer hands, deals them cards and sets messages and flags.
    updates the score and balance """
    global deck, player, dealer, outcome, action, in_play, score, bet, balance, startup
    # set the startup flag to false in order to draw the game content
    startup = False
    # update the score and display message if the player did not finish previous round
    if in_play:
        score -= 1
        outcome = "You have lost previous round!"
    else:
        outcome = ""
    # create a deck and a player and dealer hand
    deck = Deck()
    deck.shuffle()
    player = Hand()
    dealer = Hand()
    # deal two cards to both dealer and player
    for i in range(2):
        player.add_card(deck.deal_card())
        dealer.add_card(deck.deal_card())
    # use the bet from input box and deduce it from the player balance
    bet = temp_bet
    balance -= bet
    # set the action message and flag that the round is in progress
    action = "Hit or stand?"
    in_play = True
    if USE_PRINT:
        print_values()

def hit():
    """ Adds a card to the player hand and checks if it is busted """
    global outcome, in_play, score
    # if the hand is in play, hit the player
    if in_play:
        # disallow player to get a card if he's over 21
        if player.get_value() <= 21:
            player.add_card(deck.deal_card())
        # if busted, assign a message to outcome, update in_play and score
        if player.get_value() > 21:
            outcome = "You are busted. You loose!"
            in_play = False
            score -= 1
        else:
            outcome = ""
        if USE_PRINT:
            print_values()


def stand():
    """ Adds cards to the dealer hand until the value is 17 or greater, then evaluates the hands values and updates
    score, balance and necessary messages and flags """
    global outcome, action, in_play, score, balance
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    if in_play:
        # add cards to the dealer hand until it has value 17 or more
        while dealer.get_value() <= 17:
            dealer.add_card(deck.deal_card())
        # check if dealer busted; update outcome and score
        if dealer.get_value() > 21:
            outcome = "Dealer is busted. You win!"
            score += 1
            balance += get_win()
        else:
            # compare the hands values; update outcome and score
            if dealer.get_value() < player.get_value():
                outcome = "You win!"
                score += 1
                balance += get_win()
            else:
                outcome = "You loose!"
                score -= 1
        # set the flag that this round is over, and update the action
        in_play = False
        action = "New deal?"
        if USE_PRINT:
            print_values()


# draw handler
def draw(canvas):
    # draw the background image
    canvas.draw_image(bg_image, BG_CENTER, BG_SIZE, BG_CENTER, BG_SIZE)
    if startup:
        # draw the welcome text and the rules if the game is just started or restarted
        canvas.draw_text(intro_head, [LEFT_MARGIN, LOC_DEALER], 27, "Black", "sans-serif")
        i = 2
        for rule in intro_rules:
            canvas.draw_text(rule, [LEFT_MARGIN, LOC_DEALER + 22 * i], 17, "Black", "sans-serif")
            i += 1
    else:
        # draw the texts and values
        canvas.draw_text("DEALER", [LEFT_MARGIN, LOC_DEALER], 21, "Black", "sans-serif")
        canvas.draw_text("PLAYER", [LEFT_MARGIN, LOC_PLAYER], 21, "Black", "sans-serif")
        canvas.draw_text("BALANCE $" + str(balance), [LEFT_MARGIN, SCORES_TOP], 21, "Black", "sans-serif")
        canvas.draw_text("BET $" + str(bet), [LOC_BET, SCORES_TOP], 21, "Black", "sans-serif")
        canvas.draw_text("SCORE " + str(score), [LOC_SCORE, SCORES_TOP], 21, "Black", "sans-serif")
        canvas.draw_text(outcome, [MID_MARGIN, LOC_DEALER], 21, get_blink_color(), "sans-serif")
        canvas.draw_text(action, [MID_MARGIN, LOC_PLAYER], 21, "Black", "sans-serif")
        # draw the cards of both player's and dealer's hand
        dealer.draw(canvas, [LEFT_MARGIN, LOC_DEALER + 10])
        player.draw(canvas, [LEFT_MARGIN, LOC_PLAYER + 10])
        # hide the first dealers card while the round still lasts
        if in_play:
            canvas.draw_image(card_back, CARD_CENTER, CARD_SIZE, [LEFT_MARGIN + CARD_SIZE[0] / 2, LOC_DEALER + CARD_SIZE[1] / 2 + 10], CARD_SIZE)


def fancy():
    """ sets both the cards and backgrounds to fancy """
    global card_images, card_back
    card_images = card_images_fancy
    card_back = card_back_fancy


def standard():
    """ sets both the cards and backgrounds to standard """
    global card_images, card_back
    card_images = card_images_standard
    card_back = card_back_standard


def reset():
    """ resets balance, bet and score and sets flag as the game has just started """
    global score, bet, temp_bet, balance, in_play, startup
    score = 0
    bet = temp_bet = 50
    balance = 1000
    bet_input.set_text(str(temp_bet))
    in_play = False
    startup = True


def get_blink_color():
    """ uses blink text variables to get the color to be displayed to simulate text blinking """
    global blink_ticks
    blink_ticks += 1
    if blink_ticks == len(blink_colors) * blink_interval:
        blink_ticks = 0
    return blink_colors[blink_ticks // blink_interval]


def set_bet(text):
    """ event handler for the input field. stores the text in temp variable if it is a number """
    global temp_bet
    try:
        temp_bet = int(text)
    except ValueError:
        bet_input.set_text(str(temp_bet))


def get_win():
    """ calculates the win based on the player score 2x if < 21 and 3x if = 21 """
    if player.get_value() == 21:
        return 3 * bet
    else:
        return 2 * bet


def print_values():
    """ prints the game values to the console """
    print("Player hand:", str(player), "value", str(player.get_value()))
    print("Dealer:", str(dealer), "value", str(dealer.get_value()))
    print("Balance:", str(balance), "Bet:", str(bet), "Score:", str(score))
    if not in_play:
        print("Outcome:", outcome)
    print("")

# initialization frame
frame = simplegui.create_frame("Blackjack", BG_SIZE[0], BG_SIZE[1])
frame.set_canvas_background("Green")

#create buttons, labels, input and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.add_label("")
frame.add_label("Select deck:")
frame.add_button("Standard", standard, 100)
frame.add_button("Fancy", fancy, 100)
frame.add_label("")
bet_input = frame.add_input("Enter your bet:", set_bet, 100)
bet_input.set_text(str(temp_bet))
frame.add_label("(changed on the next deal)")
frame.add_label("")
frame.add_button("Reset", reset, 100)
frame.set_draw_handler(draw)


# get things rolling
frame.start()


# remember to review the gradic rubric