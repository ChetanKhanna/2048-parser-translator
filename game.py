import random
import copy

class Board:
    def __init__(self, board=None):
        if not board:
            self.board = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
        else:
            self.board = board
        self.changed = False
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
        self.empty_cells = []
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
        self.changed = False
        if move[2] == 'LEFT':
            self._shift_left()
            self._merge_left(move[1])
            self._shift_left()
        elif move[2] == 'RIGHT':
            self._shift_right()
            self._merge_right(move[1])
            self._shift_right()
        elif move[2] == 'UP':
            self.board = [list(i) for i in zip(*self.board)]
            self._shift_left()
            self._merge_left(move[1])
            self._shift_left()
            self.board = [list(i) for i in zip(*self.board)]
        else:
            self.board = [list(i) for i in zip(*self.board)]
            self._shift_right()
            self._merge_right(move[1])
            self._shift_right()
            self.board = [list(i) for i in zip(*self.board)]
        if self.changed:
            self.find_empty_cells()
            self.fill_random_tile()

    def _shift_left(self):
        for i in range(4):
            tmp = [non_zero for non_zero in self.board[i] if non_zero!=0] \
                            + [zero for zero in self.board[i] if zero==0]
            if tmp != self.board[i]:
                self.board[i] = tmp
                self.changed = True

    def _shift_right(self):
        for i in range(4):
            tmp = [zero for zero in self.board[i] if zero == 0] \
                    + [non_zero for non_zero in self.board[i] if non_zero != 0]
            if tmp != self.board[i]:
                self.board[i] = tmp
                self.changed = True

    def _merge_left(self, op):
        for i in range(4):
            for j in range(3):
                if self.board[i][j] > 0 and self.board[i][j] == self.board[i][j+1]:
                    self.changed = True
                    if op == 'ADD':
                        self.board[i][j] += self.board[i][j+1]
                    elif op == 'SUBTRACT':
                        self.board[i][j] -= self.board[i][j+1]
                    elif op == 'MULTIPLY':
                        self.board[i][j] *= self.board[i][j+1]
                    else:
                        self.board[i][j] /= self.board[i][j+1]
                    self.board[i][j+1] = 0

    def _merge_right(self, op):
        for i in range(4):
            for j in range(3,0,-1):
                if self.board[i][j] > 0 and self.board[i][j] == self.board[i][j-1]:
                    self.changed = True
                    if op == 'ADD':
                        self.board[i][j] += self.board[i][j-1]
                    elif op == 'SUBTRACT':
                        self.board[i][j] -= self.board[i][j-1]
                    elif op == 'MULTIPLY':
                        self.board[i][j] *= self.board[i][j-1]
                    else:
                        self.board[i][j] /= self.board[i][j-1]
                    self.board[i][j-1] = 0

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
board.apply_move(('move', 'MULTIPLY', 'LEFT'))
print()
board.print_board()
print()
board.apply_move(('move', 'MULTIPLY', 'LEFT'))
print()
board.print_board()
print()
board.apply_move(('move', 'MULTIPLY', 'LEFT'))
print()
board.print_board()