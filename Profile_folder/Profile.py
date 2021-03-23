# imports
from Profile_folder.ScoreLinkedList import HighScoreLinkedList

# Main
class Profile:
    ''' Class that holds information of the profile of a player 
        
        Class variables
        ---------------
        user_name : str
            name that the player refers to himself
        games : list
            list including all instances of games the player has played
        wins, loss : int
            count of wins and loss the player has
        high_scores : HighScoreLinkedList()
            linked list of all the highscore ordered from highest to lowest
    '''
    def __init__(self, user_name):
        self.user_name = user_name
        self.games = []
        self.wins = 0
        self.loss = 0
        self.high_scores = HighScoreLinkedList()


    def get_all_info(self):
        ''' Function that returns all information for the profile page '''
        return self.user_name, len(self.games), self.wins, self.loss, self.high_scores.get_front()

    def get_games(self):
        ''' Function that returns list of all instances of the games the player has played '''
        return self.games

    def get_high_score_str(self):
        ''' Function that creates a str of top 10 highscore the player has ''' 
        highscore_str = ""
        for i, score in enumerate(self.high_scores):
            highscore_str += str(i + 1) + ". " + str(score) + "\n\n"
            print(str(score))
        return highscore_str.strip("\n\n")

    def add_to_high_score(self, score):
        ''' Function that adds a highscore to the player '''
        self.high_scores.add_in_order(score)
        if len(self.high_scores) > 10:
            self.high_scores.pop_back()

    def add_to_win_or_loss(self, did_win):
        ''' Function that increments wins or loss depending on parameter boolean '''
        if did_win:
            self.wins += 1
        else:
            self.loss += 1

    def add_game(self, game_obj):
        ''' Function that adds a instance of a game to the player '''
        self.games.append(game_obj)

    def is_new_highscore(self, score):
        ''' Function that checks if a score manages to the highscore board '''
        if len(self.high_scores) < 10:
            return True
        else:
            return score > self.high_scores.get_back()
    

    