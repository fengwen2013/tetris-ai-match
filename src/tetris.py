import time

from optparse import OptionParser
from model import Board
from bots.DefaultBot import StackBot, RandomBot

class Tetris():
    mode = 'auto'

    def __init__(self):
        self.board1 = Board(10, 22, StackBot())
        self.board2 = Board(10, 22, RandomBot())

        self.start()

    def start(self):
        self.compete(self.board1, self.board2)

    def compete(self, b1, b2):
        while True:
            if Tetris.mode == 'auto':
                time.sleep(1)
            else:
                input()

            Board.create_piece()
            l1 = b1.get_attack_points()
            l2 = b2.get_attack_points()

            print('l1: %d; l2: %d' % (l1, l2))
            b1.get_attacked(l2)
            b2.get_attacked(l1)

            s1, _, _ = b1.get_board_state()
            s2, _, _ = b2.get_board_state()

            self.print_game(s1, s2)

            if b1.defeated() or b2.defeated():
                break

        if b1.defeated() and not b2.defeated():
            print('Player2 won')
        elif b2.defeated() and not b1.defeated():
            print('Player1 won')
        else:
            print('Tie')

    def print_game(self, s1, s2):
        l = len(s1)

        for i in range(0, l):
            str1 = ''.join(['{:4}'.format(item) for item in s1[l - i - 1]])
            str2 = ''.join(['{:4}'.format(item) for item in s2[l - i - 1]])

            print('%s\t\t\t|\t\t\t%s' % (str1, str2))

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-m", "--mode", dest = "mode", default = "manual",
        help = "Set game mode: [auto | manual]")

    (options, args) = parser.parse_args()
    if options.mode == 'manual' or options.mode == 'auto':
        Tetris.mode = options.mode

    tetris = Tetris()
