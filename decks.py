from cards import Card, UnoCard
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
        self.shuffle()


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


class UnoDeck(Deck):
    COLORS = ["Red", "Yellow", "Green", "Blue"]
    NUMBER_RANKS = ["Zero", "One", "Two", "Three", "Four", "Five",
                    "Six", "Seven", "Eight", "Nine"]
    ACTION_RANKS = ["Skip", "Reverse", "Draw Two"]

    def __init__(self):
        self.numDecks = 1
        self.reset()

    def reset(self, numDecks=1):
        self.drawPile = []
        self.discardPile = []
        self.outPile = []

        for color in self.COLORS:
            # There is one zero and two of every other number per color.
            self.drawPile.append(UnoCard("Zero", color))
            for rank in self.NUMBER_RANKS[1:]:
                for _ in range(2):
                    self.drawPile.append(UnoCard(rank, color))

            for rank in self.ACTION_RANKS:
                for _ in range(2):
                    self.drawPile.append(UnoCard(rank, color))

        for _ in range(4):
            self.drawPile.append(UnoCard("Wild", None))
            self.drawPile.append(UnoCard("Wild Draw Four", None))

        self.shuffle()

    def draw(self):
        if not self.drawPile:
            self.recycleDiscards()
        if not self.drawPile:
            raise RuntimeError("There are no Uno cards left to draw.")

        drawnCard = self.drawPile.pop(0)
        self.outPile.append(drawnCard)
        return drawnCard

    def play(self, card):
        """Move a card from a player's hand area to the discard pile."""
        self.discard(card)

    def recycleDiscards(self):
        """Shuffle used cards back in while leaving the top discard visible."""
        if len(self.discardPile) <= 1:
            return

        topCard = self.discardPile.pop()
        self.drawPile.extend(self.discardPile)
        self.discardPile = [topCard]
        self.shuffle()
