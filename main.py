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

# list of other tokens
tokens = [
    'ID',
    'NUMBER',
    'COMMA',
    'FULLSTOP',
    'QUESTIONMARK'
]

tokens += list(reserved.values())

# regex for lexer

def t_ID(t):
    r'[a-zA-Z][a-zA-Z0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t

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

# currently unused, but added as per spec sheet
def t_QUESTIONMARK(t):
    r'\?'
    return t

t_ignore = ' \t'

def t_error(t):
    print('Illegal token in lexer') # only for debugging, remove later
    t.lexer.skip(1)
    print_on_stderr()

# build the lexer
lexer = lex.lex()

# cfg for parser

# top level rule
def p_game(p):
    '''
    game : statement
         | nofullstop
         | invalidvarname FULLSTOP
    '''
    # if object starts with a 'warn' then there was some error detection in lower levels
    # error msg has been displayed therefore we do not process this
    if not p[1][0].startswith('warn'):
        run(p[1])

def p_statement(p):
    '''
    statement : move FULLSTOP
              | assign FULLSTOP
              | name FULLSTOP
              | query FULLSTOP
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
    # check if <<x>>,<<y>> are valid indices
    # otherwise prefix 'warn' to p[0] which is passed to the next level up
    if not (1 <= p[4] <= 4 and 1 <= p[6] <= 4):
        print('2048> There is not tile like that. The tile co-ordinates must be in the range 1,2,3,4.')
        p[0] = ('warn_assign', p[2], (p[4], p[6]))
        print_on_stderr()
    else:
        p[0] = ('assign', p[2], (p[4], p[6]))

def p_name(p):
    '''
    name : VAR ID IS NUMBER COMMA NUMBER
    '''
    # check if <<x>>,<<y>> are valid indices
    # otherwise prefix 'warn' to p[0] which is passed to the next level up
    if not (1 <= p[4] <= 4 and 1 <= p[6] <= 4):
        print('2048> There is not tile like that. The tile co-ordinates must be in the range 1,2,3,4.')
        p[0] = ('warn_name', p[2], (p[4], p[6]))
        print_on_stderr()
    else:
        p[0] = ('name', p[2], (p[4], p[6]))

def p_query(p):
    '''
    query : VALUE IN NUMBER COMMA NUMBER
    '''
    # check if <<x>>,<<y>> are valid indices
    # otherwise prefix 'warn' to p[0] which is passed to the next level up
    if not (1 <= p[3] <= 4 and 1 <= p[5] <= 4):
        print('2048> There is not tile like that. The tile co-ordinates must be in the range 1,2,3,4.')
        p[0] = ('warn_query', (p[3], p[5]))
        print_on_stderr()
    else:
        p[0] = ('query', (p[3], p[5]))

def p_invalidvarname(p):
    '''
    invalidvarname : VAR error IS NUMBER COMMA NUMBER
    '''
    # we handle this separately via error recovery process (parser resynchronization)
    print('2048> Syntax error!')
    print('2048> Invalid token for variable name')
    p[0] = ('warn_namevar', p[2], (p[4], p[6]))

    # no print_on_stderr() here since it's already done in p_error()

def p_nofullstop(p):
    '''
    nofullstop : move
               | assign
               | name
               | query
               | invalidvarname
    '''
    # we cannot handle errors at the end of the input sentence
    # therefore we added it as a separate rule and explicitly marked an syntax error.
    print('2048> Syntax error!')
    print('2048> You should end a command with a fullstop.')
    p[0] = ('warn_fullstop', p[1])
    print_on_stderr()

def p_error(p):
    # each time a parser is unable to match the current token with any rule
    # this method is called.
    # error recovery begins from this method.
    # parser will try to search in rules that match upto before the
    # erraneous token and 'error' token after that. (see p_invalidvarname rule)
    print('2048> Sorry, I do not understand that.')
    print_on_stderr()

# build the parser
parser = yacc.yacc()

def run(stmt):
    board = global_env['board']
    if stmt[0] == 'move':
        resp = board.apply_move(stmt)
        if resp['status'] == 1:
            print('2048> Thanks,', stmt[2].lower(), 'move done, random tile added.')
            print('2048> The current state is:')
            board.print_board()
            print_on_stderr(board.board)
        else:
            print_on_stderr()
    elif stmt[0] == 'assign':
        resp = board.apply_assign(stmt)
        if resp['status'] == 1:
            print('2048> Thanks, assignment done.')
            print('2048> The current state is:')
            board.print_board()
            print_on_stderr(board.board)
        else:
            print_on_stderr()
    elif stmt[0] == 'name':
        resp = board.apply_name(stmt)
        if resp['status'] == 1:
            print('2048> Thanks, naming done.')
            print_on_stderr(board.board)
        else:
            print_on_stderr()
    else:
        resp = board.apply_query(stmt)
        if resp[status] == 1:
            print('2048> Thanks, querying done')
            print('2048> Current value:', resp['data']['value'])
            print_on_stderr(board.board)
        else:
            print_on_stderr()

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
    print_on_stderr(board.board)
    while 1:
        try:
            inp = input('2048> Please type a command.\n----> ')
            parser.parse(inp)
        except KeyboardInterrupt:
            print()
            break
        except EOFError:
            print()
            break
