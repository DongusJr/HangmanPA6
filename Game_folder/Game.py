#Imports
from Game_folder.Score import Score

# Main
class Game:
    ''' Class that holds information for each game played

        Class variables
        ---------------
        is_win : bool
            Indicates wheter player won or not
        guess_tuple : tuple with ints
            Holds how many wrong guesses were and what was max guess count
        difficulty_str : str
            Indicates what difficulty the player was on, used to calculate score
        win_streak : int
            Indicates how many wins in a row the player has
        score_obj : Score
            Object to calculate score
    '''
    def __init__(self, difficulty_str, total_score = 0, win_streak = 0):
        self.is_win = None
        self.guess_tuple = (None, None)
        self.difficulty_str = difficulty_str
        self.win_streak = win_streak
        self.score_obj = Score(win_streak)

    def __str__(self):
        ''' Prints out information for the game history '''
        win_str = "Win" if self.is_win else "Loss"
        print(win_str, self.guess_tuple[0], self.guess_tuple[1], self.difficulty_str, self.score_obj.get_score())
        return "{:<10}{}/{:<8}{:<14}{:<10}".format(win_str, self.guess_tuple[0], self.guess_tuple[1], self.difficulty_str, self.score_obj.get_score())

    def set_guess_tuple(self, guesses, max_guesses):
        ''' set wrong guesses and max guesses of a games '''
        self.guess_tuple = (guesses, max_guesses)

    def get_game_score(self):
        ''' Function that returns the score for the game '''
        return self.score_obj.get_score()

    def mark_is_win(self, bool_val):
        ''' Function that marks a game as a win or loss depending on a boolean '''
        self.is_win = bool_val
        if bool_val:
            self.score_obj.increment_win_streak() # Increase the win streak
        else:
            self.score_obj.reset_win_streak() # Reset the win streak
    
    def calculate_score(self):
        ''' Function that calculates the score after game '''
        self.score_obj.calculate_and_add_score(self.guess_tuple, self.difficulty_str)





    