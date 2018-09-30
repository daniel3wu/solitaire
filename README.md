# solitaire

## Overview
This is a console-based, unix-compatible Python implementation of the popular card game Solitaire (also known as "Patience").
To play, simply run the **solitaire.py** file using Python 3.

## Rules
This implementation of Solitaire was modeled after the official rules described [here](https://www.bicyclecards.com/how-to-play/solitaire/) by Bicycle Cards.

## Edge Cases To Account For (non-exhaustive)
- Only Kings can fill up vacancies in the Tableau
- The four stacks in the Foundations must begin with the lowest value card, an Ace.
- The Stock/Waste piles loop continuously through the cards
- The game concludes when the Foundation piles are filled.
- You can move a stack of cards between columns of the Tableau, rather than just one.
- On the Tableau, if a column's revealed cards are all removed, the bottom card of the unrevealed pile is flipped.

## Design Choices
### Python
Python was used because it's flexibility in creating multiple classes in one file allowed me to implement this small game in a single file.
### Classes
The Card and Deck class were used to initialize our starting deck and distribute cards between the different spaces of the game: the Tableau, the Foundation, and the Stock/Waste pile. The Tableau class manages the 7 starting piles of cards and their interactions with the Stock/Waste and the Foundation. The Foundation class handles the placement of cards into the Foundation piles. The StockWaste class moves cards in between the Stock pile and Waste pile, and provides getters/setters for Stock and Waste piles.
### Data Structures
Piles of cards were mostly implemented using lists, which were the optimal choice because they retain the order of elements and retrieve elements quickly. A dictionary of integer keys and list values was used to organize the 7 piles on the Tableau.
