import random
import copy

class Board:
    '''
    General API for the game:
    returns a dictionary with the following keys:
    return = {
        status = 1 for success, -1 for fail
        data = {} of values returned by function or empty if failed or no data
        error = string describing error
    }
    The keys for data dictionary are specified in particular function, if present
    '''
    def __init__(self):
        self.board = [
            [[0, set()], [0, set()], [0, set()], [0, set()]],
            [[0, set()], [0, set()], [0, set()], [0, set()]],
            [[0, set()], [0, set()], [0, set()], [0, set()]],
            [[0, set()], [0, set()], [0, set()], [0, set()]],
        ]
        self.all_names = set()
        self.changed = False
        self.empty_cells = []
        for i in range(4):
            for j in range(4):
                self.empty_cells.append((i,j))
    
    def fill_random_tile(self):
        row, col = random.choice(self.empty_cells)
        if random.uniform(0,1) < 0.6:
            self.board[row][col] = [2, self.board[row][col][1]]
        else:
            self.board[row][col] = [4, self.board[row][col][1]]
        self.empty_cells.remove((row, col))
    
    def initiate_new_board(self):
        self.board = [
            [[0, set()], [0, set()], [0, set()], [0, set()]],
            [[0, set()], [0, set()], [0, set()], [0, set()]],
            [[0, set()], [0, set()], [0, set()], [0, set()]],
            [[0, set()], [0, set()], [0, set()], [0, set()]],
        ]
        self.empty_cells = []
        for i in range(4):
            for j in range(4):
                self.empty_cells.append((i,j))
        self.fill_random_tile()

    def find_empty_cells(self):
        self.empty_cells = []
        for i in range(4):
            for j in range(4):
                if self.board[i][j][0] == 0:
                    self.empty_cells.append((i,j))

    def apply_move(self, move):
        self.changed = False
        try:
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
            return {'status': 1, 'data': {}, 'error': ''}
        except Exception as e:
            return {'status': -1, 'data': {}, 'error': e}

    def _shift_left(self):
        for i in range(4):
            tmp = [non_zero for non_zero in self.board[i] if non_zero[0] != 0] \
                            + [zero for zero in self.board[i] if zero[0] == 0]
            if tmp != self.board[i]:
                self.board[i] = tmp
                self.changed = True

    def _shift_right(self):
        for i in range(4):
            tmp = [zero for zero in self.board[i] if zero[0] == 0] \
                    + [non_zero for non_zero in self.board[i] if non_zero[0] != 0]
            if tmp != self.board[i]:
                self.board[i] = tmp
                self.changed = True

    def _merge_left(self, op):
        for i in range(4):
            for j in range(3):
                if self.board[i][j][0] > 0 and self.board[i][j][0] == self.board[i][j+1][0]:
                    self.changed = True
                    if op == 'ADD':
                        self.board[i][j][0] += self.board[i][j+1][0]
                    elif op == 'SUBTRACT':
                        self.board[i][j][0] -= self.board[i][j+1][0]
                    elif op == 'MULTIPLY':
                        self.board[i][j][0] *= self.board[i][j+1][0]
                    else:
                        self.board[i][j][0] /= self.board[i][j+1][0]
                    if self.board[i][j][0] > 0:
                        self.board[i][j][1].update(self.board[i][j+1][1])
                    else:
                        self.board[i][j][1] = set()
                    self.board[i][j+1] = [0, set()]

    def _merge_right(self, op):
        for i in range(4):
            for j in range(3,0,-1):
                if self.board[i][j][0] > 0 and self.board[i][j][0] == self.board[i][j-1][0]:
                    self.changed = True
                    if op == 'ADD':
                        self.board[i][j][0] += self.board[i][j-1][0]
                    elif op == 'SUBTRACT':
                        self.board[i][j][0] -= self.board[i][j-1][0]
                    elif op == 'MULTIPLY':
                        self.board[i][j][0] *= self.board[i][j-1][0]
                    else:
                        self.board[i][j][0] /= self.board[i][j-1][0]
                    if self.board[i][j][0] > 0:
                        self.board[i][j][1].update(self.board[i][j-1][1])
                    else:
                        self.board[i][j][1] = set()
                    self.board[i][j-1] = [0, set()]

    def apply_assign(self, assign):
        try:
            val = assign[1]
            i, j = assign[2]
            self.board[i-1][j-1][0] = val
            return {'status': 1, 'data': {}, 'error': ''}
        except Exception as e:
            return {'status': -1, 'data': {}, 'error': e}
    
    def apply_name(self, name):
        try:
            i, j = name[2]
            if name[1] not in self.all_names:
                self.all_names.add(name[1])
                self.board[i-1][j-1][1].add(name[1])
            return {'status': 1, 'data': {}, 'error': ''}
        except Exception as e:
            return {'status': -1, 'data': {}, 'error': e}

    def apply_query(self, query):
        '''
        data dict keys:
            value : value of stored in cell asked in query
        '''
        try:
            i, j = query[1]
            return {'status': 1, 'data': {'value': self.board[i-1][j-1][0]}, 'error': ''}
        except Exception as e:
            return {'status': -1, 'data': {}, 'error': e}

    def print_board(self):
        for i in range(4):
            print('----'*8)
            for j in range(4):
                val = self.board[i][j][0]
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

# board = Board()
# board.initiate_new_board()
# board.print_board()
# board.apply_move(('move', 'MULTIPLY', 'LEFT'))
# print()
# board.print_board()
# print()
# board.apply_move(('move', 'MULTIPLY', 'LEFT'))
# print()
# board.print_board()
# print()
# board.apply_move(('move', 'MULTIPLY', 'LEFT'))
# print()
# board.print_board()
# board.apply_assign(('assign', 46, (3, 4)))
# print()
# board.print_board()
# board.apply_name(('name', 'xyz', (4, 3)))
# board.apply_name(('name', 'abcd', (4, 3)))
# print()
# print(board.board)
# print(board.all_names)
# res = board.apply_query(('query', (4, 1)))
# print()
# print(res)