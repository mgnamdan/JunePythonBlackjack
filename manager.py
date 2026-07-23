from random import choice

from decks import Deck, UnoDeck
from players import CompBJPlayer, HumanBJPlayer, UnoPlayer, HumanUnoPlayer


class GameManager:

    def promptNextGame(self):
        while True:
            print("")
            print("Would you like to play another game? (y/n)")
            choiceMade = input(" --> ").strip().lower()
            if choiceMade in ["yes", "y"]:
                return True
            if choiceMade in ["no", "n", "quit", "exit"]:
                return False
            print("")
            print("Invalid choice - please try again!")


class BlackjackManager(GameManager):

    COMPNAMES = ["Adam", "Bob", "Cassie", "Doug", "Elizabeth", "Fred", "Gabby"]

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

    def determineWinner(self):
        scores = {}
        for player in self.players:
            score = player.giveScore()
            if score <= 21:
                scores.setdefault(score, []).append(player.name)

        if not scores:
            print("")
            print("Everyone busts! Everyone loses!")
            return

        highScore = max(scores)
        winners = scores[highScore]

        if len(winners) == 1:
            print("")
            print(f"Congratulations {winners[0]}! You win with a score of {highScore}!")
        elif self.dealer.name in winners:
            print("")
            print(f"The dealer wins with a score of {highScore}!")
        else:
            print("")
            winnerNames = ", ".join(winners[:-1]) + f" and {winners[-1]}"
            print(f"{winnerNames} tie with a score of {highScore}!")

    def playGame(self):
        gameOn = True
        while gameOn:
            self.reset()
            for player in self.players:
                self.manageTurn(player)
            self.determineWinner()
            gameOn = self.promptNextGame()


class UnoManager(GameManager):

    COMPNAMES = ["Ada", "Bruno", "Cleo", "Diego", "Evie", "Finn", "Gia"]

    def reset(self):
        self.deck = UnoDeck()
        self.players = []
        self.direction = 1
        self.currentPlayerIdx = 0

        print("")
        print("Enter your name:")
        humanName = input(" --> ").strip() or "Player"
        self.players.append(HumanUnoPlayer(humanName))

        print("")
        print("How many computer opponents? (1-3)")
        try:
            numComps = int(input(" --> ").strip())
        except ValueError:
            numComps = 1
        numComps = min(3, max(1, numComps))

        availableNames = [name for name in self.COMPNAMES if name != humanName]
        for _ in range(numComps):
            compName = choice(availableNames)
            availableNames.remove(compName)
            self.players.append(UnoPlayer(compName))

        for _ in range(7):
            for player in self.players:
                player.drawCard(self.deck.draw())

        # Start on a number so no action is resolved before the first turn.
        rejectedCards = []
        while True:
            startingCard = self.deck.draw()
            if startingCard.rank in UnoDeck.NUMBER_RANKS:
                break
            rejectedCards.append(startingCard)

        for card in rejectedCards:
            self.deck.outPile.remove(card)
            self.deck.drawPile.append(card)
        self.deck.shuffle()

        self.deck.play(startingCard)
        self.topCard = startingCard
        self.activeColor = startingCard.color

    def drawCards(self, player, amount):
        for _ in range(amount):
            player.drawCard(self.deck.draw())
        cardWord = "card" if amount == 1 else "cards"
        print(f"{player.name} draws {amount} {cardWord}.")

    def showTable(self, currentPlayer):
        print("")
        print("==================================================")
        print(f"Top card: {self.topCard}  |  Current color: {self.activeColor}")
        for player in self.players[1:]:
            print(f"{player.name}: {len(player.hand)} cards")
        print(f"It is {currentPlayer.name}'s turn.")

    def playCard(self, player, cardIdx):
        card = player.discardCard(cardIdx)
        self.deck.play(card)
        self.topCard = card

        if card.isWild:
            self.activeColor = player.chooseColor()
            print(f"{player.name} plays {card} and chooses {self.activeColor}.")
        else:
            self.activeColor = card.color
            print(f"{player.name} plays {card}.")

        if len(player.hand) == 1:
            print(f"UNO! {player.name} has one card left!")
        return card

    def manageTurn(self, player):
        cardIdx = player.makeChoice(self.topCard, self.activeColor)

        if cardIdx is None:
            drawnCard = self.deck.draw()
            player.drawCard(drawnCard)
            print(f"{player.name} draws a card.")

            if player.shouldPlayDrawnCard(drawnCard, self.topCard, self.activeColor):
                return self.playCard(player, len(player.hand) - 1)
            return None

        return self.playCard(player, cardIdx)

    def applyCardEffect(self, playedCard):
        if playedCard is None:
            return 1

        if playedCard.rank == "Reverse":
            self.direction *= -1
            print("The direction of play reverses.")
            return 2 if len(self.players) == 2 else 1

        if playedCard.rank == "Skip":
            skippedIdx = (self.currentPlayerIdx + self.direction) % len(self.players)
            print(f"{self.players[skippedIdx].name} is skipped.")
            return 2

        drawAmounts = {"Draw Two": 2, "Wild Draw Four": 4}
        if playedCard.rank in drawAmounts:
            affectedIdx = (self.currentPlayerIdx + self.direction) % len(self.players)
            affectedPlayer = self.players[affectedIdx]
            self.drawCards(affectedPlayer, drawAmounts[playedCard.rank])
            print(f"{affectedPlayer.name} loses a turn.")
            return 2

        return 1

    def playRound(self):
        self.reset()
        winner = None

        while winner is None:
            currentPlayer = self.players[self.currentPlayerIdx]
            self.showTable(currentPlayer)
            playedCard = self.manageTurn(currentPlayer)

            if not currentPlayer.hand:
                winner = currentPlayer
                break

            spacesToMove = self.applyCardEffect(playedCard)
            self.currentPlayerIdx = (
                self.currentPlayerIdx + self.direction * spacesToMove
            ) % len(self.players)

        print("")
        print(f"Congratulations {winner.name}! You win Uno!")

    def playGame(self):
        gameOn = True
        while gameOn:
            self.playRound()
            gameOn = self.promptNextGame()
