import ply.yacc as yacc

# Importa los tokens del analizador léxico
from lexer import tokens

#Reglas semanticas
errores = []

def verificar_variable_inicializada(variables_inicializadas, variable_name):
    if variable_name not in variables_inicializadas:
        if f"Variable '{variable_name}' no inicializada antes de su uso" not in errores:
            errores.append(f"Variable '{variable_name}' no inicializada antes de su uso")

def verificar_tipos_operacion_math(exp1, op, exp2):
    if exp1 is None or exp2 is None:
        errores.append("No se puede operar con valores Nulos")
    elif isinstance(exp1, (int, float)) and isinstance(exp2, (int, float)):
        if op in ['+', '-', '*', '/', '%', '**']:
            if exp2 == 0:
                errores.append("No se puede dividir entre 0")
            else:
                return "op_numerica"  # Operación numérica
        else:
            errores.append("Operador no permitido entre números")
    elif isinstance(exp1, str) and isinstance(exp2, str):
        if op == '+':
            return "op_cadenas"  # Concatenación de cadenas
        else:
            errores.append("Operador no permitido para textos")
    else:
        errores.append("Tipos de expresiones no compatibles")


def verificar_tipos(op1, operador, op2):
    tipo_op1 = type(op1)
    tipo_op2 = type(op2)

    if operador == '==' or operador == '!=':
        # Permitir comparaciones de igualdad y desigualdad para cualquier tipo
        return True
    elif tipo_op1 == int and tipo_op2 == int:
        # Permitir comparaciones de orden solo para enteros
        return True
    elif tipo_op1 == str and tipo_op2 == str:
        # Permitir comparaciones de orden solo para cadenas
        return True
    else:
        # Restringir comparaciones de orden para otros tipos
        errores.append(f"Error: No se pueden comparar variables de tipos diferentes ({tipo_op1} y {tipo_op2}) usando '{operador}'")
        return False