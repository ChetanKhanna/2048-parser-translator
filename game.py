import random
import copy

class Board:
    def __init__(self, board=None):
        if not board:
            self.board = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
        else:
            self.board = board
        self.board_copy = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
        self.empty_cells = []
        for i in range(4):
            for j in range(4):
                self.empty_cells.append((i,j))
        self.name_map = dict()
    
    def fill_random_tile(self):
        row, col = random.choice(self.empty_cells)
        if random.uniform(0,1) < 0.6:
            self.board[row][col] = 2
        else:
            self.board[row][col] = 4
        self.empty_cells.remove((row, col))
    
    def initiate_new_board(self):
        self.board = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
        for i in range(4):
            for j in range(4):
                self.empty_cells.append((i,j))
        self.fill_random_tile()

    def find_empty_cells(self):
        self.empty_cells = []
        for i in range(4):
            for j in range(4):
                if self.board[i][j] == 0:
                    self.empty_cells.append((i,j))

    def apply_move(self, move):
        if move[1] not in ['LEFT', 'RIGHT', 'UP', 'DOWN']:
            print('Invalid move!')
            return -1
        if move[1] == 'LEFT':
            self._shift_left()
            # self._merge_and_operate(move[2])
            self._shift_left()
        elif move[1] == 'RIGHT':
            self._shift_right()
            # self._merge_and_operate(move[2])
            self._shift_right()
        # elif move[1] == 'UP':
        #     self._shift_up()
        #     self._merge_and_operate(move[2])
        #     self._shift_up()
        # else:
        #     self._shift_down()
        #     self._merge_and_operate(move[2])
        #     self._shift_down()
        self.fill_random_tile()
        return 1
    
    def _shift_left(self):
        for i in range(4):
            self.board[i] = [non_zero for non_zero in self.board[i] if non_zero!=0] \
                            + [zero for zero in self.board[i] if zero==0]
        self.find_empty_cells()
    
    def _shift_right(self):
        for i in range(4):
            self.board[i] = [zero for zero in self.board[i] if zero == 0] \
                    + [non_zero for non_zero in self.board[i] if non_zero != 0]
        self.find_empty_cells()
    
    # def _shift_up():

        
    
    def print_board(self):
        for i in range(4):
            print('----'*8)
            for j in range(4):
                val = self.board[i][j]
                if val == 0:
                    val = ' '
                    space = '     '
                else:
                    if 0 < val < 10:
                        space = '     '
                    elif 10 < val < 100:
                        space = '    '
                    elif 100 < val < 1000:
                        space = '   '
                    elif 1000 < val < 10000:
                        space = '  '
                    else:
                        space = ' '
                print('|', val, end='     ')
            print('|')

board = Board()
board.initiate_new_board()
board.print_board()
board.apply_move(('move', 'RIGHT', 'ADD'))
print()
board.print_board()