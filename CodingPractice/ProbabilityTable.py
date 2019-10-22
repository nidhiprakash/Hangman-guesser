## table that determines the probability of a charcter following a set of provided characters. All train data is from words_250000_train.txt
## each letter a - z will hold a list of likelihoods that the character a - z follows it
## the highest probability is the letter that will be guessed
## the probability technique will be used when the frequency list has been exhausted

def build_dictionary(dictionary_file_location):
    text_file = open(dictionary_file_location, "r")
    full_dictionary = text_file.read().splitlines()
    text_file.close()
    return full_dictionary

# full_dictionary_location = "words_250000_train.txt"
full_dictionary_location = 'words_250000_train.txt'
full_dictionary = build_dictionary(full_dictionary_location)

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
        index+=1
    ## append ! to indicate the end of a word
    letterList.append('!')
    index+=1

lettersAfter = {character: 0 for character in 'abcdefghijklmnopqrstuvwxyz'}

## lookback 3 letters to get prediction
## prediction for 'bra'


predictLetters = ['e','p','h']

lookback = len(predictLetters)

for i in letterDictionary[predictLetters[-1]]:
    if (i + 1 == len(letterList)):
        continue
    else:
        ## Do different stuff for different lookback lengths
        if lookback == 1:
            letterAfter = letterList[i + 1]
            if (letterAfter != '!'):
                lettersAfter[letterAfter] += 1
        elif lookback == 2:
            if (i - 1) < 0:
                continue
            ## only increase the letters after count if it is a letter after following the lookback letters
            if letterList[i - 1] == predictLetters[0]:
                letterAfter = letterList[i + 1]
                if (letterAfter != '!'):
                    lettersAfter[letterAfter] += 1
        elif lookback == 3:
            if (i - 1) < 0 or (i - 2) < 0:
                continue
            ## only increase the letters after count if it is a letter after following the lookback letters
            if letterList[i - 2] == predictLetters[0] and letterList[i - 1] == predictLetters[1]:
                letterAfter = letterList[i + 1]
                if (letterAfter != '!'):
                    lettersAfter[letterAfter] += 1


lettersAfter= sorted(lettersAfter.items(), reverse=True, key=lambda kv: kv[1])
print(lettersAfter)

likelihood = []
for tuple in lettersAfter:
    if tuple[1] != 0:
        likelihood.append(tuple[0])

print(likelihood)

