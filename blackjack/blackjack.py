# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0
deck = None
dealer = None
player = None
dealer_score = 0
player_score = 0
outcome = ''
t_player = 0
t_dealer = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


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
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
            # create Hand object
            self.cards = []
            self.value = 0

    def __str__(self):
            # return a string representation of a hand
            st = "Hand contains "
            for card in self.cards:
                st = st +" "+ card.get_suit()+card.get_rank()
            return st

    def add_card(self, card):
            # add a card object to a hand
            self.cards.append(card)
            
    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
            # compute the value of the hand, see Blackjack video
            value = 0
            no_of_ace = 0
            for card in self.cards:
                card_value = VALUES[card.get_rank()]
                value += card_value
                if card_value==1:
                    no_of_ace+=1
            if no_of_ace ==0:
                return value
            else:
                if value+10<=21:
                    return value+10
                else:
                    return value
   
    def draw(self, canvas, pos):
            # draw a hand on the canvas, use the draw method for cards
            for card in self.cards:
                card.draw(canvas, pos)
                pos[0] += 75
 
        
# define deck class 
class Deck:
    def __init__(self):
            # create a Deck object
            self.cards = []
            for suit in SUITS:
                for rank in RANKS:
                    card = Card(suit,rank)
                    self.cards.append(card)
                    

    def shuffle(self):
        # add cards back to deck and shuffle
            # use random.shuffle() to shuffle the deck
            random.shuffle(self.cards)

    def deal_card(self):
            # deal a card object from the deck
            return self.cards.pop(0)
    
    def __str__(self):
            # return a string representing the deck
            st = "Deck contains "
            for card in self.cards:
                st = st +" "+ card.get_suit()+card.get_rank()

            return st



#define event handlers for buttons
def deal():
  
    global outcome, in_play, player_score, dealer_score, t_dealer
    if in_play == True:
        t_dealer += 1
        
    init()
    print "======New game====="
    # your code goes here
    deck.shuffle()
    dealer.add_card(deck.deal_card())
    dealer.add_card(deck.deal_card())
    player.add_card(deck.deal_card())
    player.add_card(deck.deal_card())
    
    #debugging info
    print "Dealer hand:" + str(dealer)
    print "Dealer score:" + str(dealer.get_value())
    dealer_score = dealer.get_value()
    
    print "Player hand:" + str(player)
    print "Player score:" + str(player.get_value())
    player_score = player.get_value()
    
      
    in_play = True
    
def hit():
        # replace with your code below
 
    # if the hand is in play, hit the player
    global player_score, in_play,outcome, t_player, t_dealer
    if in_play == True:
        if player.get_value() <= 21:
            player.add_card(deck.deal_card())
            player_score = player.get_value()
        if player.get_value() >21:
            print "You have busted: " + str(player)
            print "Player score: "+ str(player.get_value())
            in_play = False
            outcome ="You have busted"
            t_dealer += 1
        else:
            print "Player hand:"+str(player)
            print "Player score: "+ str(player.get_value())
            
    # if busted, assign a message to outcome, update in_play and score
       
def stand():
        # replace with your code below
    global in_play, dealer_score,outcome,t_dealer, t_player
    #if dealer_score >= 17:
    #    print "Dealer is busted!"
    #    in_play = False
    if player_score <= dealer_score:
        print "Dealer wins!"
        in_play = False
        outcome ="Dealer wins!"
        t_dealer += 1
        return None
    
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    if in_play == True:
        while(True):
            dealer.add_card(deck.deal_card())
            dealer_score = dealer.get_value() 
            print "Dealer hand:" + str(dealer)
            print "Dealer score: "+str(dealer.get_value())
            if dealer.get_value()>17:
                break
            if player_score <= dealer_score:
                print "Dealer wins!"
                outcome ="Dealer wins!"
                in_play = False
                t_dealer += 1
                
        if dealer.get_value() >= 17:
            print "Dealer is busted! Player wins!"
            outcome ="Dealer busted!"
            in_play = False
            t_player += 1
    else:
        print "Start a new game by clicking 'Deal'!"
        #outcome = "Start a new game by clicking 'Deal'!"
        
    # assign a message to outcome, update in_play and score

# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    
    #card = Card("S", "A")
    #card.draw(canvas, [300, 300])
    canvas.draw_text("BlackJack",[200,40],40,"White")
    
    canvas.draw_text("Player's hand",[60,80],40,"White")
    player.draw(canvas,[60,100])
    
    canvas.draw_text("Dealer's hand",[50,280],40,"White")
    dealer.draw(canvas,[50,300])
    if in_play == True:
        canvas.draw_image(card_back, [CARD_BACK_CENTER[0] ,CARD_BACK_CENTER[1] ], CARD_BACK_SIZE, [50 + CARD_BACK_CENTER[0], 300 + CARD_BACK_CENTER[1]], CARD_BACK_SIZE)
    
    canvas.draw_text("Player's score: "+str(player_score),[50,440],40,"White")
    canvas.draw_text("Dealer's score: "+str(dealer_score),[50,490],40,"White")

    canvas.draw_text(outcome,[60,590],40,"White")
    canvas.draw_text("Player: "+str(t_player),[350,440],40,"White")
    canvas.draw_text("Dealer: "+str(t_dealer),[350,490],40,"White")
def init():
    global deck, dealer, player,outcome
    deck = Deck()
    dealer = Hand()
    player = Hand()
    outcome = ''

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

init()

# get things rolling
frame.start()


# remember to review the gradic rubric
