import random
import re

## uncomment prints and use user input guess for game version

def build_dictionary(dictionary_file_location):
    text_file = open(dictionary_file_location, "r")
    full_dictionary = text_file.read().splitlines()
    text_file.close()
    return full_dictionary

def getGlobalFrequency(full_dictionary):
    globalFrequency = {character: 0 for character in 'abcdefghijklmnopqrstuvwxyz'}
    for dictionary_word in full_dictionary:
        for letter in dictionary_word:
            globalFrequency[letter] +=1

    sortedGlobalFrequencies = sorted(globalFrequency.items(), reverse=True, key=lambda kv: kv[1])

    return [item[0] for item in sortedGlobalFrequencies]

def buildFrequencyTable(full_dictionary,guessedLetters,guessedWord):
    updatedDictionary = []
    ## we just want the frequency of the length of the guessed word. We don't care about words of other lengths

    wordLengthFrequency = {character: 0 for character in 'abcdefghijklmnopqrstuvwxyz'}

    ## convert guessed letters to regular expression range:
    guessedLettersString = ''.join(guessedLetters[:4]) ## the number of guessed letters included could be optimized


    ## populate wordLength dictionary with the characters and there frequencies for the words that match the passed in regular expression
    for dictionary_word in full_dictionary:
        ## don't include the first four letters that we've guessed when updating the search -- TODO not sure if don't include first guessed words or...
        if ((len(guessedLetters) == 0 and re.match('^'+guessedWord+'$',dictionary_word)) or ((re.match('^'+guessedWord+'$',dictionary_word) ))):
        # if ((len(guessedLetters) == 0 and re.match('^'+guessedWord+'$',dictionary_word)) or ((re.match('^'+guessedWord+'$',dictionary_word) and (not re.match('['+guessedLettersString+']',dictionary_word))))):
            updatedDictionary.append(dictionary_word)
            for letter in dictionary_word:
                wordLengthFrequency[letter] += 1

    ## for every word size get the letter frequency dictionary for size x.
    ## sort the frequency of each letter for words of size x and add a list of the letter frequencies to the frequency table list.
    ## this loop ends up creating a list of lists which is the frequency table that will be used for guessing letters.

    wordSizeDict = wordLengthFrequency
    sortedLetterFrequencies = sorted(wordSizeDict.items(), reverse=True, key=lambda kv: kv[1])

    letterFrequencyList = []

    for item in sortedLetterFrequencies:
        if item[1] != 0:
            letterFrequencyList.append(item[0])

    return updatedDictionary,letterFrequencyList

def buildLetterLikelihood(full_dictionary):

    ## letter list holds every letter from the dictionary as it was read in. list will appear like ...adewordloo...
    letterList = []
    ## dictionary holds the individual lists for each letter that stores the indices in which the letter is located in the list
    letterDictionary = {character: [] for character in 'abcdefghijklmnopqrstuvwxyz'}

    index = 0
    ## iterate through words in the dictionary
    for dictionary_word in full_dictionary:
        ## iterate through characters in the word. Using an integer to be able to access the preceding character
        for letter in dictionary_word:
            letterList.append(letter)
            letterDictionary[letter].append(index)
            index += 1
        letterList.append('!')
        index += 1

    return letterList,letterDictionary

## returns a list of letters based on their likelihood of following or preceding the inputed array of letters
## for example if the passed in array is ['l','e','p'] then the method will output ['h','s'] as the letters most likely
## to follow 'lep' based on the words from the train dictionary
## or return ['a','t'] as most likely letters to precede 'lep'
## guessFollowing is a boolean that is used to determine if we are guessing preceding words or following words
## input arrays can be of length 1 - length 3. this is represented by the lookback period and used to determine letter matching funcitons
def nextMostLikelyLetter(guessFollowing,knownLetters,letterList,letterDictionary):

    ## list that contains the frequency of letters preceding/following the inputed array of prediction letters
    letters = {character: 0 for character in 'abcdefghijklmnopqrstuvwxyz'}

    predictLetters = knownLetters
    lookback = len(predictLetters)

    def getLetter(index):
        if guessFollowing:
            return index + 1
        else:
            return index - 1

    ## return if letters in the list of letters match the provided prediction letters
    def checkMatch(lookback,index):
        ## checking for match after input letters ['l','e','p'] need to make sure letters in letter list match e and l depending on lookback
        if guessFollowing:
            if lookback == 2:
                return letterList[index - 1] == predictLetters[0]
            elif lookback == 3:
                return letterList[index - 2] == predictLetters[0] and letterList[index -1] == predictLetters[1]
        ## checking for match before input letters ['l','e','p'] need to make sure letters in letter list match e and l depending on lookback
        else:
            if lookback ==2:
                return letterList[index + 1] == predictLetters[1]
            elif lookback == 3:
                return letterList[index + 1] == predictLetters[1] and letterList[index + 1] == predictLetters[2]

    for i in letterDictionary[predictLetters[-1]]:
        ## Do different stuff for different lookback lengths
        if lookback == 1:
            try:
                letter = letterList[getLetter(i)]
                if (letter != '!'):
                    letters[letter] += 1
            except:
                continue
        elif lookback == 2:
            try:
                ## only increase the letters after count if it is a letter after following the lookback letters
                if checkMatch(lookback,i):
                    letter = letterList[getLetter(i)]
                    if (letter != '!'):
                        letters[letter] += 1
            except:
                continue
        elif lookback == 3:
            ## only increase the letters after count if it is a letter after following the lookback letters
            try:
                if checkMatch(lookback,i):
                    letter = letterList[getLetter(i)]
                    if (letter != '!'):
                        letters[letter] += 1
            except:
                continue

    letters = sorted(letters.items(), reverse=True, key=lambda kv: kv[1])

    likelihood = []
    for tuple in letters:
        if tuple[1] != 0:
            likelihood.append(tuple[0])

    return likelihood


