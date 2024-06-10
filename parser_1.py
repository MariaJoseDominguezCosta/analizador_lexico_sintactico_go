import ply.yacc as yacc
from semantico import *

variables_inicializadas = {}

# Definición de precedencia para los operadores
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
)


# Diccionario para almacenar los nombres y sus valores
nombres = {}


# Regla para las sentencias (statements)
def p_program(p):
    '''program : statement_list'''
    p[0] = p[1]

# Declaración de paquete
def p_package_declaration(p):
    '''package_declaration : PACKAGE IDENTIFIER'''
    p[0] = p[2]


# Declaración de importación
def p_import_declaration(p):
    '''import_declaration : IMPORT STRING_LIT
    | IMPORT LPAREN import_spec_list RPAREN'''
    if len(p) == 4:
        p[0] = p[3]
    else:
        p[0] = ('import_declaration', p[2])


# Lista de especificaciones de importación
def p_import_spec_list(p):
    '''import_spec_list : import_spec
    | import_spec_list COMMA import_spec'''
    if len(p)==2:
        p[0] = p[1]
    else:
        p[0] = p[1] + p[3]


# Especificación de importación
def p_import_spec(p):
    '''import_spec : STRING_LIT
    | IDENTIFIER STRING_LIT'''
    p[0] = p[1]


# Declaración de función
def p_function_declaration(p):
    '''function_declaration : FUNC IDENTIFIER function_signature function_body'''
    function_name = p[2]
    function_body = p[4]
    p[0] = (function_name, function_body)


# Firma de la función
def p_function_signature(p):
    '''function_signature : LPAREN parameter_list RPAREN
    | LPAREN RPAREN'''
    if len(p) == 4:
        p[0] = p[2]
    else:
        p[0] = None

# Lista de parámetros
def p_parameter_list(p):
    '''parameter_list : parameter_declaration
    | parameter_list COMMA parameter_declaration'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] + p[3]


# Declaración de parámetro
def p_parameter_declaration(p):
    '''parameter_declaration : IDENTIFIER type'''
    p[0] = p[2]


# Tipo de dato
def p_type(p):
    '''type : IDENTIFIER
    | pointer_type
    | array_type'''
    p[0]= p[1]


# Tipo de puntero
def p_pointer_type(p):
    '''pointer_type : TIMES type'''
    p[0]= p[2]


# Tipo de arreglo
def p_array_type(p):
    '''array_type : LBRACK expression RBRACK type'''
    p[0]= p[4]


# Cuerpo de la función
def p_function_body(p):
    '''function_body : block'''
    p[0] = p[1]


# Bloque de código
def p_block(p):
    '''block : LBRACE statement_list RBRACE
    | LBRACE RBRACE'''
    if len(p) == 4:
        p[0] = p[2]
    else:
        p[0] = None


# Lista de declaraciones
def p_statement_list(p):
    '''statement_list : statement
    | statement_list statement'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]


# Declaración
def p_statement(p):
    '''statement : package_declaration import_declaration
    | const_declaration
    | var_declaration
    | simple_statement
    | return_statement
    | if_statement
    | for_statement
    | function_declaration
    | print_statement
    '''
    p[0] = p[1]


# Declaración simple
def p_simple_statement(p):
    '''simple_statement : expression'''
    p[0] = ('simple_statement', p[1])


# Declaración de retorno
def p_return_statement(p):
    '''return_statement : RETURN expression
    | RETURN'''
    if len(p) == 4:
        p[0] = ('return_statement', p[2])
    else:
        p[0] = ('return_statement')


# Declaración de if
def p_if_statement(p):
    '''if_statement : IF expression LBRACE statement_list RBRACE
    | IF expression LBRACE statement_list RBRACE ELSE LBRACE statement_list RBRACE'''
    if p[2]:
        p[0] = 'La condición es verdadera'
    else:
        p[0] = 'La condición es falsa'



# Declaración de for
def p_for_statement(p):
    '''for_statement : FOR expression LBRACE statement_list RBRACE'''
    p[0] = p[2]


# Declaración de impresión
def p_print_statement(p):
    '''print_statement : FMT DOT PRINTLN LPAREN STRING_LIT RPAREN
    | PRINTLN LPAREN STRING_LIT RPAREN'''
    if len(p) == 6:
        print_args = [p[3]]
        formatted_string = ' '.join(map(str, print_args))
        print(formatted_string)
        p[0] = formatted_string
    else:
        print_args = [p[5]]
        formatted_string = ' '.join(map(str, print_args))
        print(formatted_string)
        p[0] = formatted_string

# Declaración de constante
def p_const_declaration(p):
    '''const_declaration : CONST IDENTIFIER ASSIGN expression
    | CONST LPAREN const_spec_list RPAREN'''
    if len(p)==6:
        p[0] = p[4]
    else:
        p[0] = p[3]


# Especificación de constante
def p_const_spec(p):
    '''const_spec : IDENTIFIER ASSIGN expression
    | IDENTIFIER ASSIGN expression const_spec'''
    p[0] = p[3]


# Lista de especificaciones de constante
def p_const_spec_list(p):
    '''const_spec_list : const_spec
    | const_spec_list const_spec'''
    if len(p)== 4:
        p[0] = p[3]
    else:
        p[0] = p[1]


