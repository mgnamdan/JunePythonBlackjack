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
    