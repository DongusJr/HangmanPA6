# imports
from Fakewindow.FakeWindow import FakeWindow
from enum import Enum
from Game_folder.Game import Game
import random

# Enum classes
class ProfileCommands(Enum):
    VIEW_GAME_HISTORY = "1"
    VIEW_HIGHSCORES = "2"
    GO_BACK = "0"

# Main
class ProfileUI:
    ''' Class for the profile window of the program '''
    def __init__(self, profile_obj):
        self.profile = profile_obj
        self.profile_window = FakeWindow()
        self.highscore_window = FakeWindow()
        self.game_history_window = FakeWindow()
        self.page = 0
        self.window_and_function_lis = [(self.profile_window, self.make_profile_window), \
                                        (self.highscore_window, self.make_highscore_window), \
                                        (self.game_history_window, self.make_game_history_window)]

    def check_if_window_was_resized(self):
        if self.profile_window.has_window_changed_size():
            for window_obj, make_function in self.window_and_function_lis:
                window_obj.reset_window()
                make_function()

    def make_profile_window(self):
        ''' Function that creates the profile window '''
        self.profile_window.add_box(4, 7)
        self.profile_window.add_header("Profile")
        # Get the profile information and place it on the window
        user_name, n_o_games, wins, loss, highscore = self.profile.get_all_info()
        user_str, n_o_games_str, wins_str, loss_str, highscore_str = "User", "Number of games", "Wins", "Losses", "Highscore"
        self.profile_window.add_text(user_str + "\n" + "-"*len(user_str) + "\n" + user_name, 2, 10)
        self.profile_window.add_text(n_o_games_str + "\n" + "-"*len(n_o_games_str) + "\n" + str(n_o_games), 2, 5)
        self.profile_window.add_text(wins_str + "\n" + "-"*len(wins_str) + "\n" + str(wins), 2, 3.2)
        self.profile_window.add_text(loss_str + "\n" + "-"*len(loss_str) + "\n" + str(loss), 2, 2.4)
        self.profile_window.add_text(highscore_str + "\n" + "-"*len(highscore_str) + "\n" + str(highscore), 2, 1.8)
        # Add the commands available for the user
        self.profile_window.add_enum_commands_as_text(ProfileCommands, 2.4, 1.3)
        # Horizontal split
        self.profile_window.add_split(3,True)

    def make_highscore_window(self):
        ''' Function for the creation of the highscore window '''
        self.highscore_window.add_box(3,6)
        self.highscore_window.add_header("Highscores")
        highscore_str = self.profile.get_high_score_str()
        if highscore_str != "":
            # There are some highscores to display
            self.highscore_window.add_text(highscore_str, 2, 6)
        else:
            # No highscores to display
            self.highscore_window.add_text("No highscores", 2, 2)
        self.highscore_window.add_text('"0" to go back', 2 , 1.05)
        

    def view_profile(self):
        ''' Function that navigates the user through the profile screen '''
        self.make_profile_window()
        go_back = False
        while not go_back:
            self.profile_window.print_window()
            user_input = input(":")
            self.check_if_window_was_resized()
            # Returns True if player wants to leave the screen
            go_back = self.direct_input(user_input)

    def direct_input(self, user_input):
        ''' Function that directse players input on where he wants to go '''
        try:
            command = ProfileCommands(user_input)
        except:
            return False # Not a valid command, nothing happends
        if command == ProfileCommands.VIEW_GAME_HISTORY:
            self.view_game_history()
            return False
        elif command == ProfileCommands.VIEW_HIGHSCORES:
            self.view_highscores()
            return False
        elif command == ProfileCommands.GO_BACK:
            return True
    
    def view_highscores(self):
        ''' Function that displays the highscores for the player '''
        self.make_highscore_window()
        while True:
            self.highscore_window.print_window()
            user_input = input(":")
            self.check_if_window_was_resized()
            if user_input == "0": # Player wants to leave the screen
                break
    
    def make_games_str(self, games):
        ''' Function that makes a str for the game list '''
        game_str = ""
        page_end = min((self.page+1)*10, len(games))
        page_start = self.page*10
        game_str += "{:<10}{}/{:<8}{:<14}{:<10}\n\n".format("Won/Loss", "Guess", "Max", "Difficulty", "Score")
        for i in range(page_start, page_end):
            game_str += str(i + 1) + ") " + str(games[i]) + "\n\n"
        return game_str


    def make_game_history_window(self):
        ''' Function creates the game history window '''
        games = self.profile.get_games()
        self.game_history_window.add_box(3,6)
        self.game_history_window.add_header("Games")
        game_str = self.make_games_str(games)
        if game_str != "":
            # There are games in the players history
            self.game_history_window.add_text(game_str, 2, 6)
        else:
            # No game in the history
            self.game_history_window.add_text("No games", 2, 2)
        if (self.page+1)*10 < len(games):
            self.game_history_window.add_text("1) Next page", 1.1, 1.025)
        if self.page > 0:
            self.game_history_window.add_text("2) Prev page", 6, 1.025) 
        self.game_history_window.add_text('"0" to go back', 2 , 1.025)

    def view_game_history(self):
        ''' Function that displays the game history window for the player '''
        games = self.profile.get_games()
        while True:
            self.make_game_history_window()
            self.game_history_window.print_window()
            user_input = input(":")
            self.check_if_window_was_resized()
            if user_input == "0":
                break # Go back
            elif user_input == "1" and (self.page+1)*10 < len(games):
                self.page += 1
            elif user_input == "2" and self.page > 0:
                self.page -= 1
            self.game_history_window.clear_error_message()
            self.add_text("           ", 2, 2)
