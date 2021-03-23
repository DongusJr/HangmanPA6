class SinglyLinkedNode:
    def __init__(self, chr_, next_ = None):
        ''' Simple node that points to the next node '''
        self.next = next_
        self.chr = chr_
        # node is revealed or unrevealed for the game
        self.is_revealed = False

class WordLinkedList:
    ''' Data structure that holds each character of a word in a node '''
    def __init__(self):
        self.head = None
        self.org_word = None
        self.size = 0
        self.reveal_count = 0

    def __str__(self):
        ''' Function that makes a str of the word, keeping unrevealed characters unrevealed '''
        return self._make_str_recursively(self.head)

    def __len__(self):
        ''' Function that returns the length of the word '''
        return self.size

    def _make_str_recursively(self, node):
        ''' Function that creates a word str from the linked list '''
        if node == None:
            return "" # No more letters in the word
        else:
            if node.is_revealed:
                # The chr is revealed, print it
                return str(node.chr) + " " + self._make_str_recursively(node.next)
            else:
                # The chr is concealed, hide it
                return "-" + " " + self._make_str_recursively(node.next)

    def make_list_from_word(self, word_str):
        ''' Function that creates a list from a word str '''
        self.org_word = word_str # Save the original word
        self.head = self.make_list_from_word_recursive(word_str)

    def make_list_from_word_recursive(self, word_str):
        ''' Function that recursively turns a word str into a linked list '''
        if word_str == "":
            return None # No more letters left, tail connects to None
        else:
            self.size += 1
            node = SinglyLinkedNode(word_str[0]) # Make a new node
            node.next = self.make_list_from_word_recursive(word_str[1:]) # Connect it
        return node # returns head

    def is_original_word(self, guess_word):
        ''' Function that checks if a word is the original word '''
        return self.org_word == guess_word

    def reveal_word(self):
        ''' Function that reveals all the nodes in the linked list '''
        walk = self.head
        while walk != None:
            # Walk through the list and reveal each letter
            walk.is_revealed = True
            walk = walk.next

    def reveal_letter(self, char):
        ''' Function that reveals a letter in the linked list '''
        walk = self.head
        while walk != None:
            # Walk through the list until the letter is found and conceal it
            if walk.chr == char and not walk.is_revealed:
                walk.is_revealed = True
                self.reveal_count += 1
            walk = walk.next

    def has_guessed_all(self):
        ''' Function that checks if all the letters have been revealed '''
        return self.reveal_count == self.size



