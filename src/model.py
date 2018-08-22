import random
from bots.DefaultBot import RandomBot

class Piece:
    piece_shape = [
        [[1, 1, 1],
         [0, 1, 0]],

        [[0, 2, 2],
         [2, 2, 0]],

        [[3, 3, 0],
         [0, 3, 3]],

        [[0, 0, 4],
         [4, 4, 4]],

        [[5, 0, 0],
         [5, 5, 5]],

        [[6, 6],
         [6, 6]],

        [[7, 7, 7, 7]]
    ]

    def __init__(self, piece_id):
        self.shape = Piece.piece_shape[piece_id]

    def rotate(self, direction):
        for i in range(0, direction + 1):
            self.rotate_90_degree()


    def rotate_90_degree(self):
        original = self.shape
        nr = len(original)
        nc = len(original[0])
        shape = [[0] * nr for i in range(nc)]

        for i in range(0, nr):
            for j in range(0, nc):
                shape[j][nr - i - 1] = original[i][j]
        
        self.shape = shape

    def get_height(self):
        return len(self.shape)

    def get_width(self):
        return len(self.shape[0])

    def get_shape(self):
        return self.shape;
        

class Board:
    num_pieces = len(Piece.piece_shape)
    sequence = list(range(0, num_pieces))
    sequence_index = 2
    cur_pieces = (Piece(sequence[0]), Piece(sequence[1]))
    
    def __init__(self, max_width=10, max_height=22, bot=RandomBot()):
        self.max_width = max_width
        self.max_height = max_height
        self.cur_height = 0;
        self.board = [[0] * max_width for i in range(max_height)]

        self.attack_points = 0
        self.total_lines = 0
        self.bot = bot

    @staticmethod
    def create_piece():
        sequence = Board.sequence;
        index = Board.sequence_index;
        piece = Board.cur_pieces[1]
        next_piece = Piece(sequence[index])

        if index < len(sequence) - 1:
            index += 1
        else:
            Board.shuffle(sequence)
            index = 0

        Board.sequence = sequence
        Board.sequence_index = index
        Board.cur_pieces = (piece, next_piece)

    @staticmethod
    def get_cur_pieces():
        return Board.cur_pieces

    @staticmethod
    def shuffle(sequence):
        i = 0
        l = len(sequence)
        for i in range(l):
            ri = random.randint(0, i)

            tmp = sequence[i]
            sequence[i] = sequence[ri]
            sequence[ri] = tmp

    def merge(self, piece, r_loc, c_loc):
        self.add_piece(piece, r_loc, c_loc)
        self.remove_lines(piece, r_loc)

    # return leftmost and lowest
    def add_piece(self, piece, r_loc, c_loc):
        print('add_piece')        

        cur_height = self.cur_height
        piece_height = piece.get_height()
        piece_width = piece.get_width()
        piece_shape = piece.get_shape()

        print(piece_shape)
        print('r_loc: %d; c_loc: %d' % (r_loc, c_loc))

        r_loc = 0;
        low_height, high_height = self.get_range_height(c_loc, c_loc + piece_width)

        for r in range(low_height, high_height + 1):
            collision = self.check_collision(piece, r, c_loc)
            if not collision:
                r_loc = r;
                for i in range(0, len(piece_shape)):
                    for j in range(0, len(piece_shape[i])):
                        r = r_loc + piece_height - i - 1
                        c = c_loc + j
                        if piece_shape[i][j] != 0:
                            self.board[r][c] = piece_shape[i][j]
                break;

        low_height, high_height = self.get_range_height(c_loc, c_loc + piece_width)
        self.cur_height = max(high_height, self.cur_height)
        self.attack_points = 0

    def get_range_height(self, start, end):
        low_height = 0;
        high_height = 0;

        print('start: %d; end: %d' % (start, end))

        for i in range(0, self.max_height):
            if self.board[i][start] != 0:
                low_height = i + 1
                high_height = i + 1

        for i in range(start + 1, end):
            height = 0
            for j in range(0, self.max_height):
                # print('r: %d; c: %d' % (j, i))
                if self.board[j][i] != 0:
                    height = j + 1

            low_height = min(low_height, height)
            high_height = max(high_height, height)

        return low_height, high_height

    def check_collision(self, piece, r_loc, c_loc):
        piece_shape = piece.get_shape()
        piece_height = piece.get_height()

        for i in range(0, len(piece_shape)):
            for j in range(0, len(piece_shape[i])):
                r = r_loc + piece_height - i - 1
                c = c_loc + j
                if r >= self.max_height or (self.board[r][c] != 0 and piece_shape[i][j] != 0):
                    return True

        return False

    def remove_lines(self, piece, r_loc):
        print('remove_lines')

        piece_height = piece.get_height()
        cur_height = self.cur_height
        l = r_loc - 1 # l is highest incomplete row
        n = 0;

        for i in range(r_loc, r_loc + cur_height):
            if not self.is_full_line(self.board[i]):
                l += 1
                self.board[l] = self.board[i]
            else:
                n += 1

        for i in range(l + 1, r_loc + cur_height):
            self.board[i] = [0] * self.max_width
       
        self.attack_points = n; 
        self.cur_height -= n;
        self.total_lines += n;

    def is_full_line(self, line):
        for i in range(0, len(line)):
            if line[i] == 0 or line[i] == -1:
                return False

        return True

    def get_attacked(self, num_lines):
        # 1 <= num_lines <= 4

        max_height = self.max_height

        for i in range(self.cur_height + num_lines - 1, -1, -1):
            if i >= num_lines:
                self.board[i] = self.board[i - num_lines]
            else:
                self.board[i] = [-1] * self.max_width


        self.cur_height = min(max_height, self.cur_height + num_lines)

    def defeated(self):
        return self.cur_height >= self.max_height

    def get_attack_points(self):
        bot = self.bot
        pieces = self.get_cur_pieces()
        r_loc, c_loc = bot.next_move(pieces, self.board, self.cur_height)
       
        self.merge(pieces[0], r_loc, c_loc)

        return self.attack_points

    def get_board_state(self):
        print('total_lines: %d; cur_attack_points: %d; cur_height: %d' %
            (self.total_lines, self.attack_points, self.cur_height))
        return self.board, self.total_lines, self.cur_height

    def print_state(self):
        matrix = self.board
        print('state')
        print('\n'.join([''.join(['{:4}'.format(item) for item in row]) for row in reversed(matrix)]))
