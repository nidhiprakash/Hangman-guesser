import json
import requests
import random
import string
import secrets
import time
import re
import collections
try:
    from urllib.parse import parse_qs, urlencode, urlparse
except ImportError:
    from urlparse import parse_qs, urlparse
    from urllib import urlencode

HANGMAN_URL = "https://www.trexsim.com/trexsim/hangman"



class HangmanAPI(object):
    def __init__(self, access_token=None, session=None, timeout=None):
        self.access_token = access_token
        self.session = session or requests.Session()
        self.timeout = timeout
        self.guessed_letters = []
        self.guessNumber = 0

        full_dictionary_location = "words_250000_train.txt"
        self.full_dictionary = self.build_dictionary(full_dictionary_location)
        self.frequencyTable,self.globalFrequencyList = self.buildFrequencyTable(self.full_dictionary)


    ## create a dictionary of dictionaries for frequency table. outer dictionary holds the length of the word. inner dictionary holds the letter and its frequency in words of x length
    ## range of word lengths is based on longest word in sample dictionary
    ## since 0 based indexing a==0
    def buildFrequencyTable(self,full_dictionary):
        longestWord = 0;
        for dictionary_word in full_dictionary:
            if len(dictionary_word) > longestWord:
                longestWord = len(dictionary_word)

        frequencyTable = [wordSize for wordSize in range(longestWord)]
        wordLengths = {length: {character: 0 for character in 'abcdefghijklmnopqrstuvwxyz'} for length in range(longestWord)}
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

            ## check if letter frequency list is empty. if list is empty means no words of size x in sample dict.
            ## so fill with the global frequency list

            # if (len(letterFrequencyList) != 0):
            frequencyTable[wordSize] = letterFrequencyList
            # else:
            ## actually might be a good idea to keep the frequency table specefic to the word sizes and only refer the global frequency for
            ## guesses that exceed the lengths of the word for length x's frequency list.
            # frequencyTable[wordSize] = globalFrequencyList

        return frequencyTable,globalFrequencyList


    def guess(self, word):  # word input example: "_ p p _ e "
        ###############################################
        # Replace with your own "guess" function here #
        ###############################################

        # clean the word so that we strip away the space characters
        # replace "_" with "." as "." indicates any character in regular expressions
        clean_word = word[::2].replace("_", ".")
        print(clean_word)

        # find length of passed word
        len_word = len(clean_word)
        print(clean_word)

        if (len(self.frequencyTable[len_word]) > self.guessNumber):
            guess_letter = self.globalFrequencyList[self.guessNumber]
        else:
            guess_letter = self.frequencyTable[len_word][self.guessNumber]

        self.guessNumber += 1

        return guess_letter


    ##########################################################
    # You'll likely not need to modify any of the code below #
    ##########################################################

    def build_dictionary(self, dictionary_file_location):
        text_file = open(dictionary_file_location, "r")
        full_dictionary = text_file.read().splitlines()
        text_file.close()
        return full_dictionary

    def start_game(self, practice=True, verbose=True):
        # reset guessed letters to empty set and current plausible dictionary to the full dictionary
        self.guessed_letters = []
        self.current_dictionary = self.full_dictionary

        response = self.request("/new_game", {"practice": practice})
        if response.get('status') == "approved":
            game_id = response.get('game_id')
            word = response.get('word')
            tries_remains = response.get('tries_remains')
            if verbose:
                print(
                    "Successfully start a new game! Game ID: {0}. # of tries remaining: {1}. Word: {2}.".format(game_id,
                                                                                                                tries_remains,
                                                                                                                word))
            while tries_remains > 0:
                # get guessed letter from user code
                guess_letter = self.guess(word)

                # append guessed letter to guessed letters field in hangman object
                self.guessed_letters.append(guess_letter)
                if verbose:
                    print("Guessing letter: {0}".format(guess_letter))

                try:
                    res = self.request("/guess_letter",
                                       {"request": "guess_letter", "game_id": game_id, "letter": guess_letter})
                except HangmanAPIError:
                    print('HangmanAPIError exception caught on request.')
                    continue
                except Exception as e:
                    print('Other exception caught on request.')
                    raise e

                if verbose:
                    print("Sever response: {0}".format(res))
                status = res.get('status')
                tries_remains = res.get('tries_remains')
                if status == "success":
                    if verbose:
                        print("Successfully finished game: {0}".format(game_id))
                    return True
                elif status == "failed":
                    reason = res.get('reason', '# of tries exceeded!')
                    if verbose:
                        print("Failed game: {0}. Because of: {1}".format(game_id, reason))
                    return False
                elif status == "ongoing":
                    word = res.get('word')
        else:
            if verbose:
                print("Failed to start a new game")
        return status == "success"

    def my_status(self):
        return self.request("/my_status", {})

    def request(
            self, path, args=None, post_args=None, method=None):
        if args is None:
            args = dict()
        if post_args is not None:
            method = "POST"

        # Add `access_token` to post_args or args if it has not already been
        # included.
        if self.access_token:
            # If post_args exists, we assume that args either does not exists
            # or it does not need `access_token`.
            if post_args and "access_token" not in post_args:
                post_args["access_token"] = self.access_token
            elif "access_token" not in args:
                args["access_token"] = self.access_token

        try:
            # response = self.session.request(
            response = requests.request(
                method or "GET",
                HANGMAN_URL + path,
                timeout=self.timeout,
                params=args,
                data=post_args)
        except requests.HTTPError as e:
            response = json.loads(e.read())
            raise HangmanAPIError(response)

        headers = response.headers
        if 'json' in headers['content-type']:
            result = response.json()
        elif "access_token" in parse_qs(response.text):
            query_str = parse_qs(response.text)
            if "access_token" in query_str:
                result = {"access_token": query_str["access_token"][0]}
                if "expires" in query_str:
                    result["expires"] = query_str["expires"][0]
            else:
                raise HangmanAPIError(response.json())
        else:
            raise HangmanAPIError('Maintype was not text, or querystring')

        if result and isinstance(result, dict) and result.get("error"):
            raise HangmanAPIError(result)
        return result


class HangmanAPIError(Exception):
    def __init__(self, result):
        self.result = result
        self.code = None
        try:
            self.type = result["error_code"]
        except (KeyError, TypeError):
            self.type = ""

        try:
            self.message = result["error_description"]
        except (KeyError, TypeError):
            try:
                self.message = result["error"]["message"]
                self.code = result["error"].get("code")
                if not self.type:
                    self.type = result["error"].get("type", "")
            except (KeyError, TypeError):
                try:
                    self.message = result["error_msg"]
                except (KeyError, TypeError):
                    self.message = result

        Exception.__init__(self, self.message)


api = HangmanAPI(access_token="26744cb0eb622a651080b56f4e7d6b", timeout=2000)


api.start_game(practice=1,verbose=True)
[total_practice_runs,total_recorded_runs,total_recorded_successes] = api.my_status() # Get my game stats: (# of tries, # of wins)
print('run %d practice games out of an allotted 100,000' %total_practice_runs)


[total_practice_runs,total_recorded_runs,total_recorded_successes] = api.my_status() # Get my game stats: (# of tries, # of wins)
success_rate = total_recorded_successes/total_recorded_runs
print('overall success rate = %.3f' % success_rate)