class Score:
    ''' Class that calculates score for a game '''
    def __init__(self, win_streak):
        self._score = 0
        self._win_streak = win_streak

    def increment_win_streak(self):
        ''' Function that increases the win streak '''
        self._win_streak += 1

    def get_score(self):
        ''' Function that returns the calcualted score '''
        return self._score

    def calculate_and_add_score(self, guess_tuple, difficulty_str):
        ''' Function that calculates the score of a game based on stats '''
        guesses, max_guesses = guess_tuple
        self._score = 0
        # score multiplier dependant on difficulty
        score_multiplier = self._get_score_multiplier(difficulty_str)
        self._score = 50*(max_guesses - guesses)*score_multiplier # 50 times each guess that was left
        self._score += 5*(self._win_streak)*score_multiplier # add for a win streak
        if guesses < 2:
            self._score += 1000 # if it only took 0 or 1 wrong guesses give a bonus
        self._win_streak += 1
        return self._score
        
    def _get_score_multiplier(self, difficulty_str):
        ''' Function that gives a score mutiplier for calculation of the score dependant on difficulty '''
        if difficulty_str == "easy":
            return 1
        elif difficulty_str == "normal":
            return 2
        elif difficulty_str == "hard":
            return 5
        else:
            raise

    def reset_win_streak(self):
        ''' Function that resets the win streak ''' 
        self._win_streak = 0

    