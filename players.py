class CompBJPlayer:

    CARDVALUES = {"Two": 2, "Three": 3, "Four": 4, "Five": 5, "Six": 6, "Seven": 7,
                  "Eight": 8, "Nine": 9, "Ten": 10, "Jack": 10, "Queen": 10, "King": 10, "Ace": 11}
    
    def __init__(self, name="Dealer"):
        self.name = name
        self.hand = []
        self.score = 0


    def __repr__(self):
        return f"{self.name}"
    

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        if other.name != self.name:
            return False
        if len(other.hand) != len(self.hand):
            return False
        for idx in range(len(self.hand)):
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


class UnoPlayer:
    """Computer-controlled Uno player and base class for a human player."""

    def __init__(self, name="Computer"):
        self.name = name
        self.hand = []

    def __repr__(self):
        return self.name

    def drawCard(self, card):
        self.hand.append(card)

    def discardCard(self, cardIdx):
        return self.hand.pop(cardIdx)

    def canPlay(self, card, topCard, activeColor):
        if card.rank == "Wild":
            return True
        if card.rank == "Wild Draw Four":
            # Officially this card can only be played when no card in the hand
            # matches the current color.
            return not any(
                handCard.color == activeColor
                for handCard in self.hand
                if not handCard.isWild
            )
        return card.color == activeColor or card.rank == topCard.rank

    def playableCardIndexes(self, topCard, activeColor):
        return [
            idx for idx, card in enumerate(self.hand)
            if self.canPlay(card, topCard, activeColor)
        ]

    def makeChoice(self, topCard, activeColor):
        """Choose a playable card, preferring actions and matching colors."""
        playable = self.playableCardIndexes(topCard, activeColor)
        if not playable:
            return None

        def cardPriority(cardIdx):
            card = self.hand[cardIdx]
            actionScore = 1 if card.rank in card.ACTIONS else 0
            colorScore = sum(
                1 for handCard in self.hand if handCard.color == card.color
            )
            return actionScore, colorScore

        return max(playable, key=cardPriority)

    def shouldPlayDrawnCard(self, card, topCard, activeColor):
        return self.canPlay(card, topCard, activeColor)

    def chooseColor(self):
        colorCounts = {color: 0 for color in ["Red", "Yellow", "Green", "Blue"]}
        for card in self.hand:
            if card.color in colorCounts:
                colorCounts[card.color] += 1
        return max(colorCounts, key=colorCounts.get)

    def showHand(self):
        print(f"{self.name} has {len(self.hand)} cards.")


class HumanUnoPlayer(UnoPlayer):
    def showHand(self):
        print("")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print(f"                 {self.name}'s Hand")
        print("")
        for idx, card in enumerate(self.hand):
            print(f"              {idx + 1}. {card}")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    def makeChoice(self, topCard, activeColor):
        while True:
            self.showHand()
            print(f"Top card: {topCard}  |  Current color: {activeColor}")
            print("Choose a card number, or D to draw a card.")
            choice = input(" --> ").strip().lower()

            if choice in ["d", "draw"]:
                return None

            try:
                cardIdx = int(choice) - 1
            except ValueError:
                print("Invalid choice - please try again!")
                continue

            if cardIdx < 0 or cardIdx >= len(self.hand):
                print("That card number is not in your hand.")
            elif not self.canPlay(self.hand[cardIdx], topCard, activeColor):
                print("That card cannot be played on the current discard.")
            else:
                return cardIdx

    def shouldPlayDrawnCard(self, card, topCard, activeColor):
        if not self.canPlay(card, topCard, activeColor):
            return False

        while True:
            print(f"You drew {card}. Would you like to play it? (y/n)")
            choice = input(" --> ").strip().lower()
            if choice in ["yes", "y"]:
                return True
            if choice in ["no", "n"]:
                return False
            print("Invalid choice - please try again!")

    def chooseColor(self):
        colors = ["Red", "Yellow", "Green", "Blue"]
        while True:
            print("Choose a color: Red, Yellow, Green, or Blue")
            choice = input(" --> ").strip().title()
            if choice in colors:
                return choice
            print("Invalid color - please try again!")
