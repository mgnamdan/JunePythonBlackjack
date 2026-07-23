class Card:

    def __init__(self, rank="Two", suit="Clubs"):
        self.rank = rank
        self.suit = suit


    def __repr__(self):
        return f"{self.rank} of {self.suit}"
    

    def __str__(self):
        return f"{self.rank} of {self.suit}"
    

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        if other.rank != self.rank:
            return False
        if other.suit != self.suit:
            return False
        return True


class UnoCard(Card):
    """A card used by an Uno deck.

    ``rank`` stores the number or action and ``suit`` stores the color.  Wild
    cards have no color; the manager tracks the color chosen for the current
    discard separately so the same card can be reused in later games.
    """

    ACTIONS = ["Skip", "Reverse", "Draw Two", "Wild", "Wild Draw Four"]

    def __init__(self, rank="Zero", color="Red"):
        super().__init__(rank, color)

    @property
    def color(self):
        return self.suit

    @property
    def isWild(self):
        return self.rank in ["Wild", "Wild Draw Four"]

    def __repr__(self):
        return str(self)

    def __str__(self):
        if self.isWild:
            return self.rank
        return f"{self.color} {self.rank}"
