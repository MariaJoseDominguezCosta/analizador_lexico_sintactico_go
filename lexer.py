import ply.lex as lex

# Lista de tokens
tokens = (
    'ID',         # Identificador - variable
    'TIPO_ENTERO',# Tipo de dato entero
    'ENTERO',     # Números enteros
    'FLOTANTE',   # Números de punto flotante
    'CADENA',     # Cadenas de texto
    'CARACTER',   # Caracteres individuales
    'OP_SUMAR',        # Operador de suma
    'OP_RESTAR',      # Operador de resta
    'OP_MULTIPLICAR',# Operador de multiplicación
    'OP_DIVIDIR',    # Operador de división
    'OP_ASIGNAR', # Operador de asignación
    'PUNTO',    
    'PUNTO_COMA', # Punto y coma
    'DOS_PUNTOS', # Dos puntos
    'COMA',       # Coma
    'PARENTESIS_IZQ',  # Paréntesis izquierdo
    'PARENTESIS_DER',  # Paréntesis derecho
    'SI',         # Palabra clave SI (if)
    'SINO',       # Palabra clave SINO (else)
    'MIENTRAS',   # Palabra clave MIENTRAS (while)
    'FALSO',
    'NULO',
    'VERDADERO',
    'ALIAS',
    'ROMPER_BUCLE',
    'CLASE',
    'DEFINE_FUNCIONES',
    'EXCEPCIONES',
    'DEFINIR_BLOQUE',
    'PARA',
    'DESDE',
    'IMPORTAR',
    'OP_LOGICO_O',
    'OP_LOGICO_NOT',
    'RETORNAR',
    'MODULO',
    'POTENCIA',
    'OP_LOGICO_Y',
    'MENORQUE',
    'MAYORQUE',
    'CORCHETE_IZQ',
    'CORCHETE_DER',
    'LLAVE_IZQ',
    'LLAVE_DER',
    'COMILLA_DOBLE',
    'COMENTARIO_UNA_LINEA',
    'DIFERENTE',
    'IGUAL',
    'MAYORIGUAL',
    'MENORIGUAL',
    'MAS_MAS',
    'MODULO_MATEMATICO',
    'PRINT1',
    'PRINT2',
    'PRINT3',
    'EN',
    'OP_INCREMENTO',
    'RANGO',
    'SINOSI',
    # ... aquí puedes agregar más tokens según tus necesidades

)

# Expresiones regulares para tokens
t_OP_SUMAR = r'\+'
t_OP_RESTAR = r'-'
t_OP_MULTIPLICAR = r'\*'
t_OP_DIVIDIR = r'/'
t_OP_ASIGNAR = r'='
t_PUNTO = r'\.'
t_PUNTO_COMA = r';'
t_DOS_PUNTOS = r':'
t_COMA = r','
t_PARENTESIS_IZQ = r'\('
t_PARENTESIS_DER = r'\)'


t_MODULO = r'\%'
t_POTENCIA = r'(\*{2} | \^)'
t_OP_LOGICO_Y = r'\&\&'
t_OP_LOGICO_O = r'\|{2}'
t_MENORQUE = r'<'
t_MAYORQUE = r'>'
t_CORCHETE_IZQ = r'\['
t_CORCHETE_DER = r'\]'
t_LLAVE_IZQ = r'{'
t_LLAVE_DER = r'}'
t_COMILLA_DOBLE = r'\"'
# Definición de la regla para OP_INCREMENTO
t_OP_INCREMENTO = r'\+='

# Expresiones regulares para identificadores y palabras reservadas
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    
    palabras_reservadas = {
        'if': 'SI',
        'else': 'SINO',
        'while': 'MIENTRAS',
        'False':'FALSO',
        'None':'NULO',
        'True':'VERDADERO',
        'and':'OP_LOGICO_Y',
        'or':'OP_LOGICO_O',
        'not' : 'OP_LOGICO_NOT',
        'as':'ALIAS',
        'break':'ROMPER_BUCLE',
        'class':'CLASE',
        'def':'DEFINE_FUNCIONES',
        'except':'EXCEPCIONES',
        'finally':'DEFINIR_BLOQUE',
        'for':'PARA',
        'from':'DESDE',
        'import':'IMPORTAR',
        'return': 'RETORNAR',
        'math' : 'MODULO_MATEMATICO',
        'in': 'EN',
        'range': 'RANGO',
        'system' : 'PRINT1',
        'out' : 'PRINT2',
        'println' : 'PRINT3',
        'elif' : 'SINOSI',
        # ... más palabras reservadas pueden ser añadidas aquí
    }
    t.type = palabras_reservadas.get(t.value, 'ID')  # Si no es palabra reservada, es un ID
    return t

# Expresiones regulares para números
def t_FLOTANTE(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_ENTERO(t):
    r'\d+'
    t.value = int(t.value)
    return t


# Expresiones regulares para cadenas de texto
def t_CADENA(t):
    r'(\'[^\']*\'|\"[^\"]*\")'  # Esta expresión regular coincide con comillas simples o dobles
    t.value = t.value[1:-1]  # Elimina las comillas alrededor de la cadena
    return t

# Expresiones regulares para caracteres individuales
def t_CARACTER(t):
    r'\'.\''
    t.value = t.value[1]
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_space(t):
    r'\s+'
    t.lexer.lineno += len(t.value)
        
# Ignorar caracteres como espacios y saltos de línea
t_ignore = '\t'

def t_MAS_MAS(t):
    r'\+\+'
    return t

def t_MENORIGUAL(t):
    r'<='
    return t

def t_MAYORIGUAL(t):
    r'>='
    return t

def t_IGUAL(t):
    r'=='
    return t

def t_DIFERENTE(t):
    r'!='
    return t


# Expresión regular para comentarios de una sola línea
def t_COMENTARIO_UNA_LINEA(t):
    r'\#.*'
    t.value = t.value[1:]  # Elimina el signo de número (#) del comentario
    return t

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