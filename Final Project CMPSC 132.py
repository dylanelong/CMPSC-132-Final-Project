import random

class Player:
    def __init__(self):
        self.gamesPlayed = 0
        self.wins = 0
        self.losses = 0

    def play(self):
        currentGame = Game(self)
        replay = currentGame.startGame()
        return replay

class Game:

    def __init__(self, Player):
        self.player = Player
        self.difficulty = None
        self.number = None
        self.currentGuesses = 0
        self.remainingGuesses = 0
        self.maxGuesses = 0
        self.difficultyDict = {"Easy":{"Guesses": 20, "Size": 100}, "Medium":{"Guesses":10, "Size": 200}, "Hard":{"Guesses": 15, "Size":500}}

    def startGame(self):
        self.difficulty = None
        self.number = None
        self.currentGuesses = 0
        self.remainingGuesses = 0
        self.maxGuesses = 0
        userInput = input("Select Difficulty (Easy, Medium, Hard): ")
        while userInput != "Easy" and userInput != "Medium" and userInput != "Hard":
            print("You did not enter a valid difficulty, please reenter.")
            userInput = input("Select Difficulty (Easy, Medium, Hard): ")
        self.difficulty = userInput
        print(f"You selected {self.difficulty}.")
        replay = self.setupGame()
        return replay

    def setupGame(self):
        self.maxGuesses = self.remainingGuesses = self.difficultyDict[self.difficulty]["Guesses"]
        self.number = random.randint(1, self.difficultyDict[self.difficulty]["Size"])
        replay =self.play()
        return replay

    def displayGameStats(self):
        print(f"\nDifficulty: {self.difficulty}\nRemaining Guesses: {self.remainingGuesses}\nAttempts: {self.currentGuesses}\n")
    
    def processGuess(self, guess):
        self.remainingGuesses -= 1
        self.currentGuesses += 1
        try:
            guess = float(guess)
        except:
            print("Invalid Guess.")
            return "incorrect"
        if float(guess) == float(self.number):
            print(f"Your guess {guess} was correct.")
            return "correct"
        elif float(guess) > float(self.number):
            print("------------------------------")
            print("Too High!")
        else:
            print("------------------------------")
            print("Too Low!")
        return "incorrect"
    
    def win(self):
        self.player.wins += 1
        self.player.gamesPlayed += 1
        print(f"\nYou won!\nThe correct number is {self.number}.\nYou guesses the number in {self.currentGuesses} guesses.\nYour record is now {self.player.wins} win(s) and {self.player.losses} loss(es).\n")
        replay = input("Play again (Yes/No): ")
        if replay not in ["Yes", "No"]:
            while replay not in ["Yes", "No"]:
                print("Invalid Input!")
                replay = input("Play again (Yes/No): ")
        if replay == "Yes":
            return True
        else:
            print(f"Session concluded with {self.player.wins} win(s) and {self.player.losses} loss(es).")
            return False
    
    def lose(self):
        self.player.losses += 1
        self.player.gamesPlayed += 1
        print(f"\nYou lost!\nThe correct number is {self.number}.\nYour record is now {self.player.wins} win(s) and {self.player.losses} loss(es).\n")
        replay = input("Play again (Yes/No): ")
        if replay not in ["Yes", "No"]:
            while replay not in ["Yes", "No"]:
                print("Invalid Input!")
                replay = input("Play again (Yes/No): ")
        if replay == "Yes":
            return True
        else:
            print(f"Session concluded with {self.player.wins} win(s) and {self.player.losses} loss(es).")
            return False

    def play(self):
        print("----> Game Starting <----")
        cont = True
        replay = False
        while self.remainingGuesses and cont:
            self.displayGameStats()
            userInput = input("Enter your guess: ")
            result = self.processGuess(userInput)
            if result == "correct":
                replay = self.win()
            elif self.remainingGuesses == 0:
                replay = self.lose()
                cont = False
        return replay
        
user = Player()
replay = True
while replay:
    replay = user.play()