# Declaración de variable
def p_var_declaration(p):
    '''var_declaration : VAR var_spec
    | VAR LPAREN var_spec_list RPAREN'''
    if len(p) == 3:
        p[0] = p[2]
        if isinstance(p[2], tuple):
            nombre, valor = p[2]
            nombres[nombre] = valor
            variables_inicializadas[nombre] = True
            print(f'Variable {nombre} inicializada')
    else:
        p[0] = p[3]


# Especificación de variable
def p_var_spec(p):
    '''var_spec : IDENTIFIER type
    | IDENTIFIER type ASSIGN expression
    | IDENTIFIER type ASSIGN expression var_spec'''
    p[0] = p[2]


# Lista de especificaciones de variable
def p_var_spec_list(p):
    '''var_spec_list : var_spec
    | var_spec_list var_spec
    '''
    p[0] = p[1]

# Expresión
# Expresión atómica
def p_expression_atomic(p):
    '''expression : IDENTIFIER
                | INT_LIT
                | FLOAT_LIT
                | IMAGINARY_LIT
                | RUNE_LIT
                | STRING_LIT
                | LPAREN expression RPAREN'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]

# Operaciones binarias
def p_expression_binop(p):
    '''expression : expression PLUS expression
                | expression MINUS expression
                | expression TIMES expression
                | expression DIVIDE expression
                | expression MOD expression
                | expression AND expression
                | expression OR expression
                | expression XOR expression
                | expression LSHIFT expression
                | expression RSHIFT expression
                | expression AND_NOT expression
                | expression PLUS_ASSIGN expression
                | expression MINUS_ASSIGN expression
                | expression TIMES_ASSIGN expression
                | expression DIVIDE_ASSIGN expression
                | expression MOD_ASSIGN expression
                | expression AND_ASSIGN expression
                | expression OR_ASSIGN expression
                | expression XOR_ASSIGN expression
                | expression LSHIFT_ASSIGN expression
                | expression RSHIFT_ASSIGN expression
                | expression AND_NOT_ASSIGN expression
                | expression AND_AND expression
                | expression OR_OR expression
                | expression ARROW expression
                | expression EQL expression
                | expression NEQ expression
                | expression LSS expression
                | expression LEQ expression
                | expression GTR expression
                | expression GEQ expression
                | expression ASSIGN expression
                | expression DECLARE_ASSIGN expression
                | expression NOT expression
                | expression ELLIPSIS expression
                | expression LBRACK expression RBRACK
                | expression LBRACE expression RBRACE
                | expression COMMA expression
                | expression PERIOD expression
                | expression COLON expression'''
    # Aquí puedes manejar las operaciones binarias
    resultado_verificacion = verificar_tipos_operacion_math(p[1], p[2], p[3])

    if resultado_verificacion == 'op_numerica':
        if p[2] == '+':
            p[0] = p[1] + p[3]
        elif p[2] == '-':
            p[0] = p[1] - p[3]
        elif p[2] == '*':
            p[0] = p[1] * p[3]
        elif p[2] == '/':
            p[0] = p[1] / p[3]
        elif p[2] == '%':
            p[0] = p[1] % p[3]
        elif p[2] == '**':
            p[0] = p[1] ** p[3]

    elif resultado_verificacion == 'op_cadenas':
        p[0] = p[1] + p[3]
    elif p[2] == '==':
        p[0] = verificar_tipos(p[1], p[2], p[3]) and p[1] == p[3]
    elif p[2] == '!=':
        p[0] = verificar_tipos(p[1], p[2], p[3]) and p[1] != p[3]
    elif p[2] == '<':
        p[0] = verificar_tipos(p[1], p[2], p[3]) and p[1] < p[3]
    elif p[2] == '<=':
        p[0] = verificar_tipos(p[1], p[2], p[3]) and p[1] <= p[3]
    elif p[2] == '>':
        p[0] = verificar_tipos(p[1], p[2], p[3]) and p[1] > p[3]
    elif p[2] == '>=':
        p[0] = verificar_tipos(p[1], p[2], p[3]) and p[1] >= p[3]
    elif p[2] == '&&':
        p[0] = p[1] and p[3]
    elif p[2] == '||':
        p[0] = p[1] or p[3]
    elif p[2] == '!':
        p[0] = p[1] is not p[3]
    # Otras operaciones binarias...

# Operaciones unarias
def p_expression_unop(p):
    '''expression : INC expression
                | DEC expression
                | NOT expression'''
    if p[1] == '++':
        p[0] = p[2] + 1
    elif p[1] == '--':
        p[0] = p[2] - 1
    elif p[1] == '!':
        p[0] = not p[2]

# Regla para saltos de línea
def p_empty_line(p):
    'empty_line :'
    p[0] = (
        'Linea en Blanco'  # Retorna una cadena vacía para representar una línea en blanco
    )


# Regla para errores de sintaxis
def p_error(p):
    if p:
        error_message = (
            f"Error de sintaxis en la posición {p.lexpos}: Token '{p.value}' inesperado"
        )
    else:
        error_message = 'Error de sintaxis: se expera un token'
    raise SyntaxError(error_message)


# Instanciar el analizador
parser = yacc.yacc()


# Función para analizar una expresión
def parse(data):
    error_message = None  # Inicializa la variable error_message
    resultado = None  # Inicializa la variable resultado
    try:
        resultado = parser.parse(data, tracking=True)
        if resultado is not None:
            return str(resultado) + ' ,Sintaxis correcta'
        else:
            return 'Sintaxis correcta'

    except SyntaxError as e:
        error_message = str(e)
        print('Error:', error_message)
        return error_message
