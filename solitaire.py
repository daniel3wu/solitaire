import random
BREAK_STRING = "-------------------------------------------------------------------"

class Card():
    card_to_name = {1:"A", 2:"2", 3:"3", 4:"4", 5:"5", 6:"6", 7:"7",
                    8:"8", 9:"9", 10:"10", 11:"J", 12:"Q", 13:"K"}

    def __init__(self, value, suit):
        self.name = self.card_to_name[value]
        self.suit = suit
        self.title = "%s%s" % (self.name, self.suit)
        self.value = value

    def isBelow(self, card):
    	return self.value == (card.value + 1)

    def oppositeSuit(self, card):
    	if self.suit == "club" or self.suit == "spade":
    		return card.suit == "heart" or cards.suit == "diam"
    	else:
    		return card.suit == "spade" or cards.suit == "club"

    def canAttach(self, card):
   		if card.isBelow(self) and card.oppositeSuit(self):
   			return True

    def __repr__(self):
        return self.title

class Deck():
    unshuffled_deck = [Card(card, suit) for card in range(1, 14) for suit in ["club", "diam", "heart", "spade"]]
    def __init__(self, num_decks=1):
        self.deck = self.unshuffled_deck * num_decks
        random.shuffle(self.deck)

    def flip_card(self):
    	return self.deck.pop()

    def deal_cards(self, num_cards):
    	return [self.deck.pop() for x in range(0, num_cards)]

    def __str__(self):
    	return str(self.deck)
		
class Tableau():
	# Seven piles

	def __init__(self, card_list):
		self.piles = {x: card_list[x] for x in range(7)}
		self.revealed = {x: [self.piles[x].pop()] for x in range(7)}

	def attach_card(self, column, card):
		return -1

	def flip_card(self, col, card):
		self.revealed[col].append(self.piles[col].pop())

	def pile_length(self):
		list_lens = [len(self.revealed[x]) + len(self.piles[x]) for x in range(7)]
		return max(list_lens)

	def __repr__(self):
		return str(self.piles)

class StockWaste():
	waste = []

	def __init__(self, cards):
		self.deck = cards
		random.shuffle(self.deck)

	def flip_card(self):
		""" Move a card from the Stock pile to the Waste pile """
		if len(self.deck) == 0:
			# Reset the stock and waste after the stock runs dry
			self.waste.reverse()
			self.deck = self.waste.copy()
			self.waste.clear()
		self.waste.append(self.deck.pop())

	def remove_card(self):
		return self.waste.pop()

	def showWaste(self):
		if len(self.waste) > 0:
			return self.waste[-1]
		else:
			return "empty"

	def showStock(self):
		if len(self.deck) > 0:
			return str(len(self.deck)) + " card(s)"
		else:
			return "empty"

class Foundation():

	def __init__(self):
		self.foundation_piles = {"club":[], "heart":[], "spade":[], "diam":[]}

	def add(self, card):
		""" Adds a card to its appropriate pile"""
		stack = self.foundation_piles[card.suit]
		if len(stack) == 0 and card.value == 1:
			stack.append(card)
		elif stack[-1].isBelow(card):
			stack.append(card)
		else:
			print("Error! That card doesn't belong there.")

	def getTopCard(self, suit):
		"""
		Return the top card of a foundation pile. If the pile
		is empty, return the letter of the suit.
		"""
		pile = self.foundation_piles[suit]
		if len(pile) == 0:
			return suit[0].upper()
		else:
			return self.foundation_piles[suit][-1]

def printValidCommands():
	""" Provides the list of commands, for when users press 'h' """
	print("Valid Commands: ")
	print("\tmv - move card from Stock to Waste")
	print("\twf - move card from Waste to Foundation")
	print("\twt #T - move card from Waste to Tableau")
	print("\ttf #T - move card from Tableau to Foundation")
	print("\ttt #T1 #T2 - move card from one Tableau column to another")
	print("\th - help")
	print("\tq - quit")
	print("\t*NOTE: Hearts/diamonds are red. Spades/clubs are black.")

def printTable(tableau, foundation, stock_waste):
	""" Prints the current status of the table """
	print(BREAK_STRING)
	print("Waste \t Stock \t\t\t\t Foundation")
	print("{}\t{}\t\t{}\t{}\t{}\t{}".format(stock_waste.showWaste(), stock_waste.showStock(), 
		foundation.getTopCard("club"), foundation.getTopCard("heart"), 
		foundation.getTopCard("spade"), foundation.getTopCard("diam")))
	print("\nTableau\n\t1\t2\t3\t4\t5\t6\t7\n")
	# Print the cards, first printing the un-flipped cards, and then the flipped.
	for x in range(tableau.pile_length()):
		print_str = ""
		for col in range(7):
			hidden_cards = tableau.piles[col]
			shown_cards = tableau.revealed[col]
			if len(hidden_cards) > x:
				print_str += "\tx"
			elif len(shown_cards) + len(hidden_cards) > x:
				print_str += "\t" + str(shown_cards[x-len(hidden_cards)])
			else:
				print_str += "\t"
		print(print_str)
	print(BREAK_STRING)

if __name__ == "__main__":
    d = Deck()
    t = Tableau([d.deal_cards(x) for x in range(1,8)])
    f = Foundation()
    sw = StockWaste(d.deal_cards(24))

    print("\n" + BREAK_STRING)
    print("Welcome to Danny's Solitaire!\n")
    printValidCommands()
    printTable(t, f, sw)
    while True:
    	command = input("Enter a command (type 'h' for help): ")
    	command = command.lower()
    	command = command.replace(" ", "")
    	if command == "h":
    		printValidCommands()
    	elif command == "q":
    		print("Game exited.")
    		break
    	elif command == "mv":
    		sw.flip_card()
    		printTable(t, f, sw)
    	elif command == "wf":
    		if sw.showWaste() == "empty":
    			print("Error! There's nothing in the Waste pile.")
    		else:
    			f.add(sw.remove_card())
    			printTable(t, f, sw)
    	elif "wt" in command:
    		print("Move card from Waste to tableau")
    	elif "tf" in command:
    		print("move card from tableau to foundation")
    	elif "tt" in command:
    		print("move card from column to column")
