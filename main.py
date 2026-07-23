# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# HELPER FUNCTIONS AND IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from manager import BlackjackManager, UnoManager


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# MAIN FUNCTION DEFINITION
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def main():
    games = {
        "1": ("Blackjack", BlackjackManager),
        "2": ("Uno", UnoManager),
    }

    while True:
        print("")
        print("==================================================")
        print("                 CARD GAMES")
        print("==================================================")
        for gameNumber, (gameName, _) in games.items():
            print(f"                 {gameNumber}. {gameName}")
        print("                 Q. Quit")
        print("")
        print("Choose a game:")

        selection = input(" --> ").strip().lower()
        if selection in ["q", "quit", "exit"]:
            print("Thanks for playing!")
            break

        if selection not in games:
            print("Invalid choice - please try again!")
            continue

        _, managerClass = games[selection]
        gameManager = managerClass()
        gameManager.playGame()


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# MAIN FUNCTION CALL
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == "__main__":
    main()
