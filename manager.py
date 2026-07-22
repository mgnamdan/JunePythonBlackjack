from decks import Deck
from players import CompBJPlayer, HumanBJPlayer
from random import choice

class BlackjackManager:

    COMPNAMES = ["Adam", "Bob", "Cassie", "Doug", "Elizabeth", "Fred", "Gabby"]

    def __init__(self):
        self.reset()


    def reset(self):
        self.dealer = CompBJPlayer()
        self.players = []
        self.deck = Deck()
        self.deck.shuffle()

        print("")
        print("Enter your name: ")
        humanName = input(" --> ")
        print("")

        human = HumanBJPlayer(humanName)

        self.players.append(human)

        print("How many other computers would you like to play against? (0-4)")
        numComps = input(" --> ")

        try:
            numComps = int(numComps)
            if numComps < 0:
                numComps = 0
            if numComps > 4:
                numComps = 4
        except ValueError:
            numComps = 0

        for _ in range(numComps):
            newPlayer = CompBJPlayer(choice(self.COMPNAMES))
            self.players.append(newPlayer)

        self.players.append(self.dealer)

        for _ in range(2):
            for player in self.players:
                player.drawCard(self.deck.draw())


    def manageTurn(self, player):
        playerChoice = "hit"
        while playerChoice != "stay":
            playerChoice = player.makeChoice()
            if playerChoice == "hit":
                player.drawCard(self.deck.draw())
    

    def determineWinner(self):
        pass


    def promptNextGame(self):
        pass


    def playGame(self):
        pass