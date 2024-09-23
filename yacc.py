# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    yacc.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: plopez-b <plopez-b@student.42malaga.com    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/09/23 14:26:08 by plopez-b          #+#    #+#              #
#    Updated: 2024/09/23 14:26:13 by plopez-b         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

# Yacc example

import ply.yacc as yacc

# Get the token map from the lexer.  This is required.
from lex import tokens
from objects import Complex, Matrix
from exceptions import *
from symbols import symbol_table

precedence = (
    ('left', "QUESTION"),
    ('left', "ASSIGNMENT"),
    ('left', "PLUS", "MINUS"),
    ('left', "MODULUS"),
    ('left', "TIMES", "DIVIDE"),
    ('left', "POWER", "TIMESMATRIX", "POWERMATRIX"),
    ('right', "UMINUS"),
)

def p_sentence(p):
    '''
    sentence    :   assig
                |   value
                |   eval
                |   func_symbols
    '''
    p[0] = p[1]
    return p

def p_func_symbols(p):
    '''
    func_symbols    :   SYMBOLS
    '''
    p[0] = str(symbol_table)
    return p

def p_assig(p):
    '''
    assig       :   expr r_assign expr
    '''
    if symbol_table.can_assign(p[1]):
        symbol_table.assign(p[1].name, p[3])
    p[0] = p[3]
    return p

def p_value(p):
    '''
    value       :   expr r_assign QUESTION
    '''
    symbol_table.is_defined(p[1])
    p[0] = p[1]
    return p

def p_eval(p):
    '''
    eval        :   expr r_assign expr QUESTION
    '''
    symbol_table.is_defined(p[1])
    p[0] = p[1]
    return p

def p_r_assign(p):
    '''
    r_assign    :   ASSIGNMENT
    '''
    symbol_table.assignment()
    return p

def p_expression_identifier(p):
    '''
    expr      :   IDENTIFIER
    '''
    value = symbol_table.variable(p[1])
    p[0] = value
    return p

def p_expression_function(p):
    '''
    expr      :   IDENTIFIER LPAREN expr RPAREN
    '''
    function = symbol_table.function(p[1])
    value = function.eval(p[3])
    p[0] = value
    return p

def p_expression_imaginary(p):
    '''
    expr      :   IMAGINARY
    '''
    p[0] = Complex(0, 1)
    return p

def p_expression_rational(p):
    '''
    expr      :   RATIONAL
    '''
    p[0] = Complex(p[1], 0)
    return p

def p_unary_operations(p):
    '''
    expr        :   MINUS expr %prec UMINUS
    '''
    p[0] = -p[2]
    return p

def p_binary_operations(p):
    '''
    expr        :   expr PLUS expr
                |   expr MINUS expr
                |   expr MODULUS expr
                |   expr TIMES expr
                |   expr DIVIDE expr
                |   expr POWER expr
                |   expr TIMESMATRIX expr
                |   expr POWERMATRIX expr
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
    'expr     :   LPAREN expr RPAREN'
    p[0] = p[2]
    return p

def p_factor_matrix(p):
    'expr     :   LBRACK vec_list RBRACK'
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
    expr_list   :   expr COMMA expr_list
    '''
    p[0] = p[3]
    p[0].insert(0, p[1])
    return p

def p_expr_list_1(p):
    '''
    expr_list   :   expr
    '''
    p[0] = [p[1]]
    return p

# Error rule for syntax errors
def p_error(p):
    msg = f"Syntax error."
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
        symbol_table.new_line()
        result = parser.parse(s)
        print(result)
    except SyntaxError as e:
        print (f"\033[1;31m{e}\033[0m")
    except MathError as e:
        print (f"\033[1;31mMath error: {e}\033[0m")
    except ZeroDivisionError as e:
        print (f"\033[1;31mDivision by 0\033[0m")
