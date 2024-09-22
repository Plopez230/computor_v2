# Yacc example

import ply.yacc as yacc

# Get the token map from the lexer.  This is required.
from lex import tokens
from objects import Complex, Matrix, Function, Polynomial, MathError


class SyntaxError(Exception):
    pass


variables = {}
function_variable = None

def p_sentence(p):
    '''
    sentence    :   assig
    sentence    :   expr_1
    sentence    :   type_sent
    '''
    p[0] = p[1]
    return p

def p_type(p):
    '''
    type_sent   :   TYPE LPAREN expr_1 RPAREN
    '''
    p[0] = p[3].__class__.__name__
    return p

def p_assignment(p):
    '''
    assig       :   name ASSIGNMENT expr_1
    '''
    global function_variable
    function_variable = None
    variables[p[1]] = p[3]
    p[0] = p[3]
    return p

def p_name_variable(p):
    '''
    name        :   IDENTIFIER
    '''
    p[0] = p[1]
    return p

def p_name_function(p):
    '''
    name        :   IDENTIFIER LPAREN IDENTIFIER RPAREN
    '''
    global function_variable
    function_variable = p[3]
    p[0] = p[1]
    return p

def p_expression_reductions(p):
    '''
    expr_1      :   expr_2
    expr_2      :   expr_3
    expr_3      :   expr_4
    expr_4      :   expr_5
    expr_5      :   expr_6
    '''
    p[0] = p[1]
    return p

def p_expression_imaginary(p):
    '''
    expr_6      :   IMAGINARY
    '''
    p[0] = Complex(0, 1)
    return p

def p_expression_identifier(p):
    '''
    expr_6      :   IDENTIFIER
    '''
    global function_variable
    if p[1] == function_variable:
        p[0] = Polynomial(t=[[Complex(1, 0), Complex(1, 0)]])
    elif p[1] in variables:
        p[0] = variables[p[1]]
    else:
        raise SyntaxError(f"Variable '{p[1]}' does not exist")
    return p

def p_expression_function(p):
    '''
    expr_6      :   IDENTIFIER LPAREN IDENTIFIER RPAREN
                |   IDENTIFIER LPAREN expr_1 RPAREN
    '''
    if p[1] not in variables:
        raise SyntaxError(f"Function '{p[1]}' does not exist")
    function = variables[p[1]]
    
    if isinstance(p[3], str):
        global function_variable
        if p[3] == function_variable:
            p[0] = Function()
        elif p[3] in variables:
            p[0] = variables[p[3]]
        else:
            raise SyntaxError(f"Variable '{p[3]}' does not exist")

    if isinstance(p[3], Complex):
        p[0] = function.eval(p[3])
    
    return p

def p_expression_rational(p):
    '''
    expr_6      :   RATIONAL
    '''
    p[0] = Complex(p[1], 0)
    return p

def p_unary_operations(p):
    '''
    expr_5      :   MINUS expr_5
    '''
    p[0] = -p[2]
    return p

def p_binary_operations(p):
    '''
    expr_1      :   expr_1 PLUS expr_2
                |   expr_1 MINUS expr_2
    expr_2      :   expr_2 MODULUS expr_3
    expr_3      :   expr_3 TIMES expr_4
                |   expr_3 DIVIDE expr_4
    expr_4      :   expr_4 POWER expr_5
                |   expr_4 TIMESMATRIX expr_5
                |   expr_4 POWERMATRIX expr_5
    '''
    if p[2] == '+':
        p[0] = p[1] + p[3]
    if p[2] == '-':
        p[0] = p[1] - p[3]
    if p[2] == '*':
        p[0] = p[1] * p[3]
    if p[2] == '/':
        p[0] = p[1] / p[3]
    if p[2] == '%':
        p[0] = p[1] % p[3]
    if p[2] == '^':
        p[0] = p[1] ** p[3]
    if p[2] == '**':
        p[0] = p[1].mat_mul(p[3])
    if p[2] == '^^':
        p[0] = p[1].mat_pow(p[3])
    return p

def p_factor_expr(p):
    'expr_6     :   LPAREN expr_1 RPAREN'
    p[0] = p[2]
    return p

def p_factor_matrix(p):
    'expr_6     :   LBRACK vec_list RBRACK'
    p[0] = Matrix(p[2])
    return p

def p_matrix_list_n(p):
    '''
    vec_list    :   LBRACK expr_list RBRACK SEMICOLON vec_list
    '''
    p[0] = p[5]
    p[0].insert(0, p[2])
    return p

def p_matrix_list_1(p):
    '''
    vec_list    :   LBRACK expr_list RBRACK
    '''
    p[0] = [p[2]]
    return p

def p_expr_list_n(p):
    '''
    expr_list   :   expr_1 COMMA expr_list
    '''
    p[0] = p[3]
    p[0].insert(0, p[1])
    return p

def p_expr_list_1(p):
    '''
    expr_list   :   expr_1
    '''
    p[0] = [p[1]]
    return p

# Error rule for syntax errors
def p_error(p):
    msg = f"  {' ' * p.lexpos}^\n"
    msg += f"Syntax error: {p.value}"
    raise SyntaxError(msg)

# Build the parser
parser = yacc.yacc()

while True:
    try:
        s = input('> ')
    except EOFError:
        break
    if not s: continue
    try:
        result = parser.parse(s)
        print(result)
    except SyntaxError as e:
        print (f"\033[1;31m{e}\033[0m")
    except MathError as e:
        print (f"\033[1;31mMath error: {e}\033[0m")
    except ZeroDivisionError as e:
        print (f"\033[1;31mDivision by 0\033[0m")
