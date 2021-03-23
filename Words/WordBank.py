import random

# Exception classes
class InvalidWord(Exception):
    pass

class WordAlreadyInBank(Exception):
    pass

# Main
class WordBank:
    ''' Class that holds words in a bank '''
    def __init__(self):
        self.word_bank_filename = "Text_files/word_bank.txt"
        self.word_bank_lis = self._make_word_bank_lis_from_file()

    def _make_word_bank_lis_from_file(self):
        ''' Function that dictionary of each word in a txt file '''
        word_bank_lis = []
        with open(self.word_bank_filename, "r") as f:
            for line in f:
                word_bank_lis.append(line.strip().lower())
        return word_bank_lis

    def choose_random_word_from_bank(self):
        ''' Function that chooses a random word from the word bank '''
        return random.choice(self.word_bank_lis)

    def add_word_to_word_bank(self, word):
        ''' Function that adds a word to the word bank file '''
        if word.isalpha():
            if not word in self.word_bank_lis:
                with open(self.word_bank_filename, "a") as f:
                    f.write("\n" + word)
                self.word_bank_lis.append(word)
            else:
                raise WordAlreadyInBank
        else:
            raise InvalidWord # Word is not alphabetical

