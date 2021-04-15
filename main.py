import sys
import ply.lex as lex
import ply.yacc as yacc
from game import Board


global_env = dict()

# reserved token
reserved = {
    'ADD': 'ADD',
    'SUBTRACT': 'SUBTRACT',
    'MULTIPLY': 'MULTIPLY',
    'DIVIDE': 'DIVIDE',
    'LEFT': 'LEFT',
    'RIGHT': 'RIGHT',
    'UP': 'UP',
    'DOWN': 'DOWN',
    'ASSIGN': 'ASSIGN',
    'TO': 'TO',
    'VAR': 'VAR',
    'IS': 'IS',
    'VALUE': 'VALUE',
    'IN': 'IN',
}

# list of token names
tokens = [
    # 'ADD',
    # 'SUBTRACT',
    # 'MULTIPLY',
    # 'DIVIDE',
    # 'LEFT',
    # 'RIGHT',
    # 'UP',
    # 'DOWN',
    # 'ASSIGN',
    # 'TO',
    # 'VAR',
    # 'IS',
    # 'QUERY',
    # 'POS',
    # 'VARNAME',
    # 'VAL',
    # 'FULLSTOP',
    'ID',
    'NUMBER',
    'COMMA',
    'FULLSTOP',
    'QUESTIONMARK'
]

tokens += list(reserved.values())

# token
# t_ADD       = r'ADD'
# t_SUBTRACT  = r'SUBTRACT'
# t_MULTIPLY  = r'MULTIPLY'
# t_DIVIDE    = r'DIVIDE'
# t_LEFT      = r'LEFT'
# t_RIGHT     = r'RIGHT'
# t_UP        = r'UP'
# t_DOWN      = r'DOWN'
# t_ASSIGN    = r'ASSIGN'
# t_TO        = r'TO'
# t_VAR       = r'VAR'
# t_IS        = r'IS'
# t_QUERY     = r'VALUE IN'
# t_POS       = r'[1234],[1234]'

# def t_POS(t):
#     r'[1234],[1234]'
#     return t

def t_ID(t):
    r'[a-zA-Z][a-zA-Z0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t

# def t_VAL(t):
#     r'[0-9]+'
#     return t

def t_NUMBER(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t

def t_COMMA(t):
    r'\,'
    return t

def t_FULLSTOP(t):
    r'\.'
    return t

def t_QUESTIONMARK(t):
    r'\?'
    return t

t_ignore = ' \t'

def t_error(t):
    print('Illegal token in lexer') # only for debugging, remove later
    t.lexer.skip(1)

# build the lexer
lexer = lex.lex()

def p_game(p):
    '''
    game : statement
         | warn
    '''
    if str(p.slice[1]) == 'warn':
        print('You should end a command with a fullstop.')
    else:
        run(p[1])

def p_statement(p):
    '''
    statement : move FULLSTOP
              | assign FULLSTOP
              | name FULLSTOP
              | query FULLSTOP
    '''
    p[0] = p[1]

def p_warn(p):
    '''
    warn : move
         | assign
         | name
         | query
    '''
    p[0] = p[1]

def p_move(p):
    '''
    move : ADD UP
         | ADD DOWN
         | ADD LEFT
         | ADD RIGHT
         | SUBTRACT UP
         | SUBTRACT DOWN
         | SUBTRACT LEFT
         | SUBTRACT RIGHT
         | MULTIPLY UP
         | MULTIPLY DOWN
         | MULTIPLY LEFT
         | MULTIPLY RIGHT
         | DIVIDE UP
         | DIVIDE DOWN
         | DIVIDE LEFT
         | DIVIDE RIGHT
    '''
    p[0] = ('move', p[1], p[2])

def p_assign(p):
    '''
    assign : ASSIGN NUMBER TO NUMBER COMMA NUMBER
    '''
    p[0] = ('assign', p[2], (p[4], p[6]))

def p_name(p):
    '''
    name : VAR ID IS NUMBER COMMA NUMBER
    '''
    p[0] = ('name', p[2], (p[4], p[6]))

def p_query(p):
    '''
    query : VALUE IN NUMBER COMMA NUMBER
    '''
    p[0] = ('query', (p[3], p[5]))

def p_error(p):
    print('Syntac error!')

parser = yacc.yacc()

def run(ast):
    board = global_env['board']
    if ast[0] == 'move':
        resp = board.apply_move(ast)
        if resp['status'] == 1:
            print('2048> Thanks,', ast[2].lower(), 'move done, random tile added.')
            print('2048> The current state is:')
            board.print_board()
            print_on_stderr(board.board)
    elif ast[0] == 'assign':
        resp = board.apply_assign(ast)
        if resp['status'] == 1:
            print('2048> Thanks, assignment done.')
            print('2048> The current state is:')
            board.print_board()
            print_on_stderr(board.board)
    elif ast[0] == 'name':
        resp = board.apply_name(ast)
        if resp['status'] == 1:
            print('2048> Thanks, naming done.')
            print_on_stderr(board.board)
    else:
        resp = board.apply_query(ast)
        if resp[status] == 1:
            print('2048> Thanks, querying done')
            print('2048> Current value:', resp['data']['value'])
            print_on_stderr(board.board)

def print_on_stderr(board=None):
    if board:
        for i in range(4):
            for j in range(4):
                print(board[i][j][0], end=' ', file=sys.stderr)
        for i in range(4):
            for j in range(4):
                if board[i][j][1]:
                    print(i+1, end=',', file=sys.stderr)
                    print(j+1, end='', file=sys.stderr)
                    print(*board[i][j][1], sep=',', end=' ', file=sys.stderr)
        print(file=sys.stderr)
    else:
        print(-1, file=sys.stderr)

if __name__ == '__main__':
    board = Board()
    global_env['board'] = board
    board.initiate_new_board()        
    print('2048> Hi, I am 2048-game Engine.')
    print('2048> The start state is:')
    board.print_board()
    while 1:
        try:
            inp = input('2048> Please type a command.\n----> ')
            # lexer.input(inp)
            # for tok in lexer:
            #     print(tok)
            parser.parse(inp)
        except KeyboardInterrupt:
            print()
            break
        except EOFError:
            print()
            break
