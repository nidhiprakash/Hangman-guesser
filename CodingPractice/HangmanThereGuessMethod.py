import random

## uncomment prints and use user input guess for game version

def build_dictionary(dictionary_file_location):
    text_file = open(dictionary_file_location, "r")
    full_dictionary = text_file.read().splitlines()
    text_file.close()
    return full_dictionary

def buildFrequencyTable(full_dictionary):

    frequencyTable = [wordSize for wordSize in range(44)]
    wordLengths = {length: {character: 0 for character in 'abcdefghijklmnopqrstuvwxyz'} for length in range(44)}
    globalFrequency = {character: 0 for character in 'abcdefghijklmnopqrstuvwxyz'}

    ## populate wordLength dictionary with the characters and there frequencies for those words
    for dictionary_word in full_dictionary:
        letterFrequency = wordLengths[len(dictionary_word) - 1]
        for letter in dictionary_word:
            globalFrequency[letter] += 1
            letterFrequency[letter] += 1

    ## for every word size get the letter frequency dictionary for size x.
    ## sort the frequency of each letter for words of size x and add a list of the letter frequencies to the frequency table list.
    ## this loop ends up creating a list of lists which is the frequency table that will be used for guessing letters.
    for wordSize in frequencyTable:
        wordSizeDict = wordLengths[wordSize]
        sortedLetterFrequencies = sorted(wordSizeDict.items(), reverse=True, key=lambda kv: kv[1])
        sortedGlobalFrequencies = sorted(globalFrequency.items(), reverse=True, key=lambda kv: kv[1])
        globalFrequencyList = [item[0] for item in sortedGlobalFrequencies]
        letterFrequencyList = []

        for item in sortedLetterFrequencies:
            if item[1] != 0:
                letterFrequencyList.append(item[0])

        frequencyTable[wordSize] = letterFrequencyList

    return frequencyTable,globalFrequencyList


## Hangman Code Game with 10 tries to guess a word.
def letterCheck(guessedLetter,guessedLetters):
    if (len(guessedLetter) > 1):
        return 'you cannot guess more than one letters',False
    elif (guessedLetter not in 'abcdefjhijklmnopqrstuvwxyz'):
        return 'please guess a single lowercase letter',False
    elif (guessedLetters.__contains__(guessedLetter)):
        return 'you have already guesed that letter',False
    else:
        return 'no error',True

def hangmanGame(hinddenWord,frequencyTable,globalFrequency):

    turns = 6;
    guessNumber = 0;

    guessedWord = []
    guessedLetters = []

    for letter in range(len(hinddenWord)):
        guessedWord.append("-")

    # print()
    # print("Welcome to the game of hangman you will have",turns,"turns to try to guess a secret word.")
    # print("You may guess one letter at a time, if you guess correctly the corresponding letters in the secret word will be filled in.")
    # print("Correct guesses will not be counted against you.")
    # print("Good Luck")

    while turns > 0:
        # print()
        # print('you are on turn', turns)
        guessedWordString = ''.join(guessedWord)
        # print(''.join(guessedWord))

        if (len(frequencyTable[len(guessedWordString)]) > guessNumber):
            guessedLetter = frequencyTable[len(guessedWordString)][guessNumber]
        else:
            guessedLetter = globalFrequency[guessNumber]

        # errorCode,legalGuess = letterCheck(guessedLetter,guessedLetters)
        #
        # while (not (legalGuess)):
        #     print(errorCode)
        #     print(guessedLetter)
        #     guessedLetter = input("Please guess a letter:\n")
        #     errorCode, legalGuess = letterCheck(guessedLetter, guessedLetters)

        guessNumber += 1

        # print("you guessed",guessedLetter)
        guessedLetters.append(guessedLetter)

        if (hinddenWord.__contains__(guessedLetter)):
            # print('Good guess', guessedLetter, 'is in the word.')

            ## update the guessed word to show the new letters
            for letter in range(len(hinddenWord)):
                if (hinddenWord[letter] == guessedLetter):
                    guessedWord[letter] = guessedLetter

            ##check if the words are equal
            if (hinddenWord == (''.join(guessedWord))):
                return True
        else:
            # print('Sorry', guessedLetter, 'is not in the word.')
            turns -= 1

        ## increase turn counter
    return False

playGames = 1000
game = 0;
win = 0;
lose = 0;

while (game < playGames):

    full_dictionary_location = "words_250000_train.txt"
    full_dictionary = build_dictionary(full_dictionary_location)

    frequencyTable, globalFrequency = buildFrequencyTable(full_dictionary)

    randomWords = open('randomWords.txt', "r").read().splitlines()
    hiddenWord = randomWords[random.randint(0,len(randomWords)-1)]

    if (hangmanGame(hiddenWord,frequencyTable,globalFrequency)):
        print('won')
        win += 1
    else:
        print('lost')
        lose += 1

    game+=1

print('won:',win,'lost:',lose,'win rate:',win/playGames)





