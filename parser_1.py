import ply.yacc as yacc

from semantico import *

variables_inicializadas = {}

# Definición de precedencia para los operadores
precedence = (
    ("nonassoc", "MENORQUE", "MAYORQUE", "MENORIGUAL", "MAYORIGUAL"),
    ("right", "OP_ASIGNAR"),
    ("left", "OP_SUMAR", "OP_RESTAR"),
    (
        "left",
        "OP_MULTIPLICAR",
        "OP_DIVIDIR",
        "MODULO",
    ),
    ("left", "PARENTESIS_IZQ", "PARENTESIS_DER"),
    ("right", "UMINUS"),  # Para el operador unario negativo
    ("left", "POTENCIA"),
)


# Diccionario para almacenar los nombres y sus valores
nombres = {}


# Regla para las sentencias (statements)
def p_statement(p):
    """statement : ID OP_ASIGNAR expression
    | ID OP_ASIGNAR ENTERO
    | expression
    | print_statement
    | COMENTARIO_UNA_LINEA
    | empty_line
    | import_statement
    | declaracion_clase"""
    if len(p) == 2:
        p[0] = p[1]
    else:
        nombres[p[1]] = p[3]
        variables_inicializadas[p[1]] = True  # Marca la variable como inicializada
        print(f"Variable {p[1]} inicializada")
        p[0] = p[3]


def p_expression_arithmetic(p):
    """expression : expression OP_SUMAR expression
    | expression OP_RESTAR expression
    | expression OP_MULTIPLICAR expression
    | expression OP_DIVIDIR expression
    | expression MODULO expression
    | expression MAS_MAS
    | expression POTENCIA expression"""
    resultado_verificacion = verificar_tipos_operacion_math(p[1], p[2], p[3])

    if resultado_verificacion == "op_numerica":
        if p[2] == "+":
            p[0] = p[1] + p[3]
        elif p[2] == "-":
            p[0] = p[1] - p[3]
        elif p[2] == "*":
            p[0] = p[1] * p[3]
        elif p[2] == "/":
            p[0] = p[1] / p[3]
        elif p[2] == "%":
            p[0] = p[1] % p[3]
        elif p[2] == "**":
            p[0] = p[1] ** p[3]
    elif resultado_verificacion == "op_cadenas":
        p[0] = p[1] + p[3]


# Regla de parentesis
def p_expression_group(p):
    """expression : PARENTESIS_IZQ expression PARENTESIS_DER"""
    if len(p) == 4:
        p[0] = p[2]
    else:
        print("Error: Falta el paréntesis de cierre en la expresión.")
        p[0] = None


# Regla para números (enteros y flotantes)
def p_expression_number(p):
    """expression : ENTERO
    | FLOTANTE"""
    p[0] = p[1]


# Regla para cadenas de texto y caracteres
def p_expression_string(p):
    """expression : CADENA
    | CARACTER"""
    p[0] = p[1]


# Regla para identificadores
def p_expression_identifier(p):
    "expression : ID"
    variable_name = p[1]
    verificar_variable_inicializada(variables_inicializadas, variable_name)
    p[0] = nombres.get(variable_name, None)


# Regla para operador de negación unario
def p_expression_unary_minus(p):
    "expression : OP_RESTAR expression %prec UMINUS"
    p[0] = -p[2]


# Ejemplo: t1 = y + 2
def p_t1_assignment(p):
    "statement : ID OP_ASIGNAR expression OP_SUMAR expression"
    t1_value = nombres.get(p[3], 0) + p[5]
    nombres[p[1]] = t1_value
    p[0] = t1_value


# Regla para instrucción print
def p_print_statement(p):
    "print_statement : PRINT1 PUNTO PRINT2 PUNTO PRINT3 PARENTESIS_IZQ CADENA OP_SUMAR expression PARENTESIS_DER PUNTO_COMA"
    print_args = p[3] 
    formatted_string = " ".join(map(str, print_args))
    print(formatted_string)
    p[0] = formatted_string


# Regla para argumentos de impresión


