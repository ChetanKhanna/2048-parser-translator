import ply.lex as lex
import ply.yacc as yacc

# list of token names

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
    'VALUE IN': 'QUERY'
}

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
    'POS',
    'VARNAME',
    'VALUE',
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

def t_POS(t):
    r'[1234],[1234]'
    return t

def t_VARNAME(t):
    r'[a-zA-Z0-9]+'
    t.type = reserved.get(t.value, 'VARNAME')
    return t

t_ignore = ' \t'

def t_error(t):
    print('Illegal token in lexer') # only for debugging, remove later
    t.lexer.skip(1)

# build the lexer
lexer = lex.lex()

while 1:
    try:
        inp = input('2048> Please type a command.\n----> ')
        print('INPUT: ', inp)
        lexer.input(inp)
        for tok in lexer:
            print(tok)
    except KeyboardInterrupt:
        print()
        break
    except EOFError:
        print()
        break
