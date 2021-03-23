# Imports
from Words.WordLinkedList import WordLinkedList

# Character constants
ORD_A = 97
ORD_Z = 122

# Main
class Hangman:
    ''' Class that is helps playing the game 

        class variables
        ---------------
        guesses : int
            number of wrong guesses by user
        masx_guesses : int
            maximum amount of wrong guesses the player can make
        word_obj : WorkLinkedList
            A LinkedList containing the characters in the word in order
        chr_available_dict : dict
            A dictionary with each character that point to either True or False
            depending if the character is available to guess
        chr_in_word : set
            contains each unique chr in the original word
    '''
    def __init__(self, word_to_guess, max_guesses):
        self.guesses = 0
        self.max_guesses = max_guesses
        self.word_obj = WordLinkedList()
        self.word_obj.make_list_from_word(word_to_guess)
        self.chr_available_dict = self._make_list_of_letters_available()
        self.chr_in_word = set(word_to_guess)

    def _make_list_of_letters_available(self):
        ''' Function that creates dictionary of all available characters to guess '''
        chr_available_dict = {}
        for chr_number in range(ORD_A, ORD_Z + 1):
            chr_available_dict[chr(chr_number)] = True
        return chr_available_dict

    def get_guesses_and_max_guess(self):
        ''' Function that returns amount of wrong guesses and max guesses for player '''
        return (self.guesses, self.max_guesses)

    def increment_guess(self):
        ''' Function that increments wrong guesses by 1 '''
        self.guesses += 1

    def get_word_obj(self):
        ''' Function that returns the WordLinkedList object of the word '''
        return self.word_obj

    def reveal_letter(self, letter):
        ''' Function that reveals one letter for the player '''
        self.word_obj.reveal_letter(letter)

    def reveal_word(self):
        ''' Function that reveals the whole word for the player '''
        self.word_obj.reveal_word()

    def guess_is_in_word(self, guess):
        ''' Function that checks a players guess is in the word '''
        return guess in self.chr_in_word

    def mark_letter_unavailable(self, player_guess):
        ''' Function that disables a letter that the user has guessed '''
        self.chr_available_dict[player_guess] = False

    def guess_is_original_word(self, player_guess):
        ''' Function that checks if a user guess matches the original word '''
        return self.word_obj.is_original_word(player_guess)

    def has_guessed_all(self):
        ''' Function that checks if all letters have been guessed correctely '''
        return self.word_obj.has_guessed_all()

    def is_game_over(self):
        ''' Function that checks if amount of wrong guesses exceed what is the maximum amount of wrong guesses '''
        return self.guesses == self.max_guesses

    def letter_is_available(self, guess):
        ''' Function that checks if a letter is available for the user to guess '''
        try:
            return self.chr_available_dict[guess]
        except:
            return False

    