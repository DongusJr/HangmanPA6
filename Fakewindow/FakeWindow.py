# Imports
from ctypes import windll, create_string_buffer
from enum import Enum
from Words.AskiiWord import AskiiWord
import time, sys

# Exception classes
class WindowTooSmall(Exception):
    pass

# Enum classes
class test(Enum):
    PLAY_HANGMAN = "1"
    CUSTOMIZE_WORDS = "2"
    QUIT = "3"

# Constants for the window
TOP_LEFT_CORNER =  u'\u2554' # ╔
TOP_RIGHT_CORNER = u'\u2557' # ╗
BOT_LEFT_CORNER =  u'\u255a' # ╚
BOT_RIGHT_CORNER = u'\u255d' # ╝
VERT_WALL =        u'\u2551' # ║
HORZ_WALL =        u'\u2550' # ═
VERT_WALL_RIGHT =  u'\u2560' # ╠
VERT_WALL_LEFT =   u'\u2563' # ╣
HORZ_WALL_UP =     u'\u2569' # ╩
HORZ_WALL_DOWN =   u'\u2566' # ╦
WALL_ALL =         u'\u256c' # ╬
SPACE =            " "

class FakeWindow:
    ''' Class that creates and displays all the windows used for the program

            Notable class variables
            -----------------------
            w_x_size, w_y_size : int, int
                The size of the window in terminal/cmd
            space_x_size, space_y_size : int, int
                the size of the space for width and height from the edge to the box, 
                the box is symmetrical so it is the same for both sides
            box_x_size, box_y_size : int, int
                the size of the box in width and height
            window_lis : lis(lis)
                double list compassing all the coordinates available for the window
            has_split : bool
                boolean indicating wheter the window box has a split border in it, used for positioning ohter elements
            window_too_small : bool
                indicates that the fake window is too small for printing
        '''
    def __init__(self):
        self.set_window_size()
        self.window_lis = [[" "]*self.w_x_size for y in range(self.w_y_size)]
        self.has_split = False

    def has_window_changed_size(self):
        ''' Function that checks if the terminal/cmd has been resized '''
        new_w_x_size, new_w_y_size = self._get_window_size()
        return not (new_w_x_size == self.w_x_size and new_w_y_size == self.w_y_size)

    def set_window_size(self):
        ''' Function that reassigns the window_size again, makes sure that the window size is compatable '''
        self.w_x_size, self.w_y_size = self._get_window_size()
        # 
        if self.w_x_size < 28 or self.w_y_size < 28:
            self.window_too_small = True
        else:
            self.window_too_small = False

    def get_box_coords(self):
        ''' Function that returns the (x_1, y_1), (x_2, y_2) coordinates of the box that indicates where it starts and stops '''
        return (self.space_x_size + 1, self.space_y_size , \
               (self.w_x_size - self.space_x_size), (self.w_y_size - self.space_y_size + 1))

    def add_box(self, space_ratio_x, space_ratio_y):
        ''' Function that adds a box with a border into the window, parameter ratios determine their position that is calculated '''
        # Calculate the space for the box and the space seperating it
        self.space_x_size = int(self.w_x_size // space_ratio_x)
        self.space_y_size = int(self.w_y_size // space_ratio_y)
        self.box_x_size = self.w_x_size - self.space_x_size*2
        self.box_y_size = self.w_y_size - self.space_y_size*2
        fkw_x_1, fkw_y_1, fkw_x_2, fkw_y_2 = self.get_box_coords()
        # Make the bottom and top border
        for x in range(fkw_x_1 + 1, fkw_x_2):
            self.window_lis[fkw_y_1][x] = HORZ_WALL # ═
            self.window_lis[fkw_y_2][x] = HORZ_WALL # ═
        # Make the left and right border
        for y in range(fkw_y_1 + 1, fkw_y_2):
            self.window_lis[y][fkw_x_1] = VERT_WALL # ║
            self.window_lis[y][fkw_x_2] = VERT_WALL # ║
        # Make the corners
        self.window_lis[fkw_y_1][fkw_x_1] = TOP_LEFT_CORNER  # ╔
        self.window_lis[fkw_y_1][fkw_x_2] = TOP_RIGHT_CORNER # ╗
        self.window_lis[fkw_y_2][fkw_x_1] = BOT_LEFT_CORNER  # ╚
        self.window_lis[fkw_y_2][fkw_x_2] = BOT_RIGHT_CORNER # ╝

    def add_art(self):
        ''' Function that adds a loaded ascii art into the box '''
        if self.has_split:
            # Make it center in the right side of the split
            # x and y position where the art starts
            art_pos_x = self.split_x_pos + ((((self.space_x_size + self.box_x_size) - self.split_x_pos) - self.art_x_size)//2) + 1
            art_pos_y = self.space_y_size + (self.box_y_size - self.art_y_size)//2
            art_x_1, art_y_1, art_x_2, art_y_2 = (art_pos_x), (art_pos_y), (art_pos_x + self.art_x_size), (art_pos_y + self.art_y_size)
        else:
            # Without split
            art_pos_x = self.space_x_size + (self.box_x_size - self.art_x_size)//2
            art_pos_y = self.space_y_size + (self.box_y_size - self.art_y_size)//4
            art_x_1, art_y_1, art_x_2, art_y_2 = (art_pos_x), (art_pos_y), (art_pos_x + self.art_x_size), (art_pos_y + self.art_y_size) 
        for y in range(art_y_1, art_y_2):
            for x in range(art_x_1, art_x_2):
                # self.art_chr_amount indicates how much of the art should be revealed
                # if the grid is ordered in a line the position of x and y is : y*size_x + x
                coords_curr_pos = ((y - art_y_1)*self.art_x_size + (x - art_x_1))
                if (0 <= coords_curr_pos <= self.art_chr_amount):
                    # revealed part of the art
                    self.window_lis[y][x] = self.askii_art_lis[y - art_y_1][x - art_x_1]
                else:
                    # unrevealed part of the art
                    self.window_lis[y][x] = " "

    def add_art_file(self, art_file_name):
        ''' Function that takes in a .txt file with an askii art and loads it into the class in a data structure 
            NOTE: Make sure that the width of the ascii art is always the same, use spaces to fill in gaps '''
        self.askii_art_lis = [] 
        with open(art_file_name, "r") as file:
            for line in file:
                line = line.strip("\n")
                self.askii_art_lis.append(line)
        self.art_x_size = len(self.askii_art_lis[0])
        self.art_y_size = len(self.askii_art_lis)

    def add_header(self, word):
        ''' Function that adds and ascii word header to the window, above the box '''
        askii_word_obj = AskiiWord(word) # Get the ascii word
        askii_word_lis = askii_word_obj.get_askii_word()
        height_of_word = askii_word_obj.get_height()
        length_of_word = askii_word_obj.get_length()
        # Get position for the header
        header_y_pos = (self.space_y_size - height_of_word) // 2
        header_x_pos = (self.w_x_size - length_of_word) // 2
        hd_x_1, hd_y_1, hd_x_2, hd_y_2 = (header_x_pos + 1), (header_y_pos), (self.w_x_size - header_x_pos - 1), (header_y_pos + 5)
        for y in range(height_of_word + 1):
            for x in range(length_of_word):
                # add each part of the word into the window
                self.window_lis[hd_y_1 + y][hd_x_1 + x] = askii_word_lis[y][x]

    def set_art_display_ratio(self, guesses, max_guesses):
        ''' Function that sets how much portion of the art is revealed '''
        # the ratio of the guess/max_guess multipled with the size of the art and then floored down to an int 
        self.art_chr_amount = int((guesses/max_guesses) * (self.art_x_size*self.art_y_size))

    def add_split(self, split_ratio, horizonal = False):
        ''' Function that adds a line split into the box, can be vertical and horizontal '''
        if not horizonal:
            # Vertical split
            # x position of the split
            self.split_x_pos = self.space_x_size + (self.box_x_size - int(self.box_x_size // split_ratio))
            fkw_x_1, fkw_y_1, fkw_x_2, fkw_y_2 = self.get_box_coords()
            for y in range(fkw_y_1 + 1, fkw_y_2):
                # Go down the y-axis and add the split
                self.window_lis[y][self.split_x_pos] = VERT_WALL # ║
            # Connect the edge of the box where the split is
            self.window_lis[fkw_y_1][self.split_x_pos] = HORZ_WALL_DOWN # ╦
            self.window_lis[fkw_y_2][self.split_x_pos] = HORZ_WALL_UP   # ╩
        else:
            # Horizontal split | Ditto the comments above
            self.split_y_pos = self.space_y_size + (self.box_y_size - int(self.box_y_size // split_ratio))
            fkw_x_1, fkw_y_1, fkw_x_2, fkw_y_2 = self.get_box_coords()
            for x in range(fkw_x_1 + 1, fkw_x_2):
                self.window_lis[self.split_y_pos][x] = HORZ_WALL
            self.window_lis[self.split_y_pos][fkw_x_1] = VERT_WALL_RIGHT
            self.window_lis[self.split_y_pos][fkw_x_2] = VERT_WALL_LEFT
        self.has_split = True # Mark that there is a split in the box

    def add_enum_commands_as_text(self, enum_commands, x_ratio, y_ratio):
        ''' Function that takes an Enum class and makes a str out of the commands it has '''
        space_between_commands = 3 # amount of newlines between commands
        # Position dependant of the parameters ratios
        c_x_1, c_y_1 = int(self.space_x_size + self.box_x_size // x_ratio), int(self.space_y_size + self.box_y_size // y_ratio) - 1
        for command in enum_commands:
            # i.e. 1) Play game
            command_str = command.value + ") " + command.name.capitalize().replace("_", " ")
            for index, chr_in_command_str in enumerate(command_str):
                # Put in the commands in their respective space on the window
                self.window_lis[c_y_1][c_x_1 + index] = chr_in_command_str
            c_y_1 += space_between_commands # new command

    def add_text(self, text, x_ratio, y_ratio):
        ''' Function that adds a text into the window in a position depedent on the parameter ratios '''
        c_y = int(self.space_y_size + self.box_y_size // y_ratio)
        for line in text.split("\n"):
            c_x = int(self.space_x_size + (self.box_x_size - len(line)) // x_ratio + 1)
            for index, chr_in_text in enumerate(line):
                self.window_lis[c_y][c_x + index] = chr_in_text
            c_y += 1 # newline

    def add_error_message(self, message):
        ''' Function that adds a message in the bottom of the box '''
        fkw_x_1, fkw_y_1, fkw_x_2, fkw_y_2 = self.get_box_coords()
        # If the box has a split center the message left side of the split
        if not self.has_split:
            m_x_1 = int(self.space_x_size + (self.box_x_size - len(message)) // 2 + 1)
        else:
            m_x_1 = int((self.space_x_size + self.split_x_pos - len(message)) // 2 + 1)
        m_x_2 = m_x_1 + len(message)
        # if and else for collisions on the box wall
        # Corner and edges of the box
        self.window_lis[fkw_y_2 - 2][m_x_1 - 1] = TOP_LEFT_CORNER if m_x_1 - 1 != fkw_x_1 else VERT_WALL_RIGHT # ╔ else ╠
        self.window_lis[fkw_y_2 - 2][m_x_2] = TOP_RIGHT_CORNER if m_x_2 != fkw_x_2 else VERT_WALL_LEFT # ╗ else ╣
        self.window_lis[fkw_y_2 - 1][m_x_1 - 1] = VERT_WALL # ║
        self.window_lis[fkw_y_2 - 1][m_x_2] = VERT_WALL # ║
        self.window_lis[fkw_y_2][m_x_1 - 1] = HORZ_WALL_UP  if m_x_1 - 1 != fkw_x_1 else BOT_LEFT_CORNER # ╩ else ╚
        self.window_lis[fkw_y_2][m_x_2] = HORZ_WALL_UP  if m_x_1 - 1 != fkw_x_1 else BOT_RIGHT_CORNER # ╩ else ╝
        # Sides of the box
        for x in range(m_x_1, m_x_2):
            self.window_lis[fkw_y_2 - 2][x] = HORZ_WALL # ═ | top side of the box
            if x < m_x_1 + len(message):
                self.window_lis[fkw_y_2 - 1][x] = message[x - m_x_1] # Add the text

    def clear_error_message(self):
        ''' Function that clears an error message from the window '''
        fkw_x_1, fkw_y_1, fkw_x_2, fkw_y_2 = self.get_box_coords()
        if self.has_split:
            # If it has a split we remove everything between left side of the box and the split position
            fkw_x_2 = self.split_x_pos
        for y in range(fkw_y_2 - 2, fkw_y_2):
            for x in range(fkw_x_1 + 1, fkw_x_2):
                self.window_lis[y][x] = " " # Empty the bottom 3 rows of the box
        for x in range(fkw_x_1 + 1, fkw_x_2):
            self.window_lis[fkw_y_2][x] = HORZ_WALL # ═ | Rebuild the border

    def clear_box(self):
        ''' Function that clears everything inside the box '''
        # Get the coords of the box
        x_1, y_1, x_2, y_2 = self.space_x_size + 2, self.space_y_size + 1, self.space_x_size + self.box_x_size, self.space_y_size + self.box_y_size  + 1
        for y in range(y_1, y_2 ):
            for x in range(x_1, x_2):
                self.window_lis[y][x] = " " # Make it empty
        if self.has_split:
            # Fix the edges where the split tampered the box
            fkw_x_1, fkw_y_1, fkw_x_2, fkw_y_2 = self.get_box_coords()
            self.window_lis[fkw_y_1][self.split_x_pos] = HORZ_WALL  # ═
            self.window_lis[fkw_y_2][self.split_x_pos] = HORZ_WALL # ═
        self.clear_error_message() # Use this to rebuild the bottom side of the box incase of an error message
        self.has_split = False

    def reset_window(self):
        ''' Function that resets the window and the window_lis '''
        self.w_x_size, self.w_y_size = self._get_window_size()
        self.window_lis = [[" "]*self.w_x_size for y in range(self.w_y_size)]
        # Check if the window is too small
        if self.w_x_size < 28 or self.w_y_size < 28:
            self.window_too_small = True
        else:
            self.window_too_small = False

    def _get_window_size(self):
        ''' Some voodoo magic code I found on the net some time ago which gives amount of spaces and newlines
            a terminal/cmd can hold, representing the x and y axiss of the window '''
        # stdin handle is -10
        # stdout handle is -11
        # stderr handle is -12

        h = windll.kernel32.GetStdHandle(-12)
        csbi = create_string_buffer(22)
        res = windll.kernel32.GetConsoleScreenBufferInfo(h, csbi)

        if res:
            import struct
            (buf_x, buf_y, cur_x, cur_y, wattr,
            left, top, right, bottom, max_x, max_y) = struct.unpack("hhhhHhhhhhh", csbi.raw)
            size_x = right - left + 1
            size_y = bottom - top + 1
        else:
            sizex, sizey = 80, 25 
            # can't determine actual size - return default values
        return (size_x, size_y - 2)
        
    def print_window(self):
        ''' Function that displays the window '''
        # Incase of the window being too small
        if self.window_too_small:
            error_message = "Window too small :("
            additional_message = "Resize your screen and type something in to fix"
            error_message_len = ((self.w_x_size - len(error_message)) // 2)
            additional_message_len = ((self.w_x_size - len(additional_message)) // 2)
            print("\n"*(self.w_y_size // 2 - 1) + " "*error_message_len + error_message + "\n" + " "*additional_message_len + additional_message + "\n"*(self.w_y_size // 2))
            return
        window_str = ""
        for y in range(self.w_y_size):
            for x in range(self.w_x_size - 1):
                window_str += self.window_lis[y][x]
            window_str += "\n"
        sys.stdout.write("\n" + window_str) # User sys.stdout for less stuttering