def p_print_args(p):
    """
    print_args : print_arg
            | print_args COMA print_arg
            | list_access

    """
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]


def p_print_arg(p):
    """
    print_arg : expression
            | ID
            | VERDADERO
            | FALSO
            | CADENA
            | ENTERO
            | FLOTANTE
    """
    p[0] = p[1]


# Regla para acceso a listas
def p_list_access(p):
    "list_access : ID CORCHETE_IZQ expression CORCHETE_DER"
    list_name = p[1]
    index = p[3]
    p[0] = f"{list_name}[{index}]"


# Expresiones de comparación
def p_expression_comparison(p):
    """expression : expression IGUAL expression
    | expression MAYORQUE expression
    | expression MAYORIGUAL expression
    | expression MENORQUE expression
    | expression MENORIGUAL expression
    | expression DIFERENTE expression"""
    if p[2] == "==":
        p[0] = verificar_tipos(p[1], p[2], p[3]) and p[1] == p[3]
    elif p[2] == ">":
        p[0] = verificar_tipos(p[1], p[2], p[3]) and p[1] > p[3]
    elif p[2] == ">=":
        p[0] = verificar_tipos(p[1], p[2], p[3]) and p[1] >= p[3]
    elif p[2] == "<":
        p[0] = verificar_tipos(p[1], p[2], p[3]) and p[1] < p[3]
    elif p[2] == "<=":
        p[0] = verificar_tipos(p[1], p[2], p[3]) and p[1] <= p[3]
    elif p[2] == "!=":
        p[0] = verificar_tipos(p[1], p[2], p[3]) and p[1] != p[3]


# Gramática para expresiones booleanas
def p_expresion_booleana(t):
    """
    expression   :   expression OP_LOGICO_Y expression
                |   expression OP_LOGICO_O expression
                |   expression OP_LOGICO_NOT expression
                |  PARENTESIS_IZQ expression OP_LOGICO_Y expression PARENTESIS_DER
                |  PARENTESIS_IZQ expression OP_LOGICO_O expression PARENTESIS_DER
                |  PARENTESIS_IZQ expression OP_LOGICO_NOT expression PARENTESIS_DER
    """
    if t[2] == "&&":
        t[0] = t[1] and t[3]
    elif t[2] == "||":
        t[0] = t[1] or t[3]
    elif t[2] == "!":
        t[0] = t[1] is not t[3]
    elif t[3] == "&&":
        t[0] = t[2] and t[4]
    elif t[3] == "||":
        t[0] = t[2] or t[4]
    elif t[3] == "!":
        t[0] = t[2] is not t[4]


# Gramática para la estructura condicional if
def p_if_statement(p):
    """statement : SI expression LLAVE_IZQ
    | SI expression"""
    if len(p) < 4 or p[3] != "{":
        p[0] = "Error de sintaxis: Se esperaba '{' al final de la expresión 'if'"
    # Aquí puedes manejar la ejecución del bloque de código dentro del 'if'
    elif p[2]:
        p[0] = "La condición es verdadera"
    else:
        p[0] = "La condición es falsa"


def p_elif_statement(p):
    """statement : SINOSI expression LLAVE_IZQ
    | SINOSI expression"""
    if len(p) < 4 or p[3] != "{":
        p[0] = "Error de sintaxis: Se esperaba '{' al final de la expresión 'elif'"
    # Aquí puedes manejar la ejecución del bloque de código dentro del 'elif'
    elif p[2]:
        p[0] = "La condición del 'elif' es verdadera"
    else:
        p[0] = "La condición del 'elif' es falsa"


# Gramática para la estructura condicional else
def p_else_statement(p):
    """statement : SINO LLAVE_IZQ
    | SINO"""
    if len(p) < 3 or p[2] != "{":
        p[0] = "Error de sintaxis: Se esperaba '{' al final de la expresión 'else'"
    else:
        p[0] = "La condición del 'else'"


# Regla para la asignación de listas
def p_assignment_list(p):
    "statement : ID OP_ASIGNAR lista"
    nombres[p[1]] = p[3]
    p[0] = p[3]


