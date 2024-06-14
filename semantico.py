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
    

# Definimos una estructura de entorno para mantener las declaraciones de variables y funciones

def declare_variable(variable_inicializada, name):
    if name in variable_inicializada:
        if f"Variable '{name}' is already declared" not in errores:
            errores.append(f"Variable '{name}' is already declared.")

def lookup_variable(variables, name):
    if name not in variables:
        errores.append(f"Variable '{name}' is not declared.")
        
def declare_function(funciones, name):
    if name in funciones:
        errores.append(f"Function '{name}' is already declared.")
        

def lookup_function(funciones, name):
    if name not in funciones:
        errores.append(f"Function '{name}' is not declared.")

def declare_type(tipos, name):
    if name in tipos:
        errores.append(f"Type '{name}' is already declared.")

def lookup_type(tipos, name):
    if name not in tipos:
        errores.append(f"Type '{name}' is not declared.")
        
def declare_import(importaciones, name):
    if name in importaciones:
        errores.append(f"Import '{name}' is already declared.")
        
def lookup_import(importaciones, name):
    if name not in importaciones:
        errores.append(f"Import '{name}' is not declared.")

# Definimos una función para verificar la asignación de tipos
def verificar_asignacion_tipos(variables_inicializadas, name, var_type, value):
    if name in variables_inicializadas:
        if variables_inicializadas[name]!= var_type:
            errores.append(f"Variable '{name}' redeclarada con tipo diferente.")
    else:
        variables_inicializadas[name] = var_type

    return variables_inicializadas

# Definimos una función para verificar la asignación de tipos a funciones
def verificar_asignacion_tipos_funciones(funciones, name, return_type, param_types):
    if name in funciones:
        if funciones[name]!= (return_type, param_types):
            errores.append(f"Function '{name}' redeclarada con tipo diferente.")
    else:
        funciones[name] = (return_type, param_types)

    return funciones

# Definimos una función para verificar la asignación de tipos a variables
def verificar_asignacion_tipos_variables(variables, name, var_type):
    if name in variables:
        if variables[name]!= var_type:
            errores.append(f"Variable '{name}' redeclarada con tipo diferente.")
    else:
        variables[name] = var_type

    return variables