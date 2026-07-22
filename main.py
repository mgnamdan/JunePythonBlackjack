# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# HELPER FUNCTIONS AND IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from cards import Card



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# MAIN FUNCTION DEFINITION
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def main():
    testDeck = Deck()
    testPlayer = CompBJPlayer()
    testPlayer2 = HumanBJPlayer()

    card1 = Card("Jack", "Hearts")
    card2 = Card("Eight", "Spades")
    card3 = Card("Seven", "Clubs")
    card4 = Card()
    card5 = Card()
    card6 = Card()

    testPlayer2.drawCard(card1)
    testPlayer2.drawCard(card2)

    print(f"choice = {testPlayer2.makeChoice()}")

    testPlayer2.drawCard(card3)

    print(f"choice = {testPlayer2.makeChoice()}")

    testPlayer2.discardCard(0)

    testPlayer2.drawCard(card4)
    testPlayer2.drawCard(card5)
    testPlayer2.drawCard(card6)

    print(f"choice = {testPlayer2.makeChoice()}")


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# MAIN FUNCTION CALL
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == "__main__":
    main()
