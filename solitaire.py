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
    	return self.value == (card.value - 1)

    def isOppositeSuit(self, card):
    	if self.suit == "club" or self.suit == "spade":
    		return card.suit == "heart" or card.suit == "diam"
    	else:
    		return card.suit == "spade" or card.suit == "club"

    def canAttach(self, card):
    	if card.isBelow(self) and card.isOppositeSuit(self):
    		return True
    	else:
    		return False

    def __str__(self):
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
	# Class that keeps track of the seven piles of cards on the Tableau

	def __init__(self, card_list):
		self.unflipped = {x: card_list[x] for x in range(7)}
		self.flipped = {x: [self.unflipped[x].pop()] for x in range(7)}

	def flip_card(self, col):
		""" Flips a card under column col on the Tableau """
		if len(self.unflipped[col]) > 0:
			self.flipped[col].append(self.unflipped[col].pop())

	def pile_length(self):
		""" Returns the length of the longest pile on the Tableau """
		return max([len(self.flipped[x]) + len(self.unflipped[x]) for x in range(7)])

	def addCards(self, cards, column):
		""" Returns true if cards were successfully added to column on the Tableau. 
			Returns false otherwise. """
		column_cards = self.flipped[column]
		if len(column_cards) == 0 and cards[0].value == 13:
			column_cards.extend(cards)
			return True
		elif len(column_cards) > 0 and column_cards[-1].canAttach(cards[0]):
			column_cards.extend(cards)
			return True
		else:
			return False

	def tableau_to_tableau(self, c1, c2):
		""" Returns True if any card(s) are successfully moved from c1 to c2 on
			the Tableau, returns False otherwise. """
		c1_cards = self.flipped[c1]

		for index in range(len(c1_cards)):
			if self.addCards(c1_cards[index:], c2):
				self.flipped[c1] = c1_cards[0:index]
				if index == 0:
					self.flip_card(c1)
				return True
		return False

	def tableau_to_foundation(self, foundation, column):
		""" Moves a card from the Tableau to the appropriate Foundation pile """
		column_cards = self.flipped[column]
		if len(column_cards) == 0:
			return False

		if foundation.addCard(column_cards[-1]):
			column_cards.pop()
			if len(column_cards) == 0:
				self.flip_card(column)
			return True
		else:
			return False

	def waste_to_tableau(self, waste_pile, column):
		""" Returns True if a card from the Waste pile is succesfully moved to a column
			on the Tableau, returns False otherwise. """
		card = waste_pile.waste[-1]
		if self.addCards([card], column):
			waste_pile.pop_waste_card()
			return True
		else:
			return False

class StockWaste():
	""" A StockWaste object keeps track of the Stock and Waste piles """

	def __init__(self, cards):
		self.deck = cards
		self.waste = []

	def stock_to_waste(self):
		""" Returns True if a card is sucessfully moved from the Stock pile to the
			Waste pile, returns False otherwise. """
		if len(self.deck) + len(self.waste) == 0:
			print("There are no more cards in the Stock pile!")
			return False

		if len(self.deck) == 0:
			self.waste.reverse()
			self.deck = self.waste.copy()
			self.waste.clear()

		self.waste.append(self.deck.pop())
		return True

	def pop_waste_card(self):
		""" Removes a card from the Waste pile. """
		if len(self.waste) > 0:
			return self.waste.pop()

	def getWaste(self):
		""" Retrieves the top card of the Waste pile. """
		if len(self.waste) > 0:
			return self.waste[-1]
		else:
			return "empty"

	def getStock(self):
		""" Returns a string of the number of cards in the stock. """
		if len(self.deck) > 0:
			return str(len(self.deck)) + " card(s)"
		else:
			return "empty"

class Foundation():

	def __init__(self):
		self.foundation_stacks = {"club":[], "heart":[], "spade":[], "diam":[]}

	def addCard(self, card):
		""" Returns True if a card is successfully added to the Foundation,
			otherwise, returns False. """
		stack = self.foundation_stacks[card.suit]
		if (len(stack) == 0 and card.value == 1) or stack[-1].isBelow(card):
			stack.append(card)
			return True
		else:
			return False

	def getTopCard(self, suit):
		""" Return the top card of a foundation pile. If the pile
			is empty, return the letter of the suit."""
		stack = self.foundation_stacks[suit]
		if len(stack) == 0:
			return suit[0].upper()
		else:
			return self.foundation_stacks[suit][-1]

	def gameWon(self):
		""" Returns whether the user has won the game. """
		for suit, stack in self.foundation_stacks.items():
			if len(stack) == 0:
				return False
			card = stack[-1]
			if card.value != 13:
				return False
		return True

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
	print("{}\t{}\t\t{}\t{}\t{}\t{}".format(stock_waste.getWaste(), stock_waste.getStock(), 
		foundation.getTopCard("club"), foundation.getTopCard("heart"), 
		foundation.getTopCard("spade"), foundation.getTopCard("diam")))
	print("\nTableau\n\t1\t2\t3\t4\t5\t6\t7\n")
	# Print the cards, first printing the unflipped cards, and then the flipped.
	for x in range(tableau.pile_length()):
		print_str = ""
		for col in range(7):
			hidden_cards = tableau.unflipped[col]
			shown_cards = tableau.flipped[col]
			if len(hidden_cards) > x:
				print_str += "\tx"
			elif len(shown_cards) + len(hidden_cards) > x:
				print_str += "\t" + str(shown_cards[x-len(hidden_cards)])
			else:
				print_str += "\t"
		print(print_str)
	print("\n"+BREAK_STRING)

if __name__ == "__main__":
    d = Deck()
    t = Tableau([d.deal_cards(x) for x in range(1,8)])
    f = Foundation()
    sw = StockWaste(d.deal_cards(24))

    print("\n" + BREAK_STRING)
    print("Welcome to Danny's Solitaire!\n")
    printValidCommands()
    printTable(t, f, sw)

    while not f.gameWon():
    	command = input("Enter a command (type 'h' for help): ")
    	command = command.lower().replace(" ", "")
    	if command == "h":
    		printValidCommands()
    	elif command == "q":
    		print("Game exited.")
    		break
    	elif command == "mv":
    		if sw.stock_to_waste():
    			printTable(t, f, sw)
    	elif command == "wf":
    		if f.addCard(sw.getWaste()):
    			sw.pop_waste_card()
    			printTable(t, f, sw)
    		else:
    			print("Error! No card could be moved from the Waste to the Foundation.")
    	elif "wt" in command and len(command) == 3:
    		col = int(command[-1]) - 1
    		if t.waste_to_tableau(sw, col):
    			printTable(t, f, sw)
    		else:
    			print("Error! No card could be moved from the Waste to the Tableau column.")
    	elif "tf" in command and len(command) == 3:
    		col = int(command[-1]) - 1
    		if t.tableau_to_foundation(f, col):
    			printTable(t, f, sw)
    		else:
    			print("Error! No card could be moved from the Tableau column to the Foundation.")
    	elif "tt" in command and len(command) == 4:
    		c1, c2 = int(command[-2]) - 1, int(command[-1]) - 1
    		if t.tableau_to_tableau(c1, c2):
    			printTable(t, f, sw)
    		else:
    			print("Error! No card could be moved from that Tableau column.")
    	else:
    		print("Sorry, that is not a valid command.")

    if f.gameWon():
    	print("Congratulations! You've won!")