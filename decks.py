from cards import Card
from random import shuffle

class Deck:

    RANKS = ["Two", "Three", "Four", "Five", "Six", "Seven",
             "Eight", "Nine", "Ten", "Jack", "Queen", "King", "Ace"]
    SUITS = ["Clubs", "Hearts", "Spades", "Diamonds"]

    def __init__(self, numDecks=1):
        self.numDecks = numDecks
        self.reset(self.numDecks)


    def reset(self, numDecks):
        self.drawPile = []
        self.discardPile = []
        self.outPile = []
        for _ in range(numDecks):
            for suit in self.SUITS:
                for rank in self.RANKS:
                    newCard = Card(rank, suit)
                    self.drawPile.append(newCard)


    def draw(self):
        drawnCard = self.drawPile.pop(0)
        self.outPile.append(drawnCard)
        return drawnCard


    def discard(self, toDiscard):
        if toDiscard in self.outPile:
            self.outPile.remove(toDiscard)
            self.discardPile.append(toDiscard)


    def shuffle(self):
        shuffle(self.drawPile)
