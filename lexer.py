import ply.lex as lex

# Lista de tokens
tokens = (
    'IDENTIFIER',
    'MAIN',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'LPAREN',
    'RPAREN',
    'LBRACE',
    'RBRACE',
    'PACKAGE',
    'IMPORT',
    'FUNC',
    'FMT',
    'PRINTLN',
    'DOT',
    'INT_LIT',
    'FLOAT_LIT',
    'IMAGINARY_LIT',
    'RUNE_LIT',
    'STRING_LIT',
    'MOD',
    'AND',
    'OR',
    'XOR',
    'LSHIFT',
    'RSHIFT',
    'AND_NOT',
    'PLUS_ASSIGN',
    'MINUS_ASSIGN',
    'TIMES_ASSIGN',
    'DIVIDE_ASSIGN',
    'MOD_ASSIGN',
    'AND_ASSIGN',
    'OR_ASSIGN',
    'XOR_ASSIGN',
    'LSHIFT_ASSIGN',
    'RSHIFT_ASSIGN',
    'AND_NOT_ASSIGN',
    'AND_AND',
    'OR_OR',
    'ARROW',
    'INC',
    'DEC',
    'EQL',
    'NEQ',
    'LSS',
    'LEQ',
    'GTR',
    'GEQ',
    'ASSIGN',
    'DECLARE_ASSIGN',
    'NOT',
    'ELLIPSIS',
    'LBRACK',
    'RBRACK',
    'COMMA',
    'PERIOD',
    'COLON',
    'VAR',
    'IF',
    'ELSE',
    'FOR',
    'RETURN',
    'CONST'
    # ... aquí puedes agregar más tokens según tus necesidades

)

# Expresiones regulares para tokens
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_DOT = r'\.'
t_MOD = r'%'
t_AND = r'&'
t_OR = r'\|'
t_XOR = r'\^'
t_LSHIFT = r'<<'
t_RSHIFT = r'>>'
t_AND_NOT = r'&\^'
t_PLUS_ASSIGN = r'\+='
t_MINUS_ASSIGN = r'-='
t_TIMES_ASSIGN = r'\*='
t_DIVIDE_ASSIGN = r'/='
t_MOD_ASSIGN = r'%='
t_AND_ASSIGN = r'&='
t_OR_ASSIGN = r'\|='
t_XOR_ASSIGN = r'\^='
t_LSHIFT_ASSIGN = r'<<='
t_RSHIFT_ASSIGN = r'>>='
t_AND_NOT_ASSIGN = r'&\^='
t_AND_AND = r'&&'
t_OR_OR = r'\|\|'
t_ARROW = r'<-'
t_INC = r'\+\+'
t_DEC = r'--'
t_EQL = r'=='
t_NEQ = r'!='
t_LSS = r'<'
t_LEQ = r'<='
t_GTR = r'>'
t_GEQ = r'>='
t_ASSIGN = r'='
t_DECLARE_ASSIGN = r':='
t_NOT = r'!'
t_ELLIPSIS = r'\.\.\.'
t_LBRACK = r'\['
t_RBRACK = r'\]'
t_COMMA = r','
t_PERIOD = r'\.'
t_COLON = r':'

# Expresiones regulares para identificadores y palabras reservadas
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    
    palabras_reservadas = {
        'package': 'PACKAGE',
        'import': 'IMPORT',
        'func': 'FUNC',
        'fmt': 'FMT',
        'Println': 'PRINTLN',
        'break': 'BREAK',
        'case': 'CASE',
        'chan': 'CHAN',
        'const': 'CONST',
        'continue': 'CONTINUE',
        'default': 'DEFAULT',
        'defer': 'DEFER',
        'else': 'ELSE',
        'fallthrough': 'FALLTHROUGH',
        'for': 'FOR',
        'func': 'FUNC',
        'go': 'GO',
        'goto': 'GOTO',
        'if': 'IF',
        'interface': 'INTERFACE',
        'map': 'MAP',
        'range': 'RANGE',
        'return': 'RETURN',
        'select': 'SELECT',
        'struct': 'STRUCT',
        'switch': 'SWITCH',
        'type': 'TYPE',
        'var': 'VAR',
        'true': 'TRUE',
        'false': 'FALSE',
        'nil': 'NIL',
        'main': 'MAIN'
        # ... más palabras reservadas pueden ser añadidas aquí
    }
    t.type = palabras_reservadas.get(t.value, 'IDENTIFIER')  # Si no es palabra reservada, es un ID
    return t


def t_INT_LIT(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_FLOAT_LIT(t):
    r'\d+\.\d*([eE][-+]?\d+)?'
    t.value = float(t.value)
    return t

def t_IMAGINARY_LIT(t):
    r'\d+(\.\d*)?[iI]'
    return t

def t_RUNE_LIT(t):
    r'\'([^\\\n]|(\\.))*?\''
    return t

def t_STRING_LIT(t):
    r'\"([^\\\n]|(\\.))*?\"'
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lexpos += len(t.value)

def t_space(t):
    r'\s+'
    t.lexer.lineno += t.value.count('\n')
    
# Ignorar caracteres como espacios y saltos de línea

t_ignore = ' \t'

# Manejo de errores léxicos
def t_error(t):
    print("Ilegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    return t


# instanciamos el analizador lexico
lexer = lex.lex()

def tokenize(data):
    lexer.input(data)
    tokens = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        tokens.append((tok.type, tok.value, tok.lineno, tok.lexpos))
    return tokens