def hangmanGame(hinddenWord,full_dictionary,letterList,letterDictionary,globalFrequencyList):

    turns = 7
    guessNumber = 0

    guessedWord = []
    guessedLetters = []

    for letter in range(len(hinddenWord)):
        guessedWord.append(".")

    while turns > 0:

        guessedWordString = ''.join(guessedWord)


        ## buildFrequency returns the list of character frequencies and an updated dictionary with only words of the correct length.
        updatedDictionary,frequencyList = buildFrequencyTable(full_dictionary,guessedLetters,guessedWordString)
        full_dictionary = updatedDictionary

        print(guessedWordString)
        print(frequencyList)

        ## can't guess duplicate so assume first guess is a duplicate to enter while loop
        guessedDuplicate = True

        ## give 5 chances with standard list route
        if (guessNumber <= 8):

            print('using frequency list technique')
            guessPosition = 0
            while (guessedDuplicate):

                ## can just guess the first letter in the list because we will keep cycling
                guessedLetter = frequencyList[guessPosition]

                ## check if we have already guessed the letter -- we will eventually guess a letter that we have not guessed. Otherwise we will break
                ## to the next letter guessing technique
                if (not (guessedLetters.__contains__(guessedLetter))):
                    guessedDuplicate = False
                else:
                    guessPosition += 1
                    if (guessPosition >= len(frequencyList)):
                        print('guessPosition is too big')
                        break

            print(guessedLetter)


        else:
            print('using next letter guessing')
            guessPosition = 0

            while(guessedDuplicate):

                guessFollowing = True
                ## split the guessed so far string into guessed parts, seperated by '.'
                brokenGuessWord = str.split(guessedWordString,'.')

                ## find the largest part of the guessed so far string to find the next letter with nextLetter method
                bigChunk = 0
                for i in range(len(brokenGuessWord)):
                    if len(brokenGuessWord[i]) > len(brokenGuessWord[bigChunk]):
                        bigChunk = i
                    try:
                        if (brokenGuessWord[bigChunk - 1] == ''):
                            ## indicates that we need to guess the letter following the word chunk
                            guessFollowing = False
                            pass
                    except:
                        ## indicates that we need to guess the letter after the word chunc
                        guessFollowing = True
                        pass


                knownLetters = list(brokenGuessWord[bigChunk])

                if (len(knownLetters) > 3 and guessFollowing):
                    knownLetters = knownLetters[-3:]
                elif(len(knownLetters) > 3 and not guessFollowing):
                    knownLetters = knownLetters[:3]


                nextLetterList = nextMostLikelyLetter(guessFollowing,knownLetters,letterList,letterDictionary)

                print('guessing following',guessFollowing,' for letters',knownLetters)
                print(nextLetterList)

                guessedLetter = nextLetterList[guessPosition]

                ## check if we have already guessed the letter
                if (not (guessedLetters.__contains__(guessedLetter))):
                    guessedDuplicate = False
                else:
                    guessPosition += 1
                    if (guessPosition >= len(nextLetterList)):
                        print('guessPosition is too big')
                        print('guessing from global list')
                        ## todo wrap all of this in a while loop that has a position check.

            print(guessedLetter)

            ## instead of using the global list I should use probabilites based on the preceding characters
            # guessedLetter = globalFrequencyList[guessNextLetter]


        guessNumber += 1

        guessedLetters.append(guessedLetter)

        if (hinddenWord.__contains__(guessedLetter)):

            ## update the guessed word to show the new letters
            for letter in range(len(hinddenWord)):
                if (hinddenWord[letter] == guessedLetter):
                    guessedWord[letter] = guessedLetter

            ##check if the words are equal
            if (hinddenWord == (''.join(guessedWord))):
                return True
        else:
            turns -= 1

        ## increase turn counter
    return False

playGames = 30
game = 0;
win = 0;
lose = 0;

while (game < playGames):

    full_dictionary_location = "words_250000_train.txt"
    full_dictionary = build_dictionary(full_dictionary_location)

    letterList, letterDictionary = buildLetterLikelihood(full_dictionary)

    globalFrequencyList = getGlobalFrequency(full_dictionary)

    randomWords = open('randomWords.txt', "r").read().splitlines()
    hiddenWord = randomWords[random.randint(0,len(randomWords)-1)]

    print(hiddenWord)

    if (hangmanGame(hiddenWord,full_dictionary,letterList,letterDictionary,globalFrequencyList)):
        print('won')
        win += 1
    else:
        print('lost')
        lose += 1

    game+=1

print('won:',win,'lost:',lose,'win rate:',win/playGames)





