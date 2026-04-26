"""
    Final Project for CMPSC 132
    Number Guessing Game
    Enhancements to the original idea:
    1) Replayability
    2) Player Statistics (Wins, Losses, Total games played)
    3) Difficulty Levels
    4) Limiting Attempts
    5) Complete player history tracking
"""
import random

class Player:
    def __init__(self):
        self.gamesPlayed = 0
        self.wins = 0
        self.losses = 0
        self.replaying = False
        self.history = []

    def play(self):
        #creates an instance of Game
        currentGame = Game(self)
        replay = currentGame.startGame(self.replaying)
        return replay
    
    def getHistory(self):
        print("Player History:")
        i = 1
        for d in self.history:
            print(f"Game {i}: {d}\n")
            i += 1


class Game:

    def __init__(self, Player):
        self.player = Player
        self.difficulty = None
        self.number = None
        self.currentGuesses = 0
        self.remainingGuesses = 0
        self.maxGuesses = 0
        #each key is a difficulty, with values of a dict
        #guesses is the number of guesses based on the difficulty
        #size is the highest integer that can be chosen by the random number generator
        self.difficultyDict = {"Easy":{"Guesses": 10, "Size": 100}, "Medium":{"Guesses":7, "Size": 200}, "Hard":{"Guesses": 5, "Size":500}}

    def startGame(self, replaying):
        #initialize stats to 0 because of replay
        self.difficulty = None
        self.number = None
        self.currentGuesses = 0
        self.remainingGuesses = 0
        self.maxGuesses = 0
        self.player.history.append({})
        if not replaying:
            #explain the game
            print("In this game, you will guess the number randomly selected by a random number generator.\n" \
            "The Number will always be a positive integer.\n" \
            "The difficulty levels are as follows:\n" \
            "-> Easy, where the number can range from 1 to 100 and you get 10 guesses\n" \
            "-> Medium, where the number can range form 1 to 200 and you get 7 guesses\n" \
            "-> Hard, where the number can range from 1 to 500 and you get 5 guesses\n")
        #gather user input on what difficulty they want to play
        userInput = input("Select Difficulty (Easy, Medium, Hard): ")
        while userInput != "Easy" and userInput != "Medium" and userInput != "Hard":
            #ensure valid user input
            print("You did not enter a valid difficulty, please reenter.")
            userInput = input("Select Difficulty (Easy, Medium, Hard): ")
        self.difficulty = userInput
        #confirm difficulty
        print(f"You selected {self.difficulty}.")
        replay = self.setupGame()
        #return for call stack
        return replay

    def setupGame(self):
        #initialize guesses based on difficulty level they selected, generate number based on that 
        self.maxGuesses = self.remainingGuesses = self.difficultyDict[self.difficulty]["Guesses"]
        self.number = random.randint(1, self.difficultyDict[self.difficulty]["Size"]) 
        replay = self.play()
        return replay

    def displayGameStats(self):
        print(f"\nDifficulty: {self.difficulty}\nRemaining Guesses: {self.remainingGuesses}\nAttempts: {self.currentGuesses}\n")
    
    def processGuess(self, guess):
        self.remainingGuesses -= 1
        self.currentGuesses += 1
        int_guess = None
        self.player.history[self.player.gamesPlayed][f"Guess {self.currentGuesses}"] = guess #save to player history
        try:
            int_guess = int(guess)
        except:
            print("Invalid Guess (invalid value).")
            return "incorrect"
        if "." in guess and guess.isnumeric(): #stated that the guess needs to be a positive integer, float not allowed
            print("Invalid Guess (only positive integers).")
            print("------------------------------")
            return "incorrect"
        elif int_guess == self.number:
            print(f"Your guess {guess} was correct!") # required feedback
            return "correct"
        elif int_guess > self.number:
            print("Too High!") #required feedback
            print("------------------------------")
        elif int_guess <= 0:
            #explicity stated a positive integer is needed
            print("Invalid Guess (only positive integers).")
            print("------------------------------")
        else:
            print("Too Low!") #required feedback
            print("------------------------------")
        return "incorrect"
    
    def win(self):
        #update the players stats
        self.player.wins += 1
        self.player.gamesPlayed += 1
        print(f"\nCongradulations! You won!\nThe correct number is {self.number}.\nYou guessed the number in {self.currentGuesses} guesses.\nYour record is now {self.player.wins} win(s) and {self.player.losses} loss(es).\n")
        replay = input("Play again (Yes/No): ") #gather input based on if the player wants to replay
        if replay not in ["Yes", "No"]:
            while replay not in ["Yes", "No"]:
                print("Invalid Input!")
                replay = input("Play again (Yes/No): ")
        if replay == "Yes":
            #return True to the play function, sends to main, reactivates play to start a new round.
            return True
        else:
            #player doesnt want to replay, display session stas
            print(f"Session concluded with {self.player.wins} win(s) and {self.player.losses} loss(es).")
            return False
    
    def lose(self):
        #updat player stats
        self.player.losses += 1
        self.player.gamesPlayed += 1
        print(f"\nYou lost!\nThe correct number is {self.number}.\nYour record is now {self.player.wins} win(s) and {self.player.losses} loss(es).\n")
        replay = input("Play again (Yes/No): ") #gather inputs from the player to determine if to replay
        if replay not in ["Yes", "No"]:
            while replay not in ["Yes", "No"]:
                print("Invalid Input!")
                replay = input("Play again (Yes/No): ")
        if replay == "Yes":
            #return true to play, causes another iteration of the while loop in main, calls play again for a fresh game
            return True
        else:
            #player doesnt want to play again, show session stats and break the while loop in main
            print(f"Session concluded with {self.player.wins} win(s) and {self.player.losses} loss(es).")
            return False

    def play(self):
        print("\n----> Game Starting <----")
        cont = True #used for when they player loses
        replay = False #chosen by the player after a game concludes
        while self.remainingGuesses and cont:
            self.displayGameStats() #show the game stats every turn
            userInput = input("Enter your guess (Positive Integer): ")
            result = self.processGuess(userInput) #sent to processGuess
            if result == "correct":
                #correct guess activates win
                replay = self.win()
                cont = False
            elif self.remainingGuesses == 0:
                replay = self.lose()
                cont = False
        #return to replay in main to tell if the player wants to replay
        return replay
        
user = Player()
replay = True
while replay:
    #lose/win return True or False depending on user input
    replay = user.play()
    if replay:
        user.replaying = True
user.getHistory()