import random
import time
def display_word(hidden, guessed):
    display = ""
    for index in range(len(hidden)):
        letter = hidden[index]
        if letter in guessed:
            display += letter
        else:
            display += "_"
    return display

def hangman():
    words = ['house', 'cat', 'chair', 'chalkboard', 'door', 'adieu', 'pygmy', 'pufferfish', 'fish', 'table']
    hidden = random.choice(words)

    maxGuess = 5
    gameover = Falsenumguesses = 0
    numguesses = 0
    guessedletters = ""
    while not gameover:
        print (display_word(hidden, guessedletters))
        guess = input("Choose a letter: ").lower()
        if len(guess) != 1:
            print ("That's not a letter")
        elif guess != "a" and guess != "b" and guess != "c" and guess != "d" and guess != "e" and guess != "f" and guess != "g" and guess != "h" and guess != "i" and guess != "j" and guess != "k" and guess != "l" and guess != "m" and guess != "n" and guess != "o" and guess != "p" and guess != "q" and guess != "r" and guess != "s" and guess != "t" and guess != "u" and guess != "v" and guess != "w" and guess != "x" and guess != "y" and guess != "z":
            print("That's not a letter")
        elif guess in guessedletters:
            print ("hey dumbass")
            time.sleep(2)
            print ("i dont know if you know this")
            time.sleep(2)
            print ("you already picked that")
            time.sleep(2)
            print ("kys")
        elif not (guess in hidden):
            print (guess + " is not in the word")
            numguesses+=1
            guessedletters+=guess
            if numguesses == maxGuess:
                gameover = True
                print ("you lost")
        if guess in hidden:
            guessedletters+=guess
            if display_word(hidden, guessedletters) == hidden:
                print (display_word(hidden, guess))
                gameover=True
                print("you win!")

hangman()
