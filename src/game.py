import time
import pygame, sys
from model import Board
from bots.DefaultBot import StackBot, RandomBot

cell_size = 20
board_width = 10
board_height = 22
fps = 30

colors = [
    (0, 0, 0),
    (70, 130,  180),
    (100, 200, 115),
    (255, 0, 0),
    (255, 255, 0),
    (50,  220, 50 ),
    (148, 0, 211),
    (150, 160, 210 ),
    (211,  211,  211) 
]

class Game(object):
    def __init__(self):
        pygame.init()
        self.width = cell_size * 2 * (board_width + 15)
        self.height = cell_size * (board_height + 10)
        

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.event.set_blocked(pygame.MOUSEMOTION)

        self.start_game()

    def start_game(self):
        pygame.time.set_timer(pygame.USEREVENT + 1, 1000)

    def draw_board(self, board, offset):
        offsetx, offsety = offset

        for y, row in enumerate(board):
            for x, val in enumerate(row):
                    pygame.draw.rect(self.screen, colors[val],
                        pygame.Rect((offsetx + x) * cell_size, (offsety + y) * cell_size,
                            cell_size, cell_size), 0)

    def draw_piece(self, piece, offset):
        self.draw_board(piece.get_shape(), offset)

    def center_msg(self, msg):
            msg_image =  pygame.font.Font(
                pygame.font.get_default_font(), 50).render(
                    msg, False, (255,255,255), (0,0,0))
        
            center_x, center_y = msg_image.get_size()
            center_x //= 2
            center_y //= 2
        
            self.screen.blit(msg_image, (
              self.width // 2 - center_x,
              self.height // 2 - center_y + 22
            ))

    def start(self, tetris):
        clock = pygame.time.Clock()


        while True:
            time.sleep(1.37)
            winner = tetris.get_winner() 
            pieces = tetris.get_visible_pieces()
            next_piece = pieces[1]

            self.screen.fill((255, 255, 255))
            self.draw_piece(next_piece, (22, 5))
            if winner == 0:
                b1, b2 = tetris.get_state()
                self.draw_board(b1, (5, 5))
                self.draw_board(b2, (32, 5))
            else:
                self.center_msg('Game Over: Player %d is the winner' % winner)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            pygame.display.update()
            clock.tick(fps)

class Tetris():
    mode = 'auto'

    def __init__(self):
        self.board1 = Board(10, 22, StackBot())
        self.board2 = Board(10, 22, RandomBot())

    def get_visible_pieces(self):
        return Board.get_cur_pieces()

    def get_state(self):
        b1 = self.board1
        b2 = self.board2
        l1 = b1.get_attack_points()
        l2 = b2.get_attack_points()
        
        Board.create_piece()
        b1.get_attacked(l2)
        b2.get_attacked(l1)
        s1, _, _ = b1.get_board_state()
        s2, _, _ = b2.get_board_state()

        return self.reverse_row(s1), self.reverse_row(s2)

    def reverse_row(self, state):
        matrix = [row[:] for row in state]
        l = len(matrix)

        for i in range(0, l // 2):
            tmp = matrix[i]
            matrix[i] = matrix[l - i - 1]
            matrix[l - i - 1] = tmp

        return matrix

    def get_winner(self):
        b1 = self.board1
        b2 = self.board2

        if b1.defeated() and not b2.defeated():
            return 2
        elif b2.defeated() and not b1.defeated():
            return 1

        return 0

if __name__ == '__main__':
    game = Game()
    tetris = Tetris()
    game.start(tetris)
