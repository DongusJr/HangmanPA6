class HighScoreLinkedList:
    ''' Data structure that holds top highscores for a player '''
    class _Node:
        def __init__(self, next_, prev, data):
            ''' Simple node that knows it neigbours '''
            self.next = next_
            self.prev = prev
            self.data = data

    def __init__(self):
        # sentinels
        self.header = self._Node(None, None, None)
        self.trailer = self._Node(None, None, None)
        self.header.next = self.trailer
        self.trailer.prev = self.header
        self.size = 0

    def __len__(self):
        ''' Function that returns amount of items in the list '''
        return self.size

    def __iter__(self):
        ''' Function used to iterating through the list (for ... in ...) '''
        self.iter_helper = self.header.next # Use this variable for iteration
        return self

    def __next__(self):
        ''' Helper function for __iter__, returns value of each node in the list ''' 
        if self.iter_helper == self.trailer:
            raise StopIteration
        else:
            return_value = self.iter_helper.data
            self.iter_helper = self.iter_helper.next # Iterate
            return return_value

    def add_in_order(self, data):
        ''' Function that adds a node with a data in order from highest value to the lowest '''
        if self.size == 0: # Edge case
            new_node = self._Node(self.trailer, self.header, data)
            self.header.next = new_node
            self.trailer.prev = new_node
        else:
            self.add_in_order_recursive(self.header.next, data)
        self.size += 1

    def add_in_order_recursive(self, node, data):
        if node.data < data: # the node has found its neighbours
            self.add_between(node, node.prev, data)
        elif node.next == self.trailer: # The node is at the end of the list
            self.add_between(self.trailer, node, data)
        else:
            self.add_in_order_recursive(node.next, data) # recurse

    def add_between(self, successor, predecessor, data):
        ''' Function that creates a node and adds it between two nodes '''
        new_node = self._Node(successor, predecessor, data)
        predecessor.next = new_node
        successor.prev = new_node

    def pop_back(self):
        ''' Function that removes the last node of a list '''
        new_tail = self.trailer.prev.prev
        old_tail = self.trailer.prev
        new_tail.next = self.trailer
        self.trailer.prev = new_tail
        old_tail.next, old_tail.prev = None, None
        self.size -= 1

    def get_back(self):
        ''' Function that returns the data of the last node of a list '''
        return self.trailer.prev.data

    def get_front(self):
        ''' Function that returns the data of the first node of the list '''
        return self.header.next.data
