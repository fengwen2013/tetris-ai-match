import random

class RandomBot:
    def __init__(self):
        self.name = 'RandomBot'

    def next_move(self, pieces, board, cur_height):
        direction = random.randint(0, 3)
        h = pieces[0].get_height()
        w = pieces[0].get_width()
        r_loc = 0
        c_loc = random.randint(0, len(board[0]) - w)
        pieces[0].rotate(direction)

        return r_loc, c_loc

class StackBot:
    def __init__(self):
        self.name = 'StackBot'
        self.col = 0

    def next_move(self, pieces, board, cur_height):
        direction = 0
        h = pieces[0].get_height()
        w = pieces[0].get_width()
        r_loc = 0
        c_loc = self.col

        if c_loc + w > len(board[0]):
            c_loc = 0
        
        self.col = c_loc + w

        return r_loc, c_loc
        
