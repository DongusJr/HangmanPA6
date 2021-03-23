# imports
from Words.WordBank import *
from Fakewindow.FakeWindow import FakeWindow
import time

# Main
class CustomWordUI:
    ''' Class that makes and displays the "Add a custom word to the word bank" screen '''
    def __init__(self):
        self.fake_window = FakeWindow() # The window object
        self.word_bank = WordBank()

    def check_if_window_was_resized(self):
        if self.fake_window.has_window_changed_size():
            self.fake_window.reset_window()
            self.make_window()
            self.fake_window.print_window()

    def make_window(self):
        ''' Function that creates the attributes of the fake window '''
        self.fake_window.add_box(6, 3) 
        self.fake_window.add_header("Word Bank")
        self.fake_window.add_text("Type in the word you want to add", 2, 4)
        self.fake_window.add_text('Type in "q" to go back', 2, 1.5)
        
    def add_a_custom_word(self):
        ''' Function that navigates the player to add a word '''
        self.make_window()
        while True:
            self.fake_window.print_window()
            self.fake_window.clear_error_message() # Clear unwanted error message to avoid collision
            players_input = input(":")
            self.check_if_window_was_resized()
            if players_input.lower() == "q": # Player wants to go back
                return
            try:
                self.word_bank.add_word_to_word_bank(players_input) # add the word
                self.fake_window.add_error_message('Word "' + players_input + '" added to the bank')
            except InvalidWord:
                self.fake_window.add_error_message("Word is invalid")
            except WordAlreadyInBank:
                self.fake_window.add_error_message("Word already in the bank")