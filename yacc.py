# Yacc example

import ply.yacc as yacc

# Get the token map from the lexer.  This is required.
from lex import tokens
from objects import Complex

def p_expression_reductions(p):
    '''
    expr_1      :   expr_2
    expr_2      :   expr_3
    expr_3      :   expr_4
    expr_4      :   expr_5
    '''
    p[0] = p[1]
    return p

def p_expression_imaginary(p):
    '''
    expr_5      :   IMAGINARY
    '''
    p[0] = Complex(0, 1)

def p_expression_rational(p):
    '''
    expr_5      :   RATIONAL
    '''
    p[0] = Complex(p[1], 0)

def p_unary_operations(p):
    '''
    expr_1      :   MINUS expr_2
    '''
    p[0] = -p[1]
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
        p[0] = p[1] ** p[3]
    return p

def p_factor_expr(p):
    'expr_5 : LPAREN expr_1 RPAREN'
    p[0] = p[2]
    return p

# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")

# Build the parser
parser = yacc.yacc()

while True:
    try:
        s = input('> ')
    except EOFError:
        break
    if not s: continue
    result = parser.parse(s)
    print(result)
