class CompBJPlayer:

    CARDVALUES = {"Two": 2, "Three": 3, "Four": 4, "Five": 5, "Six": 6, "Seven": 7,
                  "Eight": 8, "Nine": 9, "Ten": 10, "Jack": 10, "Queen": 10, "King": 10, "Ace": 11}
    
    def __init__(self, name="Dealer"):
        self.name = name
        self.hand = []
        self.score = 0


    def repr(self):
        return f"{self.name}"
    

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        if other.name != self.name:
            return False
        if len(other.hand) != len(self.hand):
            return False
        for idx in self.hand:
            if other.hand[idx] != self.hand[idx]:
                return False
        if other.giveScore() != self.giveScore():
            return False
        return True
    

    def drawCard(self, card):
        self.hand.append(card)

    
    def discardCard(self, cardIdx):
        return self.hand.pop(cardIdx)
    

    def showHand(self):
        print("")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("")
        print(f"             {self.name}'s Hand")
        print("")
        if len(self.hand) > 0:
            print("              1. [???] of [???]")
            for idx in range(1, len(self.hand)):
                print(f"              {idx+1}. {self.hand[idx]}")
        else:
            print("               No cards in hand!")
        print("")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("")


    def giveScore(self):
        self.calcScore()
        return self.score


    def calcScore(self):
        aces = 0
        score = 0
        if len(self.hand) == 0:
            self.score = score
        else:
            for card in self.hand:
                if card.rank == "Ace":
                    aces += 1
                score += self.CARDVALUES[card.rank]
            while score > 21 and aces > 0:
                score -= 10
                aces -= 1
            self.score = score


    def makeChoice(self):
        if self.giveScore() < 17:
            return "hit"
        else:
            return "stay"
        

class HumanBJPlayer(CompBJPlayer):

    def showHand(self):
        print("")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("")
        print(f"             {self.name}'s Hand")
        print("")
        if len(self.hand) > 0:
            for idx in range(len(self.hand)):
                print(f"              {idx+1}. {self.hand[idx]}")
        else:
            print("               No cards in hand!")
        print("")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("")


    def makeChoice(self):
        if self.giveScore() >= 21 or len(self.hand) >= 5:
            return "stay"
        else:
            validChoice = False
            while not validChoice:
                self.showHand()
                print("Would you like to hit or stay?")
                choice = input(" --> ").lower()
                if choice in ["hit", "h"]:
                    validChoice = True
                    choice = "hit"
                elif choice in ["stay", "s"]:
                    validChoice = True
                    choice = "stay"
                else:
                    print("Invalid choice - choose again!")
            return choice