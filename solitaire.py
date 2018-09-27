import random

class Card():
    card_to_name = {1:"Ace", 2:"Two", 3:"Three", 4:"Four", 5:"Five", 6:"Six", 7:"Seven",
                    8:"Eight", 9:"Nine", 10:"Ten", 11:"Jack", 12:"Queen", 13:"King"}

    def __init__(self, value, suit):
        self.name = self.card_to_name[value]
        self.suit = suit
        self.title = "%s // %s" % (self.name, self.suit)
        self.value = value

    def isBelow(self, card):
    	return self.value == (card.value + 1)

    def oppositeSuit(self, card):
    	if self.suit == "c" or self.suit == "s":
    		return card.suit == "h" or cards.suit == "d"
    	else:
    		return card.suit == "s" or cards.suit == "c"

    def canAttach(self, card):
   		if card.isBelow(self) and card.oppositeSuit(self):
   			return True

    def __repr__(self):
        return self.title

class Deck():
    unshuffled_deck = [Card(card, suit) for card in range(1, 14) for suit in ["c", "d", "h", "s"]]
    def __init__(self, num_decks=1):
        self.deck = self.unshuffled_deck * num_decks
        random.shuffle(self.deck)

    def flip_card(self):
    	return self.deck.pop()

    def deal_cards(self, num_cards):
    	return [self.deck.pop() for x in range(0, num_cards)]

    def __str__(self):
    	return str(self.deck)

# Pile of cards 
class Pile(Deck):
	known_cards = []

	def __init__(self):
		self.deck = []

	def __init__(self, cards):
		self.known_cards.append(cards.pop())
		self.deck = cards

	def attach_card(self, card):
		pile_bottom = self.known_cards[-1]
		if pile_bottom.canAttach(card):
			self.known_cards.append(card)

	def attach_cards(self, cards):
		pile_bottom = self.known_cards[-1]
		attachment = cards[0]
		if pile_bottom.canAttach(attachment):
			self.known_cards.extend(cards)
		
class Tableau():
	# Seven piles
	def __init__(self, deck):
		self.hi = "hi"

class Stock(Deck):
	waste = []
	def __init__(self, cards):
		self.deck = cards
		random.shuffle(self.deck)

	def flip_card(self):
		waste.append(self.deck.pop())

class Foundation():
	foundation_piles = {"Clubs":[], "Hearts":[], "Spades":[], "Diamonds":[]}

	def __init__(self):
		self.completed = False

	def attach_card(self, card):
		stack = foundation_piles[card.suit]
		if len(stack) == 0 and card.value == 1:
			foundation_piles[card.suit].append(card)
		elif stack[len(stack)-1].isBelow(card):
			foundation_piles[card.suit].append(card)
		else:
			print("Error! That card doesn't belong there.")

def printValidCommands():
	""" Provides the list of commands, for when users press 'h' """
	print("Valid Commands: ")
	print("\tmv - move card from Stock to Waste")
	print("\twf #F - move card from Waste to Foundation")
	print("\twt #T - move card from Waste to Tableau")
	print("\ttf #T #F - move card from Tableau to Foundation")
	print("\ttt #T1 #T2 - move card from one Tableau column to another")
	print("\th - help")
	print("\tq - quit")
	print("\t*NOTE: Hearts/diamonds are red. Spades/clubs are black.")

def printTable():
	""" Prints the current status of the table """
	print("---------------------------------------------------------------------")
	print("Waste \t Stock \t\t\t Foundation")
	print("empty \t X \t\t 1 \t 2 \t 3 \t 4")
	print("\nTableau")
	print("\t1\t2\t3\t4\t5\t6\t7\n")
	print("---------------------------------------------------------------------")

if __name__ == "__main__":
    d = Deck()
    f = Foundation()
    s = Stock(d.deal_cards(14))

    print("\n-------------------------------------------------------------------")
    print("Welcome to Danny's Solitaire!\n")
    printValidCommands()
    printTable()
    while True:
    	command = input("Enter a command (type 'h' for help): ")
    	command = command.lower()
    	command = command.replace(" ", "")
    	if command == "h":
    		printValidCommands()
    	elif command == "q":
    		print("Game exited.")
    		break
