# Imports
from enum import Enum
from Fakewindow.FakeWindow import FakeWindow
from UILayer.HangmanUI import HangmanUI
from UILayer.CustomWordUI import CustomWordUI
from UILayer.ProfileUI import ProfileUI
from Profile_folder.Profile import Profile

# Exception classes
class IncorrectInput(Exception):
    pass

# Enum classes
class MainCommands(Enum):
    PLAY_HANGMAN = "1"
    VIEW_PROFILE = "2"
    CUSTOMIZE_WORDS = "3"
    QUIT = "0"

# Main
class MainUI:
    ''' Class for navigation of the main window of the program '''
    def __init__(self, profile_name):
        self.fake_window_main = FakeWindow()
        self.profile = Profile(profile_name)
        # MainUI directs to the other UI's
        self.hangman_ui = HangmanUI(self.profile)
        self.custom_word_ui = CustomWordUI()
        self.profile_ui = ProfileUI(self.profile)
    
    def make_window(self):
        ''' Function that creates the window for the main window '''
        self.fake_window_main.add_box(2.5, 3)
        self.fake_window_main.add_header("Main menu")
        self.fake_window_main.add_enum_commands_as_text(MainCommands, 6, 3)

    def check_if_window_was_resized(self):
        if self.fake_window_main.has_window_changed_size():
            self.fake_window_main.reset_window()
            self.make_window()
            self.fake_window_main.print_window()

    def get_input(self):
        ''' Function that gets input for where the player wants to go '''
        is_quit = False
        self.make_window()
        while not is_quit:
            self.fake_window_main.print_window()
            user_input = input(":")
            self.check_if_window_was_resized()
            try:
                is_quit = self.direct_input(user_input)
            except IncorrectInput:
                # input not part of the Enum commands
                self.fake_window_main.add_error_message("Incorrect command")

    def direct_input(self, user_input):
        ''' Function that directs user inputs to the right place '''
        try:
            command = MainCommands(user_input)
        except:
            return False
        if command == MainCommands.PLAY_HANGMAN:
            self.hangman_ui.start_game()
        elif command == MainCommands.VIEW_PROFILE:
            self.profile_ui.view_profile()
        elif command == MainCommands.CUSTOMIZE_WORDS:
            self.custom_word_ui.add_a_custom_word()
        elif command == MainCommands.QUIT:
            return True
        return False