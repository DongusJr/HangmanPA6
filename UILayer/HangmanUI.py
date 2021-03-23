# imports
from Fakewindow.FakeWindow import FakeWindow
from Game_folder.Hangman import Hangman
from Game_folder.Game import Game
from Words.WordBank import WordBank
from Profile_folder.Profile import Profile
import time
from enum import Enum

# Exception classes
class NotAValidInput(Exception):
    pass

class LetterAlreadyGuessed(Exception):
    pass

class GuessIncorrect(Exception):
    pass

# Enum classes
class DifficultyCommands(Enum):
    EASY = "1"
    NORMAL = "2"
    HARD = "3"

# Main
class HangmanUI:
    ''' Class that makes and displays the game screen '''
    def __init__(self, profile_obj):
        self.game_window = FakeWindow() # Hangman window
        self.difficulty_window = FakeWindow()  # Used mischelenious things 
        self.word_bank = WordBank()
        self.player_profile = profile_obj
        self.window_and_function_lis = [(self.game_window, self.make_game_window), \
                                        (self.difficulty_window, self.make_difficulty_window)]

    def check_if_window_was_resized(self):
        if self.game_window.has_window_changed_size():
            for window_obj, make_function in self.window_and_function_lis:
                window_obj.reset_window()
                make_function()

    def play_pregame_animation(self):
        ''' Function that plays a pregame animation for the player '''
        word_obj = self.hangman_game.get_word_obj()
        str_len = len(str(word_obj))
        chr_len = len(word_obj)
        for chr_count, i in enumerate(range(0 , str_len + 1, 2)):
            # display one letter at a time and one piece of the art at a time
            self.game_window.add_text("Word to guess:\n\n" + str(word_obj)[0:i], 3.25, 6)
            self.add_art_with_ratio(chr_count, chr_len)
            self.game_window.print_window()
            time.sleep(0.05)
        time.sleep(1)
        for chr_count in range(str_len, 0, -1):
            # Unreveal the ascii art
            self.add_art_with_ratio(chr_count, chr_len)
            self.game_window.print_window()
            time.sleep(0.05)

    def add_art_file(self, file_name):
        ''' Function that takes a .txt file of an ascii art and saves it in a data structure '''
        self.game_window.add_art_file(file_name)

    def add_art_with_ratio(self, guesses, max_guesses):
        ''' Function that sets how much of the art should be displayed '''
        self.game_window.set_art_display_ratio(guesses, max_guesses)
        self.game_window.add_art()

    def make_game_window(self):
        ''' Function that creates the game window '''
        self.game_window.add_box(4, 4)
        self.game_window.add_split(3)
        self.game_window.add_header("Hangman")

    def add_rules(self):
        ''' Function that adds a rule text for the game '''
        self.difficulty_window.add_text("How the game works\n\n" + \
                                   "1. You get 3/6/9 guesses depending on difficulty\n\n" + \
                                    "2. You try to guess a word given on screen either by using one letter or a whole guess\n\n" + \
                                    "3. For each wrong guess, your counter goes up\n\n" + \
                                    "4. If you manage to guess the word before using all your guesses, you win!\n\n" + \
                                    "5. Score is calculated depening on win streak, amount of guesses and length of the word",
                                    2, 6)

    def play_victory_animation(self, difficulty_str, game_score, total_score):
        ''' Function that plays a victory animation for the player '''
        guesses, max_guesses = self.hangman_game.get_guesses_and_max_guess()
        self.game_window.clear_box()
        victory_messge = "Congratulations!!!"
        for i in range(len(victory_messge) + 1):
            # slowly reveal victory message for the user
            self.game_window.add_text(victory_messge[0:i], 2, 4)
            self.game_window.print_window()
            time.sleep(0.05)
        time.sleep(1)
        # Additional messages
        self.game_window.add_text(f"It took you {guesses} guesses to win", 2, 2.2)
        self.game_window.add_text("You won with the score", 2, 2)
        self.game_window.add_text(str(game_score), 2, 1.8)
        self.game_window.print_window()
        time.sleep(1)
        self.game_window.add_text("Your total score", 2, 1.6)
        self.game_window.add_text(str(total_score), 2, 1.5)
        self.game_window.print_window()
        time.sleep(1)

    def play_defeat_animation(self, total_score):
        ''' Function that plays a animation after a loss '''
        self.game_window.clear_box()
        for i in range(0, 27):
            # Slowly reveal the ascii art
            self.add_art_with_ratio(i, 26)
            self.game_window.print_window()
            time.sleep(0.05)
        time.sleep(1)
        # Additional messages
        self.game_window.add_text("You lost", 2.05, 2)
        self.game_window.print_window()
        time.sleep(1)
        word_obj = self.hangman_game.get_word_obj()
        self.game_window.add_text("The word was: " + str(word_obj).replace(" ", ""), 2, 1.6)
        self.game_window.print_window()
        time.sleep(1)
        self.game_window.add_text("You lost with a total points of", 2, 1.4)
        self.game_window.add_text(str(total_score), 2, 1.3)
        self.game_window.print_window()
        time.sleep(1)

    def get_amount_of_guesses(self, input):
        ''' Function that takes in user inputs and returns the amount of guesses he gets '''
        try:
            command = DifficultyCommands(input)
            if command == DifficultyCommands.EASY:
                return 9, command.name.lower()
            elif command == DifficultyCommands.NORMAL:
                return 6, command.name.lower()
            elif command == DifficultyCommands.HARD:
                return 3, command.name.lower()
        except:
            pass
        return None, None

    def make_difficulty_window(self):
        ''' Function that makes the difficulty picker window '''
        self.difficulty_window.add_box(8,6)
        self.difficulty_window.add_header("Hangman")
        self.add_rules()
        self.difficulty_window.add_text("Pick your difficulty", 2, 1.5)
        self.difficulty_window.add_enum_commands_as_text(DifficultyCommands, 2.1, 1.25)

    def get_difficulty_input(self):
        ''' Function that directs user input for difficulty of the game '''
        while True:
            self.difficulty_window.print_window() # print the difficulty window
            self.difficulty_window.clear_error_message() # avoid collision of error messages
            difficulty_input = input(":")
            self.check_if_window_was_resized()
            # returns None if invalid input
            amount_of_guesses, difficulty_str = self.get_amount_of_guesses(difficulty_input)
            if amount_of_guesses != None:
                return amount_of_guesses, difficulty_str
            self.difficulty_window.add_error_message("Invalid input")

    def get_player_input_for_replay(self):
        ''' Function that user input on wheter he wants to play again or not '''
        self.game_window.add_text("Would you like to play again?(y/n)", 2 , 1.1)
        self.game_window.print_window()
        while True:
            player_input = input(":").lower()
            if player_input == "y":
                return True
            elif player_input == "n":
                return False

    def start_game(self):
        ''' Function that navigates the user to the game and assigns variables to appropriate places after game '''
        play_again = True
        # Make the difficulty picker window
        self.make_difficulty_window()
        total_score = 0 # Total score the player amounts after a spell of wins
        win_streak = 0
        while play_again:
            self.check_if_window_was_resized()
            
            amount_of_guesses, difficulty_str = self.get_difficulty_input()
            # Make a new game instance of the game being played
            self.game = Game(difficulty_str, total_score, win_streak)
            # Get a random word from the word bank
            original_word = self.word_bank.choose_random_word_from_bank()
            # Make the hangman helper instance
            self.hangman_game = Hangman(original_word, amount_of_guesses)
            # Play the game
            won_game = self.play_hangman()
            guesses, max_guesses = self.hangman_game.get_guesses_and_max_guess()
            self.game.set_guess_tuple(guesses, max_guesses) # Mark incorrect and max guesses
            if won_game:
                # The player won
                self.game.calculate_score()
                game_score = self.game.get_game_score()
                total_score += game_score
                win_streak += 1
                self.play_victory_animation(difficulty_str, game_score, total_score)
            else:
                # Player lost
                self.play_defeat_animation(total_score)
                if self.player_profile.is_new_highscore(total_score):
                    # Player got a new highscore
                    self.game_window.add_text("New highscore!", 2, 1.2)
                    self.player_profile.add_to_high_score(total_score)
                # Reset total score and win streak
                total_score = 0
                win_streak = 0
            # Mark victory or loss
            self.game.mark_is_win(won_game)
            # Set the wrong guesses the player had
            self.game.set_guess_tuple(guesses, max_guesses)
            # Add the game instance to the users profile
            self.player_profile.add_game(self.game)
            # Does the player want to play again?
            play_again = self.get_player_input_for_replay()
            # Reset the window
            self.game_window.reset_window()

    def display_game_window(self, word_obj):
        ''' Function that displays the game window for the player with amount of guesses left '''
        guess, max_guesses = self.hangman_game.get_guesses_and_max_guess()
        self.add_art_with_ratio(guess, max_guesses)
        self.game_window.add_text("Word to guess\n\n" + str(word_obj), 3.25, 6)
        self.game_window.add_text(f"You are on guess: {guess}/{max_guesses}", 3.25, 3)
        self.game_window.print_window()
        self.game_window.clear_error_message()

    def get_players_guess(self, word_obj):
        ''' Function that returns a players guess and wheter his guess a whole word or not'''
        while True:
            player_guess = input("Your guess: ").lower()
            self.check_if_window_was_resized()
            self.display_game_window(word_obj)
            try:
                is_a_guess = self.validate_input(player_guess)
                break
            except NotAValidInput:
                self.game_window.add_error_message("Invalid letter")
            except LetterAlreadyGuessed:
                self.game_window.add_error_message("You have already guessed that letter")
            except GuessIncorrect:
                self.game_window.add_error_message("Your guess was incorrect")
                is_a_guess = True
                break
            self.game_window.print_window()
            self.game_window.clear_error_message()
        return player_guess, is_a_guess

    def play_hangman(self):
        ''' Function that plays the game for the player '''
        self.make_game_window()
        self.add_art_file("Text_files/askii_scull.txt") # Add the ascii art
        self.play_pregame_animation()
        word_obj = self.hangman_game.get_word_obj()
        won_game = False
        # check after each round if the game is over or if the player has won
        while not self.is_game_over() and not won_game:
            self.display_game_window(word_obj)
            player_guess, is_a_guess = self.get_players_guess(word_obj) 
            if len(player_guess) == 1:
                # The guess was only one character
                if self.hangman_game.guess_is_in_word(player_guess):
                    # Guessed correctely
                    self.hangman_game.reveal_letter(player_guess)
                    self.game_window.add_error_message("You guessed correctly!")
                else:
                    # Guessed incorrectely
                    self.game_window.add_error_message("You guessed incorrectly")
                    self.hangman_game.increment_guess()
                # User has now already guessed that letter
                self.hangman_game.mark_letter_unavailable(player_guess)
            else:
                # The guess is a word
                if self.hangman_game.guess_is_original_word(player_guess):
                    # Player guessed correctely
                    won_game = True
                    self.hangman_game.reveal_word()
                    break
                else:
                    self.hangman_game.increment_guess()
            if self.hangman_game.has_guessed_all():
                won_game = True
        # Display window one last time and reveal the word
        self.display_game_window(word_obj)
        self.hangman_game.reveal_word() # Only makes a difference if the player lost
        time.sleep(1.5)
        return won_game
        
    def validate_input(self, guess):
        ''' Function that checks if a players guess is valid '''
        if len(guess) > 1 and guess.isalpha():
            # The guess is a whole word
            if self.hangman_game.guess_is_original_word(guess):
                return True # Guess was correct
            else:
                raise GuessIncorrect
        elif self.hangman_game.letter_is_available(guess) and len(guess) == 1:
            return False # Letter was available, guess is a chr
        elif len(guess) == 1:
            raise LetterAlreadyGuessed
        else:
            raise NotAValidInput

    def is_game_over(self):
        ''' Function that checks if player has reached max guesses '''
        return self.hangman_game.is_game_over()