# Regla para definición de listas
def p_lista(p):
    "lista : CORCHETE_IZQ elementos CORCHETE_DER"
    p[0] = p[2]


# Regla para elementos de una lista
def p_elementos(p):
    """elementos : expression
    | expression COMA elementos
    """
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]


# Gramática para la estructura de control 'for'
def p_for_statement(p):
    """statement : PARA ID EN ID LLAVE_IZQ
    | PARA ID EN RANGO PARENTESIS_IZQ expression PARENTESIS_DER LLAVE_IZQ
    | PARA PARENTESIS_IZQ ID OP_ASIGNAR expression PUNTO_COMA expression PUNTO_COMA ID MAS_MAS PARENTESIS_DER LLAVE_IZQ statement LLAVE_DER"""
    if len(p) == 6:
        p[0] = f'La sentencia for recorre "{p[4]}" usando la variable {p[2]}'
    elif len(p) == 9:
        p[0] = (
            f"La sentencia for recorre  usando la variable {p[2]} en un rango de {p[6]}"
        )


# Gramática para la estructura de control 'while'
def p_while_statement(p):
    "statement : MIENTRAS expression LLAVE_IZQ"
    # Aquí puedes manejar la ejecución del bloque de código dentro del bucle 'while'
    if p[2]:
        p[0] = "La condición es verdadera"
    else:
        p[0] = "La condición es falsa"


# Regla para el operador de incremento
def p_increment_statement(p):
    "statement : ID OP_INCREMENTO ENTERO"
    # Aquí puedes manejar la operación de incremento
    variable_name = p[1]
    increment_value = p[3]
    nombres[variable_name] += increment_value
    p[0] = f"{variable_name} ha sido incrementado en {increment_value}"


# Regla para la definición de funciones
def p_function_definition(p):
    "statement : DEFINE_FUNCIONES ID PARENTESIS_IZQ parametros PARENTESIS_DER DOS_PUNTOS"
    function_name = p[2]
    parameters = p[4]
    p[0] = f"Definición de función: {function_name}({', '.join(parameters)})"


# Regla para parámetros de funciones
def p_parametros(p):
    """parametros : ID
    | ID COMA parametros"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]


# Regla para la llamada de funciones
def p_function_call(p):
    "statement : ID PARENTESIS_IZQ expression PARENTESIS_DER"
    function_name = p[1]
    argument = p[3]
    # Puedes manejar la llamada a la función aquí, como verificar si la función existe y procesar los argumentos.
    if p[1]:
        p[0] = f"Llamada a la función {function_name} con argumento: {argument}"
    else:
        p[0] = (
            f"Llamada a la función {function_name} con argumento: {argument} (No definida)"
        )


# Regla para la importación de módulos matemáticos
def p_import_math(p):
    "import_statement : IMPORTAR MODULO_MATEMATICO"
    p[0] = "Importar el módulo math"


# Regla para declaraciones de clase
def p_declaracion_clase(p):
    "declaracion_clase : CLASE ID DOS_PUNTOS"
    # Aquí puedes manejar la declaración de la clase
    p[0] = f"Declaración de clase: {p[2]}"


# Regla para saltos de línea
def p_empty_line(p):
    "empty_line :"
    p[0] = (
        "Linea en Blanco"  # Retorna una cadena vacía para representar una línea en blanco
    )


# Regla para errores de sintaxis
def p_error(p):
    if p:
        error_message = (
            f"Error de sintaxis en la posición {p.lexpos}: Token '{p.value}' inesperado"
        )
    else:
        error_message = "Error de sintaxis: se expera un token"
    raise SyntaxError(error_message)


# Instanciar el analizador
parser = yacc.yacc()


# Función para analizar una expresión
def parse(expression):
    error_message = None  # Inicializa la variable error_message
    resultado = None  # Inicializa la variable resultado
    try:
        resultado = parser.parse(expression)
        if resultado is not None:
            return str(resultado) + " ,Sintaxis correcta"
        else:
            return "Sintaxis correcta"

    except SyntaxError as e:
        error_message = str(e)
        print("Error:", error_message)
        return error_message
