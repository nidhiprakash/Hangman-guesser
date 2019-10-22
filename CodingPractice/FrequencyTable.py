## create a dictionary of dictionaries outer dictionary holds the length of the word. inner dictionary holds the letter and its frequency in words of x length
## assuming 20 is the longest word in the dictionary
## since 0 based indexing a==0

## frequency table accessed by [length of word][frequency of letter in word #1 most frequent etc...]
## the index of the table represents the size of the word. 0 based so word size of 1 is equivelant to index 0
frequencyTable = [wordSize for wordSize in range(44)]
wordLengths =  {length : {character : 0 for character in 'abcdefghijklmnopqrstuvwxyz'} for length in range(44)}
globalFrequency = {character : 0 for character in 'abcdefghijklmnopqrstuvwxyz'}

def build_dictionary(dictionary_file_location):
    text_file = open(dictionary_file_location, "r")
    full_dictionary = text_file.read().splitlines()
    text_file.close()
    return full_dictionary

full_dictionary_location = "words_250000_train.txt"
full_dictionary = build_dictionary(full_dictionary_location)

## populate wordLength dictionary with the characters and there frequencies for those words
for dictionary_word in full_dictionary:
    letterFrequency = wordLengths[len(dictionary_word) - 1]
    for letter in dictionary_word:
        globalFrequency[letter] +=1
        letterFrequency[letter] += 1
    # print(letterFrequency)

## for every word size get the letter frequency dictionary for size x.
## sort the frequency of each letter for words of size x and add a list of the letter frequencies to the frequency table list.
## this loop ends up creating a list of lists which is the frequency table that will be used for guessing letters.
for wordSize in frequencyTable:
    wordSizeDict = wordLengths[wordSize]
    sortedLetterFrequencies = sorted(wordSizeDict.items(), reverse=True, key=lambda kv: kv[1])
    sortedGlobalFrequencies = sorted(globalFrequency.items(), reverse=True, key=lambda kv: kv[1])
    globalFrequencyList = [item[0]for item in sortedGlobalFrequencies]
    letterFrequencyList = []

    for item in sortedLetterFrequencies:
        if item[1] != 0:
            letterFrequencyList.append(item[0])

    ## check if letter frequency list is empty. if list is empty means no words of size x in sample dict.
    ## so fill with the global frequency list

    # if (len(letterFrequencyList) != 0):
    frequencyTable[wordSize] = letterFrequencyList
    # else:
        ## actually might be a good idea to keep the frequency table specefic to the word sizes and only refer the global frequency for
        ## guesses that exceed the lengths of the word for length x's frequency list.
        # frequencyTable[wordSize] = globalFrequencyList

print(frequencyTable[3])