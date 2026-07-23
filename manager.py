from decks import Deck
from players import CompBJPlayer, HumanBJPlayer
from random import choice

class BlackjackManager:

    COMPNAMES = ["Adam", "Bob", "Cassie", "Doug", "Elizabeth", "Fred", "Gabby"]

    def __init__(self):
        self.playGame()



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

        usedNames = []

        for _ in range(numComps):
            validName = False
            while not validName:
                newName = choice(self.COMPNAMES)
                if newName not in usedNames:
                    usedNames.append(newName)
                    newPlayer = CompBJPlayer(newName)
                    self.players.append(newPlayer)
                    validName = True

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
    


    def promptNextGame(self):
        validChoice = False
        while not validChoice:
            print("")
            print("Would you like to play another game? (y/n)")
            choice = input(" --> ").lower()
            if choice in ["yes", "y"]:
                choice = True
                validChoice = True
            elif choice in ["no", "n", "quit", "exit"]:
                choice = False
                validChoice = True
            else:
                print("")
                print("Invalid choice - please try again!")
        return choice



    def determineWinner(self):
        # Dealer has 21 -> dealer wins; beats everyone
        # Anyone else has 21 -> they win (ties can happen)
        # Nobody has 21:
        #     1 high score -> they win
        #     multiple high scores -> they tie or dealer wins if present
        # Everyone busts -> nobody wins
        scores = {}
        for player in self.players:
            score = player.giveScore()
            if score <= 21:
                if score in scores.keys():
                    scores[score].append(player.name)
                else:
                    scores[score] = [player.name]

        scoreList = []
        for pts in scores.keys():
            scoreList.append(pts)
        scoreList.sort()
        highScore = scoreList[-1]
        winners = scores[highScore]

        if len(winners) == 0:
            print("")
            print("Everyone busts! Everyone loses!")
        elif len(winners) == 1:
            print("")
            print(f"Congratulations {winners[0]}! You win with a score of {highScore}!")
        else:
            if self.dealer in winners:
                print("")
                print(f"The dealer wins with a score of {highScore}!")
            else:
                print("")
                message = ""
                for idx in range(len(winners)):
                    if idx == len(winners) - 1:
                        message += f" and {player.name} win with a score of {highScore}!"
                    else: 
                        message += f"{player.name}, "
                print(message)



    def playGame(self):
        gameOn = True
        while gameOn:
            self.reset()
            for player in self.players:
                self.manageTurn(player)
            self.determineWinner()
            gameOn = self.promptNextGame()